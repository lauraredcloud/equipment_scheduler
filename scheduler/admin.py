from django.contrib import admin
from scheduler.models import User,ItemType,Item,Checkout

class CheckoutAdmin(admin.ModelAdmin):
    list_display = ('user','item','start_time','end_time')
    
admin.site.register(User)
admin.site.register(ItemType)
admin.site.register(Item)
admin.site.register(Checkout,CheckoutAdmin)