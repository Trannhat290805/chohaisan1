from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from .models import DiemDanh
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Attendance, Wallet
from datetime import date, timedelta
from django.contrib.auth import authenticate, login
from django.template.loader import select_template
from django.utils.translation import get_language
from .models import Category
from django.db.models import Q
from django.contrib.auth.models import User


def all_promotion_products(request):
    # Chọn các sản phẩm có giảm giá
    promotion_products = Product.objects.filter(discount_percent__gt=0)
    return render(request, 'products/all_promotions.html', {'products': promotion_products})


def slider_view(request):
    products = Product.objects.all()[:10]
    return render(request, 'slider.html', {'products': products})

def product_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'products/category_page.html', {
        'category': category,
        'products': products
    })

def product_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')  # lấy id danh mục từ URL (?category=1)

    # Lấy danh sách tất cả danh mục (để hiển thị menu)
    categories = Category.objects.all()

    if query:
        related_products = Product.objects.filter(name__icontains=query).order_by('-id')
        return render(request, 'products/product_list.html', {
            'search_mode': True,
            'related_products': related_products,
            'categories': categories,
        })
    
    elif category_id:
        # Nếu người dùng chọn danh mục → lọc sản phẩm theo danh mục đó
        products_by_category = Product.objects.filter(category_id=category_id).order_by('-id')
        return render(request, 'products/product_list.html', {
            'search_mode': False,
            'products_by_category': products_by_category,
            'categories': categories,
        })
    
    else:
        # Mặc định (hiển thị danh mục nổi bật như hiện tại)
        bestsellers = Product.objects.filter(category='bestseller').order_by('-id')
        shellfish = Product.objects.filter(category='shellfish').order_by('-id')
        frozen = Product.objects.filter(category='frozen').order_by('-id')
        promotion = Product.objects.filter(category='promotion').order_by('-id')
        sushi = Product.objects.filter(category='sushi').order_by('-id')
        tuoisong = Product.objects.filter(category='tuoisong').order_by('-id')
        nhapkhau = Product.objects.filter(category='nhapkhau').order_by('-id')
        cahoi = Product.objects.filter(category='cahoi').order_by('-id')
        hausua = Product.objects.filter(category='hausua').order_by('-id')
        cuaghe = Product.objects.filter(category='cuaghe').order_by('-id')
        tom = Product.objects.filter(category='tom').order_by('-id')
        muc = Product.objects.filter(category='muc').order_by('-id')
        eat = Product.objects.filter(category='eat').order_by('-id')
        giavi = Product.objects.filter(category='giavi').order_by('-id')
        return render(request, 'products/product_list.html', {
            'search_mode': False,
            'bestsellers': bestsellers,
            'shellfish': shellfish,
            'frozen': frozen,
            'promotion': promotion,
            'sushi': sushi,
            'tuoisong': tuoisong,
            'nhapkhau': nhapkhau,
            'cahoi': cahoi,
            'hausua': hausua,
            'cuaghe': cuaghe,
            'tom': tom,
            'muc': muc,
            'eat': eat,
            'giavi': giavi,
            'categories': categories,
        })


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        total_price += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': item_total,
        })

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def update_cart(request, product_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            if action == 'increase':
                cart[str(product_id)] += 1
            elif action == 'decrease':
                if cart[str(product_id)] > 1:
                    cart[str(product_id)] -= 1
                else:
                    cart.pop(str(product_id))
        
        request.session['cart'] = cart
    return redirect('view_cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('view_cart')

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # 🟢 Đây là dòng QUAN TRỌNG bạn thiếu
            product.save()
            return redirect('product_list')  # hoặc trang bạn muốn
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

def purchase_product(request, product_id):
    # Tạm thời chỉ trả về trang thành công đơn giản
    return render(request, 'products/purchase_success.html', {'product_id': product_id})

def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # nhận cả ảnh
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Đăng xong quay về trang shop hải sản
    else:
        form = ProductForm()
    return render(request, 'products/upload_product.html', {'form': form})



@login_required
def diem_danh(request):
    attendance, created = Attendance.objects.get_or_create(user=request.user)
    today = date.today()
    message = ""
    reward = 0

    if request.method == "POST":
        if attendance.last_check_in == today:
            message = "Bạn đã điểm danh hôm nay rồi!"
        else:
            if attendance.last_check_in and (today - attendance.last_check_in).days == 1:
                attendance.streak += 1
            else:
                attendance.streak = 1  # Reset nếu bỏ ngày

            attendance.current_day += 1
            attendance.last_check_in = today

            # Phần thưởng
            if attendance.streak == 7:
                reward = 1000
                attendance.streak = 0  # Reset sau 7 ngày liên tiếp
            else:
                reward = 200

            attendance.coins += reward
            attendance.save()

            message = f"Bạn đã nhận {reward} xu! Tổng xu hiện tại: {attendance.coins} xu."

    days = []
    for day in range(1, 8):
        checked_in = day <= attendance.current_day
        days.append({
            'day': day,
            'checked_in': checked_in,
        })

    context = {
        'days': days,
        'message': message,
        'attendance': attendance,
        'today': today,
    }
    return render(request, 'attendance.html', context)



def vi_tien(request):
    return render(request, 'vi_tien.html')

@login_required
def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    context = {
        'product': product,
        'user': user,
        'total_price': product.price,
    }
    return render(request, 'products/checkout.html', context)

def dat_hang(request):
    if request.method == 'POST':
        try:
            # Lấy giỏ hàng từ session
            cart = request.session.get('cart', {})

            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                product.sold += quantity  # ✅ Cập nhật số lượng đã bán
                product.save()

            # Xoá giỏ hàng sau khi đặt hàng
            request.session['cart'] = {}

            messages.success(request, 'Đơn hàng của bạn đã được đặt thành công!')
            return redirect('product_list')

        except Exception as e:
            messages.error(request, 'Xin lỗi quý khách vì sự cố! Đặt hàng thất bại.')
            return redirect('product_list')
    else:
        messages.error(request, 'Phương thức không hợp lệ!')
        return redirect('product_list')

    
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        total_price += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': item_total,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


def some_view(request):
    context = {}
    if request.user.is_authenticated:
        try:
            context['attendance'] = Attendance.objects.get(user=request.user)
        except Attendance.DoesNotExist:
            context['attendance'] = None
    return render(request, 'your_template.html', context)



@login_required
def login_view(request):
    lang = get_language()
    template_name = f"{lang}/login.html" if lang else "login.html"

    username_error = None
    password_error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Kiểm tra user tồn tại chưa
        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            # User không tồn tại
            username_error = "Tài khoản không tồn tại"
            return render(request, template_name, {
                'username_error': username_error,
            })

        # Nếu tồn tại, kiểm tra mật khẩu
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            # Sai mật khẩu
            password_error = "Sai mật khẩu"
            return render(request, template_name, {
                'password_error': password_error,
                'username': username,  # giữ lại tên đăng nhập đã nhập để không phải nhập lại
            })

    return render(request, template_name)


@login_required
def seller_dashboard(request):
    return render(request, 'products/seller_dashboard.html')
def search_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)  # Tìm kiếm sản phẩm theo tên (không phân biệt chữ hoa/thường)

    return render(request, 'products/product_list.html', {
        'products': products,
        'query': query,
    })
    
@login_required
def user_profile(request):
    user = request.user
    return render(request, 'user_profile.html', {'user': user})





