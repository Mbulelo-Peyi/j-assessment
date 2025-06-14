from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

class SplitSortStringViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('word')

    def test_split_and_sort_valid_data(self):
        data = {"data": "zebra apple banana"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"word": [' ',' ','a','a','a','a','a','b','b','e','e','l','n','n','p','p','r','z']})

    def test_missing_data_field(self):
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Missing 'data' field.")

    def test_empty_string_data(self):
        data = {"data": ""}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Missing 'data' field.")
