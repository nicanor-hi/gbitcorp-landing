import csv
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image as PillowImage
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client, RequestFactory, TestCase, override_settings
from django.urls import reverse
from wagtail.contrib.settings.registry import registry as settings_registry
from wagtail.models import Page, Site
from wagtail.images import get_image_model
from wagtail.snippets.models import get_snippet_models

from editorial.models import (
    BlogCategory,
    BlogIndexPage,
    BlogPostPage,
    EulaPage,
    HomePage,
    RouteContainerPage,
    ServicePage,
    SiteFooterSettings,
)


class EditorialModelTests(TestCase):
    def test_models_are_registered_without_seeded_content(self):
        self.assertEqual(HomePage.objects.count(), 0)
        self.assertEqual(BlogIndexPage.objects.count(), 0)
        self.assertEqual(BlogPostPage.objects.count(), 0)
        self.assertEqual(ServicePage.objects.count(), 0)
        self.assertEqual(EulaPage.objects.count(), 0)
        self.assertEqual(RouteContainerPage.objects.count(), 0)
        self.assertEqual(BlogCategory.objects.count(), 0)
        self.assertEqual(
            {model.__name__ for model in (HomePage, BlogIndexPage, BlogPostPage, ServicePage, EulaPage)},
            {"HomePage", "BlogIndexPage", "BlogPostPage", "ServicePage", "EulaPage"},
        )
        self.assertIn(BlogCategory, get_snippet_models())
        self.assertIn(SiteFooterSettings, settings_registry)
        for model in (
            HomePage,
            BlogIndexPage,
            BlogPostPage,
            ServicePage,
            EulaPage,
            RouteContainerPage,
        ):
            self.assertTrue(model.get_edit_handler().children)

    def test_wagtail_page_type_rules(self):
        root = Page.get_first_root_node()

        self.assertTrue(HomePage.can_exist_under(root))
        home = root.add_child(
            instance=HomePage(title="Temporary home", slug="test-home", live=True)
        )
        self.assertFalse(HomePage.can_exist_under(home))
        blog = home.add_child(
            instance=RouteContainerPage(title="Blog route", slug="blog", live=True)
        )
        index = blog.add_child(
            instance=BlogIndexPage(title="Blog index", slug="posts", live=True)
        )

        self.assertTrue(RouteContainerPage.can_exist_under(home))
        self.assertFalse(RouteContainerPage.can_create_at(home))
        self.assertFalse(RouteContainerPage.is_creatable)
        self.assertFalse(RouteContainerPage.can_exist_under(index))
        self.assertTrue(BlogPostPage.can_exist_under(index))
        self.assertFalse(BlogPostPage.can_exist_under(home))
        self.assertFalse(ServicePage.can_exist_under(root))
        self.assertFalse(HomePage.can_create_at(root))
        self.assertFalse(BlogIndexPage.can_create_at(blog))

    def test_service_page_rejects_a_structural_parent_outside_its_route(self):
        root = Page.get_first_root_node()
        home = root.add_child(
            instance=HomePage(title="Temporary home", slug="test-home", live=True)
        )
        blog = home.add_child(
            instance=RouteContainerPage(title="Blog route", slug="blog", live=True)
        )

        with self.assertRaises(ValidationError):
            blog.add_child(
                instance=ServicePage(
                    title="Temporary service",
                    slug="business-inteligence",
                    live=True,
                )
            )

    def test_category_slug_and_name_are_unique(self):
        first = BlogCategory(name="Category A", slug="category-a")
        first.full_clean()
        first.save()

        duplicate_slug = BlogCategory(name="Category B", slug="category-a")
        with self.assertRaises(ValidationError):
            duplicate_slug.full_clean()

        duplicate_name = BlogCategory(name="category a", slug="category-a-2")
        with self.assertRaises(ValidationError):
            duplicate_name.full_clean()

        invalid_slug = BlogCategory(name="Category C", slug="Category C")
        with self.assertRaises(ValidationError):
            invalid_slug.full_clean()

    def test_article_can_have_multiple_categories(self):
        root = Page.get_first_root_node()
        home = root.add_child(
            instance=HomePage(title="Temporary home", slug="test-home", live=True)
        )
        blog_container = home.add_child(
            instance=RouteContainerPage(title="Blog route", slug="blog", live=True)
        )
        index = blog_container.add_child(
            instance=BlogIndexPage(title="Blog index", slug="posts", live=True)
        )
        article = index.add_child(
            instance=BlogPostPage(title="Temporary post", slug="temporary-post", live=True)
        )
        category_a = BlogCategory.objects.create(name="Category A", slug="category-a")
        category_b = BlogCategory.objects.create(name="Category B", slug="category-b")

        article.categories.add(category_a, category_b)
        article.categories.add(category_a)
        article.save_revision().publish()
        article = BlogPostPage.objects.get(pk=article.pk)

        self.assertEqual(article.categories.count(), 2)
        self.assertEqual(article.categories.distinct().count(), 2)

        category_a.delete()
        article = BlogPostPage.objects.get(pk=article.pk)
        self.assertEqual(article.categories.count(), 1)

    def test_wagtail_image_reference_and_streamfield_round_trip(self):
        image_model = get_image_model()
        root = Page.get_first_root_node()
        home = root.add_child(
            instance=HomePage(title="Image fixture", slug="test-home", live=True)
        )
        self.assertIsNone(home.hero_image_id)
        blog = home.add_child(
            instance=RouteContainerPage(title="Blog route", slug="blog", live=True)
        )
        index = blog.add_child(
            instance=BlogIndexPage(title="Blog index", slug="posts", live=True)
        )
        article = index.add_child(
            instance=BlogPostPage(title="Image article", slug="image-article", live=True)
        )

        buffer = BytesIO()
        PillowImage.new("RGB", (2, 2), color=(255, 255, 255)).save(buffer, format="PNG")
        with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            image = image_model(
                title="Temporary test image",
                file=ContentFile(buffer.getvalue(), name="temporary-test-image.png"),
            )
            image.save()
            home.hero_image = image
            home.save()
            home.refresh_from_db()
            self.assertEqual(home.hero_image_id, image.pk)

            article.lead_image = image
            article.save()

            article_field = BlogPostPage._meta.get_field("body")
            image_block = article_field.stream_block.child_blocks["image"]
            valid_image_value = image_block.to_python(
                {
                    "image": image.pk,
                    "decorative": False,
                    "alt_text": "Diagrama explicativo",
                    "caption": "Leyenda opcional",
                    "alignment": "left",
                }
            )
            image_block.clean(valid_image_value)

            with self.assertRaises(ValidationError):
                image_block.clean(
                    image_block.to_python(
                        {
                            "image": None,
                            "decorative": True,
                            "alt_text": "",
                            "caption": "",
                            "alignment": "",
                        }
                    )
                )
            with self.assertRaises(ValidationError):
                image_block.clean(
                    image_block.to_python(
                        {
                            "image": image.pk,
                            "decorative": False,
                            "alt_text": "   ",
                            "caption": "",
                            "alignment": "",
                        }
                    )
                )
            with self.assertRaises(ValidationError):
                image_block.clean(
                    image_block.to_python(
                        {
                            "image": image.pk,
                            "decorative": True,
                            "alt_text": "",
                            "caption": "",
                            "alignment": "center",
                        }
                    )
                )

            decorative_image = image_block.to_python(
                {
                    "image": image.pk,
                    "decorative": True,
                    "alt_text": "",
                    "caption": "",
                    "alignment": "right",
                }
            )
            image_block.clean(decorative_image)

            stream_value = article_field.to_python(
                [
                    {
                        "type": "image",
                        "value": {
                            "image": image.pk,
                            "decorative": False,
                            "alt_text": "Diagrama explicativo",
                            "caption": "Leyenda opcional",
                            "alignment": "left",
                        },
                    }
                ]
            )
            self.assertEqual(stream_value[0].value["image"].pk, image.pk)
            prepared = article_field.get_prep_value(stream_value)
            self.assertEqual(prepared[0]["value"]["image"], image.pk)
            restored = article_field.to_python(prepared)
            self.assertEqual(restored[0].block_type, "image")
            self.assertEqual(restored[0].value["image"].pk, image.pk)
            self.assertEqual(restored[0].value["alt_text"], "Diagrama explicativo")
            self.assertEqual(restored[0].value["caption"], "Leyenda opcional")
            self.assertEqual(restored[0].value["alignment"], "left")

            service_field = ServicePage._meta.get_field("tools")
            service_block = service_field.stream_block.child_blocks["tool"]
            with self.assertRaises(ValidationError):
                service_block.clean(
                    service_block.to_python(
                        {"image": image.pk, "decorative": False, "alt_text": ""}
                    )
                )
            service_value = service_field.to_python(
                [
                    {
                        "type": "tool",
                        "value": {
                            "image": image.pk,
                            "decorative": True,
                            "alt_text": "",
                        },
                    }
                ]
            )
            self.assertEqual(service_value[0].value.pk, image.pk)
            service_restored = service_field.to_python(service_field.get_prep_value(service_value))
            self.assertEqual(service_restored[0].block_type, "tool")
            self.assertEqual(service_restored[0].value.pk, image.pk)

            image.delete()
            article.refresh_from_db()
            self.assertIsNone(article.lead_image_id)

    def test_wagtail_admin_exposes_page_snippet_and_site_settings_editors(self):
        root = Page.get_first_root_node()
        home = root.add_child(
            instance=HomePage(title="Admin fixture", slug="test-home", live=True)
        )
        blog = home.add_child(
            instance=RouteContainerPage(title="Blog route", slug="blog", live=True)
        )
        index = blog.add_child(
            instance=BlogIndexPage(title="Blog index", slug="posts", live=True)
        )
        article = index.add_child(
            instance=BlogPostPage(title="Admin article", slug="admin-article", live=True)
        )
        category = BlogCategory.objects.create(name="Admin category", slug="admin-category")
        article.categories.add(category)

        user = get_user_model().objects.create_superuser(
            username="temporary-admin",
            email="temporary-admin@example.invalid",
            password=None,
        )
        client = Client()

        snippet_list_url = reverse("wagtailsnippets_editorial_blogcategory:list")
        site = Site.objects.get(is_default_site=True)
        settings_edit_url = reverse(
            "wagtailsettings:edit",
            args=("editorial", "sitefootersettings", site.pk),
        )
        page_edit_url = reverse("wagtailadmin_pages:edit", args=(article.pk,))
        home_edit_url = reverse("wagtailadmin_pages:edit", args=(home.pk,))

        self.assertEqual(client.get(snippet_list_url).status_code, 302)
        self.assertEqual(client.get(settings_edit_url).status_code, 302)
        self.assertEqual(client.get(page_edit_url).status_code, 302)

        client.force_login(user)
        self.assertEqual(client.get(reverse("wagtailadmin_home")).status_code, 200)
        self.assertEqual(client.get(snippet_list_url).status_code, 200)

        settings_response = client.get(settings_edit_url)
        self.assertEqual(settings_response.status_code, 200)
        for field_name in ("address", "phone1", "phone2", "email_info", "social_links"):
            self.assertContains(settings_response, field_name)

        page_response = client.get(page_edit_url)
        self.assertEqual(page_response.status_code, 200)
        self.assertContains(page_response, "Admin category")

        home_response = client.get(home_edit_url)
        self.assertEqual(home_response.status_code, 200)
        self.assertContains(home_response, "hero_image")

    def test_exact_manifest_routes_and_structural_404s(self):
        root = Page.get_first_root_node()
        home = root.add_child(
            instance=HomePage(title="Temporary home", slug="test-home", live=True)
        )
        blog_container = home.add_child(
            instance=RouteContainerPage(title="Blog route", slug="blog", live=True)
        )
        index = blog_container.add_child(
            instance=BlogIndexPage(title="Blog index", slug="posts", live=True)
        )
        article = index.add_child(
            instance=BlogPostPage(title="Temporary post", slug="temporary-post", live=True)
        )

        business = home.add_child(
            instance=RouteContainerPage(title="Business route", slug="negocio", live=True)
        )
        service_parent = business.add_child(
            instance=RouteContainerPage(
                title="Business intelligence route", slug="outsourcing-bi", live=True
            )
        )
        service = service_parent.add_child(
            instance=ServicePage(
                title="Temporary service",
                slug="business-inteligence",
                live=True,
            )
        )

        legal = home.add_child(
            instance=RouteContainerPage(title="Legal route", slug="eula", live=True)
        )
        eula = legal.add_child(
            instance=EulaPage(title="Temporary legal page", slug="quickbook", live=True)
        )

        site = Site.objects.get(is_default_site=True)
        site.hostname = "testserver"
        site.port = 80
        site.root_page = home
        site.save()

        request = RequestFactory().get("/blog/posts/temporary-post/")
        resolved = Page.route_for_request(request, "/blog/posts/temporary-post/")
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved.page.specific_class, BlogPostPage)
        self.assertEqual(article.url_path.removeprefix(home.url_path), "blog/posts/temporary-post/")

        request = RequestFactory().get("/negocio/outsourcing-bi/business-inteligence/")
        resolved = Page.route_for_request(
            request,
            "/negocio/outsourcing-bi/business-inteligence/",
        )
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved.page.specific_class, ServicePage)
        self.assertEqual(
            service.url_path.removeprefix(home.url_path),
            "negocio/outsourcing-bi/business-inteligence/",
        )

        request = RequestFactory().get("/eula/quickbook/")
        resolved = Page.route_for_request(request, "/eula/quickbook/")
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved.page.specific_class, EulaPage)
        self.assertEqual(eula.url_path.removeprefix(home.url_path), "eula/quickbook/")

        client = Client()
        for route in ("/blog/", "/negocio/", "/negocio/outsourcing-bi/", "/eula/"):
            with self.subTest(route=route):
                self.assertEqual(client.get(route).status_code, 404)

        for container in (blog_container, business, service_parent, legal):
            self.assertFalse(container.show_in_menus)
            self.assertEqual(container.get_sitemap_urls(), [])

    def test_all_49_preserved_paths_resolve_to_their_editorial_types(self):
        manifest_path = (
            Path(__file__).resolve().parents[2]
            / "docs"
            / "21_MANIFIESTO_CONTENIDO_VIGENTE.csv"
        )
        with manifest_path.open(encoding="utf-8", newline="") as manifest_file:
            routes = [
                {"path": row["path"], "template": row["processwire_template"]}
                for row in csv.DictReader(manifest_file)
            ]

        public_paths = {row["path"] for row in routes}
        self.assertEqual(len(routes), 49)
        self.assertEqual(len(public_paths), 49)
        self.assertEqual(sum(row["template"] == "home" for row in routes), 1)

        root = Page.get_first_root_node()
        home = root.add_child(
            instance=HomePage(title="Route fixture", slug="test-home", live=True)
        )
        pages_by_path = {"/": home}
        site = Site.objects.get(is_default_site=True)
        site.hostname = "testserver"
        site.port = 80
        site.root_page = home
        site.save()

        route_types = {
            "blog-posts": BlogIndexPage,
            "blog-post": BlogPostPage,
            "service_service": ServicePage,
            "eula": EulaPage,
        }
        prefixes = set()
        for path in public_paths - {"/"}:
            parts = [part for part in path.strip("/").split("/") if part]
            for length in range(1, len(parts)):
                prefixes.add("/" + "/".join(parts[:length]) + "/")

        all_paths = sorted(
            (public_paths - {"/"}) | prefixes,
            key=lambda path: (path.count("/"), path),
        )
        structural_paths = prefixes - public_paths
        self.assertEqual(len(structural_paths), 7)
        template_by_path = {row["path"]: row["template"] for row in routes}
        for path in all_paths:
            parts = [part for part in path.strip("/").split("/") if part]
            parent_path = "/" + "/".join(parts[:-1]) + "/" if len(parts) > 1 else "/"
            parent = pages_by_path[parent_path]
            page_model = route_types.get(template_by_path.get(path), RouteContainerPage)
            page = parent.add_child(
                instance=page_model(
                    title="Route fixture",
                    slug=parts[-1],
                    live=True,
                )
            )
            pages_by_path[path] = page

        self.assertEqual(set(pages_by_path), public_paths | structural_paths)
        self.assertEqual(len(pages_by_path), 56)

        for path, template in ((row["path"], row["template"]) for row in routes):
            with self.subTest(path=path):
                result = Page.route_for_request(RequestFactory().get(path), path)
                self.assertIsNotNone(result)
                expected_model = HomePage if template == "home" else route_types[template]
                self.assertIs(result.page.specific_class, expected_model)
                self.assertIs(pages_by_path[path].specific_class, expected_model)

        client = Client()
        for path in prefixes - public_paths:
            with self.subTest(structural_path=path):
                container = pages_by_path[path].specific
                self.assertEqual(client.get(path).status_code, 404)
                self.assertFalse(container.show_in_menus)
                self.assertEqual(container.get_sitemap_urls(), [])
                self.assertEqual(container.search_fields, [])
