from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import Customer, Product, Newsletter
from django.contrib.auth.models import Group

# Register your models here.
class CustomerAdmin(UserAdmin):
    model = Customer
    list_display = ('email','first_name','last_name','mobile','date_joined', 'last_login', 'is_admin','is_staff', )
    search_fields = ('email','first_name','last_name')
    readonly_fields=('id', 'date_joined', 'last_login')
    ordering = ('email',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Customer, CustomerAdmin)
admin.site.unregister(Group)
admin.site.register(Product)
admin.site.register(Newsletter)
