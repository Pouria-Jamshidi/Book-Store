from django.db import models
from django.contrib.auth.models import AbstractUser



# =================================================== Dynamic Addresses ===================================================



# ======================================================== Models ========================================================
class User(AbstractUser):
    pfp = models.ImageField(default='pfp_uploads/default_avatar.png', upload_to='pfp_uploads', verbose_name='عکس پروفایل')
    credit = models.IntegerField(default=0, blank=True, verbose_name="کیف پول")


    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر'

    def __str__(self):
        return f'{self.username}'