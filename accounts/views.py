from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile
from django.contrib.auth import update_session_auth_hash
from datetime import datetime



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Giữ đăng nhập sau khi đổi mật khẩu
            messages.success(request, "Đổi mật khẩu thành công.")
            return redirect('user_profile')
        else:
            messages.error(request, "Vui lòng sửa lỗi bên dưới.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Tài khoản đã được xóa.")
        return redirect('home')  # Hoặc trang bạn muốn chuyển sau khi xóa
    return render(request, 'delete_account.html')


@login_required
def edit_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')

        # Cập nhật họ tên
        if full_name:
            parts = full_name.split(' ')
            user.first_name = parts[0]
            user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
        if email:
            user.email = email
        user.save()

        profile.gender = gender
        if birth_date:
            try:
                profile.birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
            except ValueError:
                profile.birth_date = None
        else:
            profile.birth_date = None
        profile.phone = phone
        profile.address = address
        profile.save()

        messages.success(request, "Cập nhật thông tin thành công!")
        return redirect('user_profile')

    else:
        full_name = user.get_full_name()

    return render(request, 'edit_profile.html', {
        'user': user,
        'profile': profile,
        'full_name': full_name,
    })

@login_required
def order_history(request):
    # Giả sử bạn có model Order liên kết với người dùng
    orders = request.user.order_set.all()  # hoặc models.Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})

@login_required
def user_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    return render(request, 'profile.html', {
        'user': user,
        'profile': profile,
    })
    
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "⚠️ Tên đăng nhập đã tồn tại.")
        elif password != confirm_password:
            messages.error(request, "⚠️ Mật khẩu xác nhận không khớp.")
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, "🎉 Đăng ký thành công! Vui lòng đăng nhập.")
            return redirect('login')  # Hoặc trang bạn muốn

    return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Tài khoản không tồn tại!')
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Sai mật khẩu!')
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def check_in_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    today = timezone.now().date()
    
    if user_profile.last_check_in != today:
        if (today - user_profile.last_check_in).days > 1:
            user_profile.consecutive_days = 1  # Reset nếu bỏ qua 1 ngày
        else:
            user_profile.consecutive_days += 1

        if user_profile.consecutive_days >= 7:
            user_profile.consecutive_days = 7

        if user_profile.consecutive_days == 7:
            user_profile.wallet += 500
        else:
            user_profile.wallet += 200

        user_profile.last_check_in = today
        user_profile.save()
    
    return render(request, 'accounts/check_in.html')

@login_required
def wallet_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'accounts/wallet.html', {'wallet': user_profile.wallet})
