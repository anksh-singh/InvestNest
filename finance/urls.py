from django.urls import path, include
from .views import SignUpView, AddClient,  AdvisorClientsList, AddProduct, AdvisorPurchaseProduct

urlpatterns = [
    path('user/sign-up/', SignUpView.as_view(), name='sign_up'),
    path('advisor/add-client/', AddClient.as_view(), name='add_client'),
    path('get/clients-list/', AdvisorClientsList.as_view(), name='clients_list'),
    path('admin/add-products/', AddProduct.as_view(), name='add_product'),
    path('advisor/purchase-product/', AdvisorPurchaseProduct.as_view(), name='advisor_purchase_product'),


]