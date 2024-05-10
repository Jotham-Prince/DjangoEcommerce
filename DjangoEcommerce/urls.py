from django.contrib import admin
from django.urls import path, include
from DjangoEcommerceApp import views
from django.conf import settings
# from DjangoEcommerceApp import AdminViews
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', views.adminLogin,name="admin_login"),
    path('',include("DjangoEcommerceApp.urls")), 
    path('',include("DjangoEcommerceApp.adminurls"))
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
