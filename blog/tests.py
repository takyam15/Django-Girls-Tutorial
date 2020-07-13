import factory
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Post


# Create your tests here.

class AuthorFactory(factory.django.DjangoModelFactory):
    """Create data for the Author model used for the tests"""
    username = 'root'
    email = 'root@example.com'
    password = 'password'

    class Meta:
        model = Author
        django_get_or_create = ('username',)


class PostFactory(factory.django.DjangoModelFactory):
    """Create data for the Post model used for the tests"""
    author = factory.SubFactory(AuthorFactory)
    title = 'Example post'
    slug = 'example-post'
    text = 'This is an example text.'
    published_date = timezone.now()

    class Meta:
        model = Post


# Tests for the models



# Tests for the forms



# Tests for the views

class PostListTests(TestCase):

    def test_get_post_list(self):
        post_1 = PostFactory(
            title='First post',
            slug='first-post'
        )
        post_2 = PostFactory(
            title='Second post',
            slug='second-post'
        )
        res = self.client.get(reverse('blog:post_list'))
        self.assertTemplateUsed(res, 'blog/post_list.html')
        self.assertQuerysetEqual(
            res.context['post_list'],
            ['<Post: First post>', '<Post: Second post>']
        )

    def test_get_empty_post_list(self):
        res = self.client.get(reverse('blog:post_list'))
        self.assertTemplateUsed(res, 'blog/post_list.html')
        self.assertQuerysetEqual(res.context['post_list'], [])
        self.assertContains(res, 'No posts are displayed.')


class PostDetailTests(TestCase):

    def test_get_post_detail(self):
        post = PostFactory(
            title='Sample post',
            slug='sample-post',
        )
        res = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'sample-post'}))
        self.assertTemplateUsed(res, 'blog/post_detail.html')
        self.assertEqual(res.context['post'].title, 'Sample post')

    def test_get_non_existent_post(self):
        res = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'non_existent'}))
        self.assertEqual(res.status_code, 404)


class PostCreateTests(TestCase):

    def setUp(self):
        self.author = AuthorFactory()
        self.client.force_login(self.author)

    def test_get_create_form(self):
        res = self.client.get(reverse('blog:post_new'))
        self.assertTemplateUsed(res, 'blog/post_edit.html')

    def test_create_new_post(self):
        new_post = {
            'title': 'New post',
            'slug': 'new-post',
            'text': 'This is a new post.'
        }
        res = self.client.post(reverse('blog:post_new'), data=new_post)
        self.assertRedirects(res, reverse('blog:post_list'))
        self.assertEqual(Post.objects.count(), 1)


class PostUpdateTests(TestCase):

    def setUp(self):
        self.author = AuthorFactory()
        self.client.force_login(self.author)

    def test_get_update_form(self):
        post = PostFactory(slug='sample-post')
        res = self.client.get(reverse('blog:post_edit', kwargs={'slug': 'sample-post'}))
        self.assertTemplateUsed(res, 'blog/post_edit.html')

    def test_get_non_existent_post_form(self):
        res = self.client.get(reverse('blog:post_edit', kwargs={'slug': 'non-existent'}))
        self.assertEqual(res.status_code, 404)

    def test_update_post(self):
        post = PostFactory(
            title='Sample post',
            slug='sample-post',
            text='This is the original text.'
        )
        updated_post = {
            'title': 'Sample post',
            'slug': 'sample-post',
            'text': 'This text has been updated.'
        }
        res = self.client.post(reverse('blog:post_edit', kwargs={'slug': 'sample-post'}), data=updated_post)
        self.assertRedirects(res, reverse('blog:post_list'))
        post.refresh_from_db()
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.text, 'This text has been updated.')

    def test_update_non_existent_post(self):
        res = self.client.post(reverse('blog:post_edit', kwargs={'slug': 'non-existent'}))
        self.assertEqual(res.status_code, 404)


class PostDeleteTests(TestCase):

    def setUp(self):
        self.author = AuthorFactory()
        self.client.force_login(self.author)

    def test_delete_post(self):
        pass

    def test_delete_non_existent_post(self):
        pass
