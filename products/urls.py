from django.urls import path, include
from . import views
from .views import login_view, seller_dashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add/', views.add_product, name='add_product'),
    path('upload/', views.upload_product, name='upload_product'),
    path('purchase/<int:product_id>/', views.purchase_product, name='purchase_product'),  # 👈 Thêm dòng này
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'), 
    path('diem-danh/', views.diem_danh, name='diem_danh'),
    path('vi-tien/', views.vi_tien, name='vi_tien'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('dat-hang/', views.dat_hang, name='dat_hang'),
    path('cart/', views.cart_view, name='cart'),
    path('login/', login_view, name='login'),
    path('seller/', seller_dashboard, name='seller_dashboard'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('search/', views.search_view, name='search'), 
    path('category/<slug:category_slug>/', views.product_by_category, name='product_by_category'),
    path('danh-muc/<slug:category_slug>/', views.product_by_category, name='product_by_category'),
    path('khuyen-mai/', views.all_promotion_products, name='all_promotion_products'),
    path('ho-so/', views.user_profile, name='user_profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
