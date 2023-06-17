from django.contrib.auth import views as auth_view
from django.urls import path

from . import views

urlpatterns = [
    # регистрация
    path("signup/", views.signup, name="signup"),
    # вход
    path("login/", auth_view.LoginView.as_view(template_name='userprofile/login.html'), name="login"),
    # выход
    path("logout/", auth_view.LogoutView.as_view(), name="logout"),
    # мой аккаунт
    path("myaccount/", views.myaccount, name="myaccount"),
    # мой магазин
    path("my-store/", views.my_store, name="mystore"),
    # детали заказа
    path("my-store/order-detail/<int:pk>/", views.my_store_order_detail, name="my_store_order_detail"),
    # добавление товара
    path("my-store/add-product/", views.add_product, name="add_product"),
    # изменение товара
    path("my-store/edit-product/<int:pk>/", views.edit_product, name="edit_product"),
    # удаление товара
    path("my-store/delete_product/<int:pk>/", views.delete_product, name="delete_product"),
    # детали товара
    path("vendors/<int:pk>/", views.vendor_detail, name="vendor_detail"),
]
