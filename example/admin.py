from django.contrib import admin

# Register your models here.
from example.models import id
from example.models import swear_words

admin.site.register(id)
admin.site.register(swear_words)