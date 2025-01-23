from django.contrib import admin
from Food_ordering_app.models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(PizzaTopping)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)

@admin.register(ShippingInformation)
class ShippingInformationAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'address', 'city', 'state', 'zip_code', 'email')

