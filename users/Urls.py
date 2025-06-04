from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserListView.as_view(), name='user-list'),
    path('create/', views.UserCreateView.as_view(), name='user-create'),
    path('<uuid:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('<uuid:pk>/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('<uuid:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
]