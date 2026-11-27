from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone

from . import views
from .models import Post


class PostModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="ola", password="unused")

    def test_str_is_title(self):
        post = Post(author=self.author, title="My first post", text="Hello")
        self.assertEqual(str(post), "My first post")

    def test_new_post_is_unpublished(self):
        post = Post.objects.create(author=self.author, title="Draft", text="...")
        self.assertIsNone(post.published_date)
        self.assertLessEqual(
            abs(timezone.now() - post.created_date), timedelta(minutes=1)
        )

    def test_publish_sets_published_date_and_saves(self):
        post = Post.objects.create(author=self.author, title="Draft", text="...")
        before = timezone.now()
        post.publish()
        post.refresh_from_db()
        self.assertIsNotNone(post.published_date)
        self.assertGreaterEqual(post.published_date, before)
        self.assertLessEqual(post.published_date, timezone.now())

    def test_deleting_author_deletes_posts(self):
        Post.objects.create(author=self.author, title="Draft", text="...")
        self.author.delete()
        self.assertFalse(Post.objects.exists())


class PostListViewTests(TestCase):
    def test_root_url_resolves_to_post_list(self):
        match = resolve("/")
        self.assertEqual(match.func, views.post_list)
        self.assertEqual(reverse("post_list"), "/")

    def test_post_list_renders_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_list.html")
        self.assertContains(response, "<title>Django Girls blog</title>", html=True)
        self.assertContains(response, "My first post")
        self.assertContains(response, "My second post")

    def test_unknown_url_is_404(self):
        response = self.client.get("/no-such-page/")
        self.assertEqual(response.status_code, 404)


class AdminTests(TestCase):
    def test_admin_requires_login(self):
        response = self.client.get("/admin/")
        self.assertRedirects(response, "/admin/login/?next=/admin/")

    def test_admin_lists_posts_for_superuser(self):
        admin = User.objects.create_superuser("admin", "admin@example.com", "pw")
        Post.objects.create(author=admin, title="Admin visible post", text="...")
        self.client.force_login(admin)
        response = self.client.get(reverse("admin:blog_post_changelist"))
        self.assertContains(response, "Admin visible post")
