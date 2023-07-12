from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='api_dataset_upload'),
    path('list/', FileListView.as_view(), name='api_dataset_list'),
    path('read/', FileReadView.as_view(), name='api_dataset_read'),
    path('delete/<int:file_id>/', FileDeleteView.as_view(), name='api_dataset_delete'),
    path('generate_token/', GenerateTokenView.as_view(), name='api_generate_token'),
    path('revoke_token/', RevokeTokenView.as_view(), name='api_revoke_token')
]
