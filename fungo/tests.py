from django.core.urlresolvers import reverse
from django.test import TestCase
from fungo.models import Category

from fungo.models import Category

class CategoryMethodTests(TestCase):

    def test_ensure_views_are_positive(self):
        """
        This should return true for categories where views are not negative.
        """
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """
        Check that we add appropriate slug to newly created category.
        """
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

class IndexViewTests(TestCase):

    def test_index_view_with_no_categories(self):
        """
        If no categories exist, an appropriate message should be displayed.
        """
        # First of all, Django's ‘TestCase’ has access to client object,
        # which can make requests.
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        """
        If some categories exist, they should be displayed.
        """
        add_cat('test', 1, 1)
        add_cat('temp', 1, 1)
        add_cat('tmp', 1, 1)
        add_cat('tmp test temp', 1, 1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")
        self.assertEqual(len(response.context['categories']), 4)
