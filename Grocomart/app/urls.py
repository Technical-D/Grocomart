from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),

    path('activate-user/<uidb64>/<token>',views.activate_user, name='activate'),

    path('logout', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('products/', views.products, name='products'),
    path('products/<str:id>', views.product_view, name='product'),
    path('review/<int:p_id>/', views.submit_review, name='review'),

    path('category/', views.category, name='category'),
    path('category/<str:name>', views.categories_view, name='categories'),
    path('cart/', views.cart_view, name='cart'),
    path('update_item/', views.updateItem, name='update_item'),
    path('checkout/', views.checkout, name='checkout'),
    path("shipping_address/", views.shipping_address, name="shipping_address"),
    
    path('process_payment/', views.process_payment, name='process_payment'),
    path('invoice/<int:id>', views.invoice, name='invoice'),

    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('newsletter/', views.newsletter, name='newsletter'),




    path("password_reset/", views.password_reset_request, name="password_reset"),

]
