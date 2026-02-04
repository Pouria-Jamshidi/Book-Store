from django.db import models
from django.db.models import Avg, OneToOneField, UniqueConstraint


# =================================================== Dynamic Addresses ===================================================
def imgCoverAddress(instance, filename):
    return f'book_cover/{instance.author.name}/{instance.title}/{filename}'

def bookFileAddress(instance, filename):
    return f'books_files/{instance.author.name}/{instance.title}/{filename}'

# ======================================================== Models ========================================================
class Genre(models.Model):
    name = models.CharField(max_length= 20, verbose_name= 'ژانرا',unique= True)

    class Meta:
        verbose_name= 'ژانرا'
        verbose_name_plural= 'ژانرا'

    def __str__(self):
        return f'{self.name}'

class Author(models.Model):
    name = models.CharField(max_length= 40, verbose_name= 'نویسنده')

    class Meta:
        verbose_name= 'نویسنده'
        verbose_name_plural= 'نویسنده'

    def __str__(self):
        return f'{self.name}'

class Book(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان کتاب')
    description = models.TextField(verbose_name='درباره کتاب', null= True, blank= True)
    genre = models.ManyToManyField(to= Genre,related_name= 'books', verbose_name= 'ژنرا')
    author = models.ForeignKey(to= Author, on_delete= models.PROTECT,related_name= 'books', verbose_name= 'نویسنده')
    cover = models.ImageField(upload_to= imgCoverAddress, null= True, blank= True, verbose_name= 'کاور کتاب')
    file = models.FileField(upload_to= bookFileAddress,verbose_name= 'فایل کتاب')
    created_at = models.DateTimeField(auto_now_add= True, verbose_name= 'تاریخ اضافه شدن به سایت')
    price = models.DecimalField(max_digits= 8, decimal_places=0, verbose_name= 'مبلغ')

    class Meta:
        verbose_name= 'کتاب'
        verbose_name_plural= 'کتاب'

    def score_average(self):
        """
        returns the average score of the book
        :return:
        """
        avg_score = self.scores.aggregate(ave=Avg('score')).get('ave')
        return round(avg_score or 0,2)

    def __str__(self):
        return f'{self.title}'

class Score(models.Model):
    book = models.ForeignKey(to= Book, on_delete= models.CASCADE,related_name= 'scores', verbose_name= 'کتاب')
    user = models.ForeignKey(to= 'accounts.User', on_delete= models.CASCADE,related_name= 'scores', verbose_name= 'کاربر')
    score = models.PositiveSmallIntegerField(verbose_name= 'امتیاز')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ امتیاز دادن')

    class Meta:
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیاز'
        unique_together = ('book', 'user')

    def __str__(self):
        return f'{self.book.title}, {self.user.username} = {self.score}'

class NavbarGenre(models.Model):
    position = models.PositiveSmallIntegerField(verbose_name='اولویت ژانرا')
    genre = OneToOneField(to=Genre,on_delete=models.CASCADE,null=True , blank=True, verbose_name= 'اسم ژانرا')

    class Meta:
        ordering = ['position'] #always order them based on position
        verbose_name = 'ژانرا نوار ناوبری'
        verbose_name_plural = 'ژانرا نوار کاربری'
        constraints = [
            UniqueConstraint(fields=['position'], name='unique_position'),
        ]

    def __str__(self):
        return f'{self.position} = {self.genre.name}'