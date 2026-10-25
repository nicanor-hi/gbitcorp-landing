from django.conf import settings
from django.test import SimpleTestCase
from django.urls import resolve


class ProjectSetupTests(SimpleTestCase):
    def test_default_database_backend_is_postgresql(self):
        self.assertEqual(
            settings.DATABASES["default"]["ENGINE"],
            "django.db.backends.postgresql",
        )

    def test_wagtail_admin_login_route_is_configured(self):
        match = resolve("/admin/login/")
        self.assertTrue(match.url_name)
