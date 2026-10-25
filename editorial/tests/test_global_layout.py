from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase
from wagtail.models import Page, Site

from config.context_processors import FOOTER_LINKS, PUBLIC_NAVIGATION
from editorial.models import SiteFooterSettings


class GlobalLayoutTests(TestCase):
    def setUp(self):
        root = Page.get_first_root_node()
        self.site = Site.objects.create(
            hostname="layout.test",
            port=80,
            root_page=root,
        )
        self.request = RequestFactory().get("/", HTTP_HOST=self.site.hostname)

    def render_shell(self):
        return render_to_string("base.html", {}, request=self.request)

    def test_base_renders_shared_landmarks_and_static_assets(self):
        html = self.render_shell()

        self.assertIn('<html lang="es">', html)
        self.assertIn('href="/static/css/site.css"', html)
        self.assertIn('src="/static/js/site-navigation.js"', html)
        self.assertIn('id="main-content"', html)
        self.assertIn('aria-label="Navegación principal"', html)
        self.assertIn('aria-label="Navegación móvil"', html)
        self.assertIn('src="/static/images/brand/logo-gbit.png"', html)
        self.assertIn("Saltar al contenido", html)

    def test_verified_navigation_does_not_link_to_structural_404_paths(self):
        html = self.render_shell()

        for _, href in (*PUBLIC_NAVIGATION, *FOOTER_LINKS):
            self.assertNotIn(href, {"/blog/", "/negocio/", "/eula/"})
        self.assertNotIn('href="/blog/"', html)
        self.assertNotIn('href="/negocio/"', html)
        self.assertNotIn('href="/eula/"', html)
        self.assertIn('href="/eula/quickbook/"', html)

    def test_empty_footer_settings_are_safe_and_do_not_create_records(self):
        self.assertEqual(SiteFooterSettings.objects.count(), 0)

        html = self.render_shell()

        self.assertIn("Contáctenos", html)
        self.assertIn("Estamos para servirte", html)
        self.assertIn("Redes Sociales", html)
        self.assertNotIn("tel:", html)
        self.assertNotIn("mailto:", html)
        self.assertEqual(SiteFooterSettings.objects.count(), 0)

    def test_footer_renders_only_values_configured_in_wagtail_settings(self):
        SiteFooterSettings.objects.create(
            site=self.site,
            address="Dirección de prueba",
            phone1="+507 200-0000",
            email_info="info@example.test",
        )

        html = self.render_shell()

        self.assertIn("Dirección de prueba", html)
        self.assertIn('href="tel:+507 200-0000"', html)
        self.assertIn('href="mailto:info@example.test"', html)
        self.assertNotIn("tel:+507 200-0001", html)
