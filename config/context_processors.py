"""Read-only context for the public site shell."""

from wagtail.models import Site

from editorial.models import SiteFooterSettings


PUBLIC_NAVIGATION = (
    ("Inicio", "/#inicio"),
    ("Líneas de negocio", "/#lineas-negocio"),
    ("Servicios", "/#servicios"),
    ("Partner-Zoho", "/#partner-zoho"),
    ("Nosotros", "/#nosotros"),
    ("Nuestra esencia", "/#clientes"),
    ("Blog", "/#blog"),
    ("Contacto", "/#contact"),
)

FOOTER_LINKS = (
    ("Inicio", "/#inicio"),
    ("Líneas de negocio", "/#lineas-negocio"),
    ("Servicios", "/#servicios"),
    ("Partner-Zoho", "/#partner-zoho"),
    ("Nosotros", "/#nosotros"),
    ("Nuestra esencia", "/#clientes"),
    ("Blog", "/#blog"),
    ("Contacto", "/#contact"),
    ("Únetenos", "https://vacantes.gbitcorp.com/jobs/Careers"),
    ("Legal", "/eula/quickbook/"),
)


def public_site_shell(request):
    """Expose verified navigation and existing footer settings without writes."""
    site = Site.find_for_request(request)
    footer = None
    if site is not None:
        footer = SiteFooterSettings.objects.filter(site_id=site.pk).first()

    return {
        "public_navigation": PUBLIC_NAVIGATION,
        "footer_links": FOOTER_LINKS,
        "site_footer": footer,
    }
