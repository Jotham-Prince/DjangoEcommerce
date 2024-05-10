from django.urls import path
from . import views
from . import AdminViews
from . import customerViews, MerchantViews

urlpatterns = [
    
    path('auth', views.index, name= 'index'),
    path("product/<int:product_id>/", customerViews.ProductDetailView.as_view(), name="product_detail"),
    path('b', customerViews.CombinedListView.as_view(), name="combined_list"),
    path('', views.combined_auth_view, name="combined_auth"),
    path('login/', views.login_view, name='login_view'),
    path('logout_process',views.LogoutProcess,name="logout_process"),
    path('register/', views.register, name='register'),
    path('merchant/', views.merchant, name='merchant'),
    path('contact.html/', views.contact_view, name='contact'),
    path('about.html/', views.about, name='about'),
    path('login/contact.html/', views.contact_view, name='contact_html'),
    path('login/about.html/', views.about, name='about'),
    path('login/wishlist.html/', views.wishlist, name='wishlist'),


    path('category.html/', views.category_list, name='category_list'),
    path('blog.html/', views.blog, name='blog'),
    path('shop.html', views.shop, name = 'shop'),
    path('faq.html', views.faq, name='faq'),
    path('wishlist.html', views.wishlist, name='wishlist'),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('biss',views.index1, name = "home2"),
    path('cart', MerchantViews.cart, name = 'cart'),
    path('checkout.html/', views.checkout, name='checkout'),
    path('about.html/blog.html', views.blog, name='about.html/blog.html'),

    # ... other url patterns
    path('add/', views.add_service, name='add_service'),
    path('edit/<int:pk>/', views.edit_service, name='edit_service'),
    path('delete/<int:pk>/', views.delete_service, name='delete_service'),
    path('serve', views.service_list, name='service_list'),
    path('<int:pk>/', views.service_detail, name='service_detail'),
    path('book/<int:service_id>/', views.create_booking, name='create_booking'),
    path('booked-services/', views.booked_services_list, name='booked_services_list'),

]