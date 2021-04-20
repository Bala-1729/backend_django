from django.contrib import admin
from .models import UserProfile, NPKValues

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(NPKValues)
