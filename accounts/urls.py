from django.urls import path, include
from . import views
from .views import user_profile, edit_profile

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('diem-danh/', views.check_in_view, name='check_in'),
    path('vi-xu/', views.wallet_view, name='wallet'),
    path('ho-so/', user_profile, name='user_profile'),
    path('lich-su-don-hang/', views.order_history, name='order_history'),
    path('ho-so/cap-nhat/', views.edit_profile, name='edit_profile'),
    path('ho-so/doi-mat-khau/', views.change_password, name='change_password'),
    path('ho-so/xoa-tai-khoan/', views.delete_account, name='delete_account'),
    path('ho-so/', user_profile, name='user_profile'),
    path('ho-so/sua/', edit_profile, name='edit_profile'),

    # Nếu muốn thêm /profile/:
    path('profile/', user_profile),  # Có thể thêm để dùng song song
    path('profile/edit/', edit_profile),

]
