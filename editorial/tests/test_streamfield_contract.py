from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from wagtail.rich_text import RichText

from editorial.models import BlogPostPage, EulaPage, HomePage, ServicePage


class StreamFieldContractTests(SimpleTestCase):
    def test_article_body_exposes_only_restricted_rich_text_block(self):
        stream_block = BlogPostPage._meta.get_field("body").stream_block
        body_block_names = set(stream_block.child_blocks)
        self.assertEqual(body_block_names, {"rich_text", "image"})
        self.assertEqual(
            set(stream_block.child_blocks["rich_text"].features),
            {"h2", "h3", "h4", "bold", "italic", "ol", "ul", "link"},
        )

        with self.assertRaises(KeyError):
            stream_block.child_blocks["raw_html"]

    def test_article_image_block_is_typed_accessible_and_rejects_unsupported_alignment(self):
        block = BlogPostPage._meta.get_field("body").stream_block.child_blocks["image"]
        self.assertEqual(
            set(block.child_blocks),
            {"image", "decorative", "alt_text", "caption", "alignment"},
        )
        self.assertEqual(
            set(block.child_blocks["alignment"].field.choices),
            {("", "---------"), ("left", "Izquierda"), ("right", "Derecha")},
        )
        self.assertFalse(block.child_blocks["caption"].required)

    def test_home_sections_are_limited_to_audited_components(self):
        sections = HomePage._meta.get_field("sections").stream_block.child_blocks
        self.assertEqual(
            set(sections),
            {
                "service_links",
                "service_carousel",
                "partner",
                "about",
                "text_section",
                "contact_section",
            },
        )
        with self.assertRaises(KeyError):
            sections["raw_html"]
        with self.assertRaises(ValidationError):
            sections["text_section"].clean({"heading": "", "body": RichText("")})

    def test_article_streamfield_round_trip_preserves_order_and_values(self):
        field = BlogPostPage._meta.get_field("body")
        initial = field.to_python(
            [
                {"type": "rich_text", "value": "<p>Primero</p>", "id": "first"},
                {"type": "rich_text", "value": "<p>Segundo</p>", "id": "second"},
            ]
        )

        restored = field.to_python(field.get_prep_value(initial))

        self.assertEqual([block.block_type for block in restored], ["rich_text", "rich_text"])
        self.assertEqual([str(block.value) for block in restored], ["<p>Primero</p>", "<p>Segundo</p>"])

    def test_service_fields_preserve_ordered_repeating_content(self):
        offering = ServicePage._meta.get_field("content_blocks").stream_block.child_blocks
        self.assertEqual(set(offering), {"offering"})
        with self.assertRaises(ValidationError):
            offering["offering"].clean({"title": "", "icon": None})
        self.assertEqual(set(ServicePage._meta.get_field("tools").stream_block.child_blocks), {"tool"})

    def test_eula_rich_text_features_are_restricted(self):
        self.assertEqual(
            set(EulaPage._meta.get_field("legal_body").features),
            {"h2", "h3", "h4", "bold", "italic", "ol", "ul", "link"},
        )
