from django.contrib import admin
from core.models import Genre,Author,Book,Score,NavbarGenre

admin.site.register(Genre)
admin.site.register(NavbarGenre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Score)