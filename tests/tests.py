from django.test import TestCase,SimpleTestCase
from django.test.client import Client

# Method HTTP GET.
class SimpleTestRead(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_my_view(self):
        response = self.client.get('/my-url/')
        self.assertEqual(response.status_code,200)

# Method HTTP POST.
class SimpleTestCreate(SimpleTestCase):
    def test_create_data(self):
        data = {}
        response = self.client.post('/my-url/',data)
        self.assertEqual(response.status_code,201)

# Method HTTP PUT/PATCH.
class SimpleTestUpdate(SimpleTestCase):
    # PUT
    def test_update_data(self):
        data = {}
        response = self.client.put('/my-url/1/',data)
        self.assertEqual(response.status_code,200)

    # PATCH
    def test_update_partial_update_data(self):
        data = {}
        response = self.client.patch('/my-url/1/',data)
        self.assertEqual(response.status_code,200)

# Method HTTP DELETE.
class SimpleTestDelete(SimpleTestCase):
    def test_delete_data(self):
        response = self.client.delete('/my-url/1/')
        self.assertEqual(response.status_code,204)