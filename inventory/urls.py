from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('login/', views.login_user, name='login_user'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('export-csv/', views.export_products_csv, name='export_products_csv'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('import-csv/', views.import_products_csv, name='import_products_csv'),
    path('export-pdf/', views.export_products_pdf, name='export_products_pdf'),




]
