from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('products/', views.products, name='products'),
    path('products/<str:id>', views.product_view, name='product'),
    path('category/', views.category, name='category'),
    path('category/<str:name>', views.categories_view, name='categories'),
    path('cart/', views.cart_view, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('newsletter/', views.newsletter, name='newsletter'),

]
