from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.shortcuts import render



class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



@login_required
def seller_dashboard(request):
    return render(request, 'dashboard.html')
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    origin = models.CharField(max_length=255, default="Việt Nam")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default="500g")
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=100)
    old_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)  # 👈 Thêm dòng này
    sold = models.PositiveIntegerField(default=0)  # hoặc IntegerField

    
    def __str__(self):
        return self.name
    
class DiemDanh(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ngay = models.DateField()
    
    class Meta:
        unique_together = ('user', 'ngay')  # Mỗi user chỉ điểm danh 1 lần/ngày



class Attendance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_day = models.IntegerField(default=0)
    last_check_in = models.DateField(null=True, blank=True)
    coins = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)  # ➡️ Số ngày liên tiếp điểm danh


    @property
    def get_rank(self):
        if self.coins >= 5000000:
            return "Khách VIP"
        elif self.coins >= 1000000:
            return "Khách Kim Cương"
        elif self.coins >= 100000:
            return "Khách Vàng"
        elif self.coins >= 50000:
            return "Khách Bạc"
        elif self.coins >= 10000:
            return "Khách Đồng"
        elif self.coins >= 500:
            return "Khách Quen"
        else:
            return "Người Mới"

    def __str__(self):
        return f'{self.user.username} - {self.coins} xu - {self.get_rank()}'

def get_rank_class(self):
    return self.get_rank().lower().replace(" ", "\\ ")
    
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    
    
    

    

