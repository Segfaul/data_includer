from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Dataset(models.Model):
    file = models.FileField(upload_to='uploaded_files/%Y/%m/%d/', verbose_name='File')
    description = models.TextField(blank=True, verbose_name="Description")

    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Upload date")
    modified_date = models.DateTimeField(auto_now_add=True, verbose_name="Modified date")

    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='User')

    def __str__(self):
        return self.file.name.split('/')[-1]

    def get_absolute_url(self):
        return reverse('dataset', kwargs={'dataset_id': self.pk})

    class Meta:
        verbose_name = 'Dataset'
        verbose_name_plural = 'Datasets'
        ordering = ['-modified_date']


class User(AbstractUser):
    api_token = models.CharField(max_length=255, null=True, blank=True, verbose_name='API-token')
