from django.db import models
from django.contrib.auth.models import AbstractUser



# =================================================== Dynamic Addresses ===================================================



# ======================================================== Models ========================================================
class User(AbstractUser):
    credit = models.IntegerField(default=0, blank=True, verbose_name="کیف پول")
    wishlist = models.ManyToManyField('core.Book', blank=True, related_name='wishlist', verbose_name= 'فهرست خواسته ها')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر'

    def __str__(self):
        return f'{self.username}'