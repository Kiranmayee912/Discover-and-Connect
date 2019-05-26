from django.urls import path
from .views import (
    UploadDetailView,
    UploadCreateView,
    UploadUpdateView,
    UploadDeleteView

)
from . import views
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='upload'),
    path('about/', views.about, name='blog-about'),
    path('search/',views.search,name='blog-search'),
    #path('upload/',views.uploadlist,name='upload'),
    path('upload/<int:pk>/', UploadDetailView.as_view(), name='upload-detail'),
    path('upload/new/', UploadCreateView.as_view(), name='upload-create'),
    path('upload/<int:pk>/update/', UploadUpdateView.as_view(), name='upload-update'),
    path('upload/<int:pk>/delete/', UploadDeleteView.as_view(), name='upload-delete'),
    path('timeline/<int:pk>',views.timeline,name='timeline') 
]