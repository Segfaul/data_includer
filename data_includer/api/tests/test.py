from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch

from table.models import *


class APITokenTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_pass')

    def test_generate_token_logout(self):
        response = self.client.get(reverse('api_generate_token'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_generate_token_login(self):
        self.client.login(username='test_user', password='test_pass')

        response = self.client.get(reverse('api_generate_token'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('api_token', response.data)
        self.assertIsNotNone(response.data['api_token'])

        self.user.refresh_from_db()
        self.assertEqual(self.user.api_token, response.data['api_token'])

    def test_revoke_token_logout(self):
        response = self.client.get(reverse('api_revoke_token'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_revoke_token_login(self):
        self.user.api_token = 'test_token'
        self.user.save()

        self.client.login(username='test_user', password='test_pass')

        response = self.client.get(reverse('api_revoke_token'))
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.api_token, None)

    def test_revoke_token_without_token(self):
        self.client.login(username='test_user', password='test_pass')

        response = self.client.get(reverse('api_revoke_token'))
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.api_token, None)


class APIFileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_pass')
        self.user.api_token = 'test_token'
        self.user.save()

    def test_file_upload_correct_token(self):

        file = SimpleUploadedFile("data.csv", b"file_content", content_type="text/csv")

        files = {'file': (file.name, file, 'text/csv')}
        headers = {'Content-Disposition': f'attachment; filename="{file.name}"', 'Content-Type': 'text/csv'}

        response = self.client.post(reverse('api_dataset_upload') + '?api_token=' + self.user.api_token,
                                    data=files, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.user.refresh_from_db()
        self.assertIsNotNone(Dataset.objects.filter(user=self.user.pk).first().file.name.split('/')[-1])

    def test_file_upload_incorrect_token(self):
        file = SimpleUploadedFile("data.csv", b"file_content", content_type="text/csv")

        files = {'file': (file.name, file, 'text/csv')}
        headers = {'Content-Disposition': f'attachment; filename="{file.name}"', 'Content-Type': 'text/csv'}

        response = self.client.post(reverse('api_dataset_upload') + '?api_token=' + '123',
                                    data=files, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_file_list(self):
        response = self.client.get(reverse('api_dataset_list') + '?api_token=' + self.user.api_token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_file_delete(self):
        file = SimpleUploadedFile("data.csv", b"file_content", content_type="text/csv")

        files = {'file': (file.name, file, 'text/csv')}
        headers = {'Content-Disposition': f'attachment; filename="{file.name}"', 'Content-Type': 'text/csv'}

        response = self.client.post(reverse('api_dataset_upload') + '?api_token=' + self.user.api_token,
                                    data=files, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(reverse('api_dataset_delete',
                                              args=[Dataset.objects.filter(user=self.user.pk).first().pk])
                                      + '?api_token=' + self.user.api_token)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_file_delete_without(self):

        response = self.client.delete(reverse('api_dataset_delete', args=[1])
                                      + '?api_token=' + self.user.api_token)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
