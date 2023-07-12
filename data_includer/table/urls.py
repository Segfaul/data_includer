from django.urls import path
from .views import *

urlpatterns = [
    path('', IntroView.as_view(), name='intro'),
    path('datasets/', DatasetListView.as_view(), name='dataset_list'),
    path('datasets/search/', DatasetSearchView.as_view(), name='dataset_search'),

    path('datasets/create/', DatasetCreateView.as_view(), name='dataset_add'),
    path('datasets/<int:dataset_id>/', DatasetDetailView.as_view(), name='dataset'),
    path('datasets/<int:pk>/update/', DatasetUpdateView.as_view(), name='dataset_update'),
    path('datasets/<int:pk>/delete/', DatasetDeleteView.as_view(), name='dataset_delete'),

    path('users/<int:user_id>/', UserDetailView.as_view(), name='user_profile'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),

]