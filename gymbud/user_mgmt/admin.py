from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Profile)
admin.site.register(Gym)
admin.site.register(Location)
admin.site.register(UserPhoto)
admin.site.register(UserSwipe)
admin.site.register(Matches)
admin.site.register(NotMatches)
admin.site.register(FavoriteExercise)
admin.site.register(SocialLinks)
admin.site.register(Blocked)
admin.site.register(Exercise)

from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'first_name',)
    list_filter = ('is_active', 'is_staff', 'current_location')
    ordering = ('-start_date',)
    list_display = ('id','email',  'first_name',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email',  'first_name', 'current_location', 'search_range', 'age', 'birthday')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'first_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(User, UserAdminConfig)