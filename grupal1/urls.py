
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.contrib.auth import views as auth_views
from grup1.views import (
    index, logged_in, tomar_pedido, guardar_detalle, 
    listar_pedidos, detalle_pedido, cambiar_estado, 
    tomar_pedido_cliente, guardar_detalle_cliente, verpedidos_cliente, detalle_pedido_cliente, confirmacion_pedido,
    productos, eliminar_producto, nopermiso, registro
    
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # ************** Login ***********
    #path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logged_in/', logged_in, name='logged_in'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # ************* Pedidos **************
    path('pedidos/', listar_pedidos, name='listar_pedidos'),
    path('pedidos/<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),
    path('pedidos/<int:pedido_id>/cambiar_estado/', cambiar_estado, name='cambiar_estado'),
    path('tomar_pedido/', tomar_pedido, name='tomar_pedido'),
    path('guardar_detalle/<int:idpedido>/', guardar_detalle, name='guardar_detalle'),
    #*********** Pedidos Cliente **************************
    path('tomar_pedido_cliente/', tomar_pedido_cliente, name='tomar_pedido_cliente'),
    path('guardar_detalle_cliente/<int:idpedido>/', guardar_detalle_cliente, name='guardar_detalle_cliente'),
    path('ver_pedidos_cliente/', verpedidos_cliente, name='ver_pedidos_cliente'),
    path('detalle_pedido_cliente/<int:pedido_id>/', detalle_pedido_cliente, name='detalle_pedido_cliente'),
    path('confirmacion_pedido/', confirmacion_pedido, name='confirmacion_pedido'),
    
    # ***********  Productos ************
    path('productos/', productos, name='productos'),
    path('productos/<int:pk>/eliminar/', eliminar_producto, name='eliminar_producto'),
    path('nopermiso/', nopermiso, name='nopermiso'),
    #************* Usarios *************
    path('registro/', registro, name='registro'),

]

# Configuración para servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)