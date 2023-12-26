from django.contrib import admin
from .models import Client, Page, Link, Contract


# Modifiers
class LinkAdmin(admin.ModelAdmin):
    exclude = ('_click_count',)


class ContractInLine(admin.StackedInline):
    model = Contract
    min_num = 1
    extra = 0

class ClientAdmin(admin.ModelAdmin):
    inlines = [ContractInLine]


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_links_display')
    change_list_template = ('Títulosss', 'Links')
        

# Register your models here.
admin.site.register(Link, LinkAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Contract)

