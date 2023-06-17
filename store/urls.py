from django.urls import path

from . import views

urlpatterns = [
    # поиск
    path("search/", views.search, name="search"),
    # добавление в корзину
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # изменения количества
    path('change_quantity/<str:product_id>/', views.change_quantity, name='change_quantity'),
    # удаление из корзины
    path('remove-from-cart/<str:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    # обзор корзины
    path('cart/', views.cart_view, name='cart_view'),
    # проверка
    path('cart/checkout/', views.checkout, name='checkout'),
    # оплата
    path('cart/success/', views.success, name='success'),
    # категории
    path("<slug:slug>/", views.category_detail, name="category_detail"),
    # товар
    path('<slug:category_slug>/<slug:slug>/', views.product_detail, name='product_detail'),
]
