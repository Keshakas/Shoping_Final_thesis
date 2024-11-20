from django.urls import path, include


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('resume/', views.resume, name='resume'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path("profile/", views.profile, name="profile"),
    path('search_price/', views.search_price, name='search_price'),
    path('search_pricee/', views.search_price_view, name='search_pricee'),
    path("myshoppingcart/", views.MyShoppingCartListView.as_view(), name="my_shopping_cart"),
    path("myshoppingcart/<int:pk>", views.MyShoppingCartDetailView.as_view(), name="my_shopping_cart_detail"),
    path('myshoppingcart/new', views.MyShoppingCartCreateView.as_view(), name='cart_new'),
    path('myshoppingcart/<int:pk>/update', views.MyShoppingCartUpdateView.as_view(), name='cart_update'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]