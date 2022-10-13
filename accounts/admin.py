from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display=('email', 'first_name', 'last_name', 'last_login', 'is_active')

    filter_horizontal =()
    list_filter =()
    #fieldSets = ()

class UserProfileAdmin(admin.ModelAdmin):
    def thumnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%">'.format(object.profile_picture.url))
    thumnail.short_description = 'Profile Picture'
    list_display = ('thumnail', 'user', 'city', 'state' , 'country')

admin.site.register(Account)
admin.site.register(UserProfile, UserProfileAdmin)
