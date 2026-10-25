from django.core.exceptions import ValidationError
from django.http import Http404
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.functions import Lower
from django.utils.text import slugify
from modelcluster.fields import ParentalManyToManyField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField, StreamField
from wagtail.images import get_image_model_string
from wagtail.images.blocks import ImageBlock
from wagtail.models import Page
from wagtail.snippets.models import register_snippet

from .blocks import (
    AboutSectionBlock,
    ArticleImageBlock,
    ContactSectionBlock,
    PartnerSectionBlock,
    RICH_TEXT_FEATURES,
    ServiceCarouselSectionBlock,
    ServiceLinksSectionBlock,
    ServiceOfferingBlock,
    TextSectionBlock,
)


ASCII_SLUG_VALIDATOR = RegexValidator(
    regex=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    message="Usa minúsculas ASCII separadas por guiones, sin espacios ni signos.",
)


def _path_relative_to_home(page):
    """Return a page path relative to the configured HomePage tree root."""
    home = next(
        (
            ancestor
            for ancestor in page.get_ancestors(inclusive=True)
            if ancestor.specific_class is HomePage
        ),
        None,
    )
    if home is None:
        return None

    relative_path = page.url_path[len(home.url_path) :]
    return f"/{relative_path}" if relative_path else "/"


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(
        max_length=120,
        unique=True,
        validators=[ASCII_SLUG_VALIDATOR],
    )
    sort_order = models.PositiveSmallIntegerField(default=0)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("sort_order"),
    ]

    class Meta:
        ordering = ("sort_order", "name")
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="editorial_blogcategory_name_ci_uniq",
            ),
        ]
        verbose_name = "categoría del blog"
        verbose_name_plural = "categorías del blog"

    def clean(self):
        super().clean()
        if self.slug and slugify(self.slug, allow_unicode=False) != self.slug:
            raise ValidationError({"slug": "El slug debe estar normalizado en ASCII."})

    def __str__(self):
        return self.name


class RouteContainerPage(Page):
    """Non-editorial live tree nodes required to preserve descendant paths."""

    parent_page_types = ["editorial.HomePage", "editorial.RouteContainerPage"]
    subpage_types = [
        "editorial.RouteContainerPage",
        "editorial.BlogIndexPage",
        "editorial.ServicePage",
        "editorial.EulaPage",
    ]
    is_creatable = False
    show_in_menus_default = False
    search_fields = []

    content_panels = Page.content_panels
    promote_panels = [FieldPanel("slug")]

    STRUCTURAL_PARENT_PATHS = {
        "blog": "/",
        "negocio": "/",
        "eula": "/",
        "outsourcing-bi": "/negocio/",
        "calidad-de-software": "/negocio/",
        "desarrollo-de-software": "/negocio/",
        "gestion-documental": "/negocio/",
    }

    @classmethod
    def can_exist_under(cls, parent):
        return (
            parent.specific_class in (HomePage, RouteContainerPage)
            and super().can_exist_under(parent)
        )

    def clean(self):
        super().clean()
        expected_parent_path = self.STRUCTURAL_PARENT_PATHS.get(self.slug)
        if expected_parent_path is None:
            raise ValidationError({"slug": "La ruta estructural no pertenece al contrato."})
        try:
            parent = self.get_parent()
        except (Page.DoesNotExist, AttributeError):
            parent = None
        if parent is None:
            actual_parent_path = None
        elif parent.specific_class is HomePage:
            actual_parent_path = "/"
        else:
            actual_parent_path = _path_relative_to_home(parent.specific)
        if actual_parent_path != expected_parent_path:
            raise ValidationError({"slug": "El contenedor debe ubicarse en su ruta aprobada."})

    def save(self, *args, **kwargs):
        self.show_in_menus = False
        return super().save(*args, **kwargs)

    def serve(self, request, *args, **kwargs):
        raise Http404

    def get_sitemap_urls(self, request=None):
        return []


class HomePage(Page):
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["editorial.RouteContainerPage"]
    max_count = 1
    hero_copy = models.TextField(blank=True)
    hero_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    sections = StreamField(
        [
            ("service_links", ServiceLinksSectionBlock()),
            ("service_carousel", ServiceCarouselSectionBlock()),
            ("partner", PartnerSectionBlock()),
            ("about", AboutSectionBlock()),
            ("text_section", TextSectionBlock()),
            ("contact_section", ContactSectionBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_copy"),
        FieldPanel("hero_image"),
        FieldPanel("sections"),
    ]

    @classmethod
    def can_exist_under(cls, parent):
        return parent.is_root() and super().can_exist_under(parent)


class BlogIndexPage(Page):
    parent_page_types = ["editorial.RouteContainerPage"]
    subpage_types = ["editorial.BlogPostPage"]
    max_count = 1
    header_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [FieldPanel("header_image")]

    def clean(self):
        super().clean()
        parent = self.get_parent()
        if self.slug != "posts" or _path_relative_to_home(parent.specific) != "/blog/":
            raise ValidationError("BlogIndexPage debe conservar la ruta /blog/posts/.")


class BlogPostPage(Page):
    parent_page_types = ["editorial.BlogIndexPage"]
    subpage_types = []
    summary = models.TextField(blank=True)
    body = StreamField(
        [
            ("rich_text", blocks.RichTextBlock(features=RICH_TEXT_FEATURES)),
            ("image", ArticleImageBlock()),
        ],
        blank=True,
        use_json_field=True,
    )
    lead_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    categories = ParentalManyToManyField(
        "editorial.BlogCategory",
        blank=True,
        related_name="posts",
    )

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
        FieldPanel("body"),
        FieldPanel("lead_image"),
        FieldPanel("categories"),
    ]


class ServicePage(Page):
    parent_page_types = ["editorial.RouteContainerPage"]
    subpage_types = []
    banner_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    description = RichTextField(blank=True, features=RICH_TEXT_FEATURES)
    content_blocks = StreamField(
        [("offering", ServiceOfferingBlock())],
        blank=True,
        use_json_field=True,
    )
    tools = StreamField(
        [("tool", ImageBlock())],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("banner_image"),
        FieldPanel("description"),
        FieldPanel("content_blocks"),
        FieldPanel("tools"),
    ]

    SERVICE_PARENT_PATHS = {
        "business-inteligence": "/negocio/outsourcing-bi/",
        "portafolio-de-servicios-qa": "/negocio/calidad-de-software/",
        "fabrica-de-software": "/negocio/desarrollo-de-software/",
        "gestion-documental": "/negocio/gestion-documental/",
    }

    def clean(self):
        super().clean()
        expected_parent_path = self.SERVICE_PARENT_PATHS.get(self.slug)
        parent = self.get_parent()
        if expected_parent_path is None or _path_relative_to_home(parent.specific) != expected_parent_path:
            raise ValidationError("ServicePage debe usar una de las cuatro rutas del manifiesto.")


class EulaPage(Page):
    parent_page_types = ["editorial.RouteContainerPage"]
    subpage_types = []
    max_count = 1
    legal_body = RichTextField(blank=True, features=RICH_TEXT_FEATURES)

    content_panels = Page.content_panels + [FieldPanel("legal_body")]

    def clean(self):
        super().clean()
        parent = self.get_parent()
        if self.slug != "quickbook" or _path_relative_to_home(parent.specific) != "/eula/":
            raise ValidationError("EulaPage debe conservar la ruta /eula/quickbook/.")


@register_setting
class SiteFooterSettings(BaseSiteSetting):
    address = models.TextField(blank=True)
    phone1 = models.CharField(max_length=80, blank=True)
    phone2 = models.CharField(max_length=80, blank=True)
    email_info = models.EmailField(blank=True)
    social_links = StreamField(
        [
            (
                "social_link",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(max_length=100)),
                        ("image", ImageBlock()),
                        ("url", blocks.URLBlock()),
                    ]
                ),
            )
        ],
        blank=True,
        use_json_field=True,
    )

    panels = [
        FieldPanel("address"),
        FieldPanel("phone1"),
        FieldPanel("phone2"),
        FieldPanel("email_info"),
        FieldPanel("social_links"),
    ]
