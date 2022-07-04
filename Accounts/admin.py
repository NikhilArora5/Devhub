from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,skill


class AccountAdmin(UserAdmin):
	ordering=['email']
	list_display = ('email', 'name', 'phone' ,'created', 'last_login', 'is_admin', 'is_staff','email_confirmed','is_active')
	search_fields = ('email', 'name','phone')
	readonly_fields = ('created', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Account, AccountAdmin)
# class skills(admin):
# 	ordering=['created']
# 	list_display=('name','created')
# 	search_fields = ('owner', 'name')
# 	filter_horizontal = ()
# 	list_filter = ()
# 	fieldsets = ()

admin.site.register(skill)

# Register your models here.
