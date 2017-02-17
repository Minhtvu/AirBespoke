from django.contrib import admin

# Register your models here.
from .models import Tailor
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _



class TailorModelAdmin(admin.ModelAdmin):
    UserAdmin.list_display += ('isTailor',)
    UserAdmin.list_filter += ('isTailor',)
    UserAdmin.fieldsets =  (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'isTailor',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ["name", "user", "updated"]
    list_display_links = ["name"]
    list_filter = ["updated"]
    search_fields = ["name", "user", "content"]
    list_editable = []

    class Meta:
        model = Tailor
admin.site.register(Tailor, TailorModelAdmin)
