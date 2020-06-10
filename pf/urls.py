"""pf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path
from pfapp import views

urlpatterns = [

    path('', views.index),
    path('admin/', admin.site.urls),
    path('Settings/', views.Settings),
    path('Delivery_Conformation/', views.Delivery_Conformation),
    path('Learn_Farming/', views.Learn_Farming),
    path('Surpluse_Market/', views.Surpluse_Market),
    path('My_Contracts/', views.My_Contracts),
    path('My_Farmers/', views.My_Farmers),
    path('Explore/', views.Explore),
    path('signup/', views.signup),
    path('logout/', views.logout),
    path('Profile/', views.Profile),
    path('My_Earnings/',views.My_Earnings),
    path('My_Customers/',views.My_Customers),
    path('Contracts_Manager/New_Request/',views.New_Request),
    path('Contracts_Manager/Active_Contracts/',views.Active_Contracts),
    path('Contracts_Manager/Active_Orders/',views.Active_Orders),
    path('Contracts_Manager/Add_Contracts/',views.Add_Contracts),
    path('Customer_Reviews/',views.Customer_Reviews),
    path('Dispatch_Manager/',views.Dispatch_Manager),
    path('user/<email>/',views.view_profile),
    path('checkout/', views.checkout),
    path('orders/', views.orders),
    path('addreview/', views.addreview),
    path('orderstatus/orderid=<order_id>&status=<status>/', views.orderstatus),
    path('Contracts_Manager/Active_Contracts/deactivate/<contract_id>/',views.deactivate_contract),

]



