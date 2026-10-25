"""Typed Wagtail blocks backed by the public-site audit."""

from django.core.exceptions import ValidationError
from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.images.blocks import ImageBlock, ImageChooserBlock


RICH_TEXT_FEATURES = ["h2", "h3", "h4", "bold", "italic", "ol", "ul", "link"]


class ArticleImageBlock(blocks.StructBlock):
    """Article image with explicit accessibility and audited alignment options."""

    image = ImageChooserBlock(label="Imagen")
    decorative = blocks.BooleanBlock(
        required=False,
        default=False,
        label="Imagen decorativa",
    )
    alt_text = blocks.CharBlock(required=False, label="Texto alternativo")
    caption = blocks.TextBlock(required=False, label="Leyenda")
    alignment = blocks.ChoiceBlock(
        choices=[("left", "Izquierda"), ("right", "Derecha")],
        required=False,
        default="",
        label="Alineación",
    )

    def clean(self, value):
        value = super().clean(value)
        if (
            value["image"]
            and not value["decorative"]
            and not (value["alt_text"] or "").strip()
        ):
            raise StructBlockValidationError(
                block_errors={
                    "alt_text": ValidationError(
                        "Añade un texto alternativo o marca la imagen como decorativa."
                    )
                }
            )
        return value

    class Meta:
        icon = "image"
        label = "Imagen de artículo"


class ImageGroupBlock(blocks.StructBlock):
    """One ProcessWire repeater row containing an ordered image collection."""

    images = blocks.ListBlock(ImageBlock(), required=False)


class ServiceLinkItemBlock(blocks.StructBlock):
    label = blocks.CharBlock(max_length=100)
    service_page = blocks.PageChooserBlock(page_type=["editorial.ServicePage"])


class ServiceLinksSectionBlock(blocks.StructBlock):
    items = blocks.ListBlock(ServiceLinkItemBlock(), required=False)


class ServiceCarouselSectionBlock(blocks.StructBlock):
    # The outer list preserves the four audited repeater records; each record
    # retains its own image order without flattening the source relationship.
    groups = blocks.ListBlock(ImageGroupBlock(), required=False)


class PartnerSectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120, required=False)
    authorized_partner_image = ImageBlock()
    products_image = ImageBlock()
    cta_label = blocks.CharBlock(max_length=80, required=False)
    cta_url = blocks.URLBlock(required=False)


class AboutSectionBlock(blocks.StructBlock):
    description = blocks.RichTextBlock(features=RICH_TEXT_FEATURES, required=False)
    image_groups = blocks.ListBlock(ImageGroupBlock(), required=False)
    careers_label = blocks.CharBlock(max_length=80, required=False)
    careers_url = blocks.URLBlock(required=False)


class TextSectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=160)
    body = blocks.RichTextBlock(features=RICH_TEXT_FEATURES)


class ContactSectionBlock(blocks.StructBlock):
    """Editorial heading only; submissions and provider configuration are separate."""

    heading = blocks.CharBlock(max_length=120, required=False)


class ServiceOfferingBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=200)
    icon = ImageBlock()
    description = blocks.RichTextBlock(features=RICH_TEXT_FEATURES, required=False)
