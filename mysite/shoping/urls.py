from django.urls import path, include


from . import views
from .views import MyShoppingCartDetailView, search_price_view, search_price

urlpatterns = [
    path('', views.index, name='index'),
    path('resume/', views.resume, name='resume'),
    path('projects/', views.projects, name='projects'),
    # path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path("profile/", views.profile, name="profile"),
    path('search_price/', views.search_price, name='search_price'),
    path("myshoppingcart/", views.MyShoppingCartListView.as_view(), name="my_shopping_cart"),
    path("myshoppingcart/<int:pk>", views.MyShoppingCartDetailView.as_view(), name="my_shopping_cart_detail"),
    path('myshoppingcart/new', views.MyShoppingCartCreateView.as_view(), name='cart_new'),
    path('myshoppingcart/<int:pk>/update', views.MyShoppingCartUpdateView.as_view(), name='cart_update'),
    path('myshoppingcart/<int:pk>/delete', views.MyShoppingCartDeleteView.as_view(), name='cart_delete'),
    path('myshoppingcart/<int:cart_id>/newproduct', views.MyProductCreatView.as_view(), name='product_new'),
    path('cart/<int:pk>/', MyShoppingCartDetailView.as_view(), name='cart_detail'),
    path('cart/<int:cart_id>/search_price/', search_price_view, name='search_price'),
    path("myproduct/<int:pk>/delete", views.MyProductDeleteView.as_view(), name="product_delete"),
    path('contact/', views.contact_view, name='contact'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]