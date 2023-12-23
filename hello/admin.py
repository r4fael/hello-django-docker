from django.contrib import admin
from .models import Client, Page, Link, Contract

# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'create_at', 'update_at')

admin.site.register(Client)
admin.site.register(Page)
admin.site.register(Contract)
admin.site.register(Link)
