from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import  LogoutView
from django.urls import path
from .import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordresetForm, MyPasswordChangeForm, MySetPasswordForm
from .views import payment

urlpatterns = [
    path("", views.home),
    path("about/", views.about,name="about"),
    path("contact/", views.contact, name="contact"),

    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
    path("category-title/<val>", views.CategoryTitle.as_view(), name='category-title'),
    path("product_detail/<int:pk>", views.ProductDetailView.as_view(), name="product_detail"),
    path("add-to-cart/", views.add_to_cart, name="add-to-cart"),
    path("cart/", views.show_cart, name="showcart"),
    path("checkout/", views.Checkout.as_view(), name="checkout"),
    path('payment/', payment, name='payment'),
    path("payment/done/", views.payment_done, name="payment_done"),
    path("orders/", views.orders, name="orders"),
    path("pluswishlist/", views.plus_wishlist),
    # path("minuswishlist/", views.minus_wishlist),
    path('wishlist_products/', views.wishlist_products, name='wishlist_products'),

    path("pluscart/", views.plus_cart, name="pluscart"),
    path("minuscart/", views.minus_cart, name="minuscart"),
    path("removecart/", views.remove_cart),
    path("search/", views.search_product, name="search"),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path("registration/", views.CustomerRegistrationView.as_view(), name="customerregistration"),
    path("accounts/login/", auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name="login"),
    path('password-reset/', auth_view.PasswordResetView.as_view(
        template_name='app/password_reset.html', form_class=MyPasswordresetForm),
         name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(
        template_name='app/password_reset_done.html', ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(
        template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(
        template_name='app/changepassword.html', form_class=MyPasswordChangeForm,
        success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(
        template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

