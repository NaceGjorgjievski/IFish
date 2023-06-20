"""
URL configuration for IFish_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from IFish.views import home, productScreen, categoryScreen, loginScreen, registerScreen, logoutUser, cartScreen, \
    shippingScreen, paymentScreen, removeCartItem, orderScreen, orderHistoryScreen, addProductScreen, ordersScreen,\
    manageOrderScreen, actionOrderSent, actionOrderArrived, productsScreen, productEditScreen
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('products/<int:pk>/', productScreen, name="productScreen"),
    path('category/<int:pk>/', categoryScreen, name="categoryScreen"),
    path('login/', loginScreen, name="loginScreen"),
    path('register/', registerScreen, name="registerScreen"),
    path('logout/', logoutUser, name="logoutUser"),
    path('cart/', cartScreen, name="cartScreen"),
    path('shipping/', shippingScreen, name="shippingScreen"),
    path('payment/', paymentScreen, name="paymentScreen"),
    path('remove/<int:pk>', removeCartItem, name="removeCartItem"),
    path('order/<int:pk>', orderScreen, name="orderScreen"),
    path('orders/', orderHistoryScreen, name="orderHistoryScreen"),
    path('add-product/', addProductScreen, name="addProductScreen"),
    path('manage/orders', ordersScreen, name="ordersScreen"),
    path('manage/orders/<int:pk>', manageOrderScreen, name="manageOrderScreen"),
    path('manage/orders/shipped/<int:pk>', actionOrderSent, name="actionOrderSent"),
    path('manage/orders/delivered/<int:pk>', actionOrderArrived, name="actionOrderArrived"),
    path('manage/products', productsScreen, name='productsScreen'),
    path('manage/products/edit/<int:pk>', productEditScreen, name="productEditScreen")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
