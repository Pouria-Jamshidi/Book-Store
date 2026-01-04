from django.db import models



# ==================================================== CHOICE FIELDS ====================================================
class StatusChoices(models.TextChoices):
    PENDING = ("pending", "در حال انجام")
    PAID = ("paid", "پرداخت شده")
    REFUNDED = ("refunded", "بازگشت وجه")
    CANCELED = ("canceled", "لغو شده")


# ======================================================== Models ========================================================

class Order(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders', verbose_name= 'کاربر')
    status = models.CharField(max_length=8, choices=StatusChoices.choices, default=StatusChoices.PENDING, verbose_name= 'وضعیت فاکتور')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name= 'تاریخ ساخته شدن')
    updated_at = models.DateTimeField(auto_now=True, verbose_name= 'تاریخ تغییر داده شدن')
    total = models.DecimalField(max_digits=10, decimal_places=0, verbose_name= 'کل مبلغ فاکتور')

    class Meta:
        verbose_name = 'فاکتور'
        verbose_name_plural = 'فاکتور'

    def __str__(self):
        return f'{self.id} - {self.user} - {self.total} - {self.status}'

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name= 'items', verbose_name= 'فاکتور')
    book = models.ForeignKey('core.Book', on_delete=models.CASCADE, verbose_name= 'کتاب')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name= 'مبلغ')
    quantity = models.PositiveIntegerField(default=1, verbose_name= "تعداد")

    class Meta:
        verbose_name = 'ایتم های فاکتور'
        verbose_name_plural = 'ایتم های فاکتور'
        unique_together = ('order', 'book')