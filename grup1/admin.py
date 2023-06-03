from django.contrib import admin
from .models import Etiqueta, Estado, Detalle, Pedido, Producto

# Register your models here.
admin.site.register(Etiqueta)
admin.site.register(Estado)
admin.site.register(Detalle)
admin.site.register(Pedido)
admin.site.register(Producto)