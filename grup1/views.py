import random, string
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Pedido, Estado, Producto, Detalle
from .forms import ProductoForm, RegistroForm
from django.core.mail import send_mail


# Create your views here.
# ************** Login ***************
def index(request):
    productos = Producto.objects.all()
    return render(request, 'index.html', {'productos': productos})

@login_required (login_url='nopermiso')
def logged_in(request):
    return render(request, 'logged_in.html')



# ************** Fin Login **************************


# ***********   Usuario ************

# ******* Enviar Correo ***********

def enviar_correo(destinatario, contrasena):
    # Configurar los detalles del correo
    remitente = 'talento@fabricadecodigo.dev'
    password = 'talento.,2023'
    asunto = 'Contraseña Aleatoria Generada'
    mensaje = f'Tu contraseña aleatoria es: {contrasena}. ¡Recuerda cambiarla después de iniciar sesión!'

    try:
        # Enviar el correo
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=remitente,
            recipient_list=[destinatario],
            auth_user=remitente,
            auth_password=password,
            fail_silently=False,
        )
    except Exception as e:
        # Manejar el error de envío de correo
        print('Error al enviar el correo:', str(e))

# ******* Fin Enviar Correo **********

def generar_contrasena_aleatoria():
    # Genera una cadena de 6 caracteres que incluye letras y números
    caracteres = string.ascii_letters + string.digits
    contrasena = ''.join(random.choice(caracteres) for _ in range(6))
    return contrasena

# Generar la contraseña aleatoria
contrasena_aleatoria = generar_contrasena_aleatoria()

# Mostrar la contraseña en pantalla
print("Contraseña aleatoria generada:", contrasena_aleatoria)

# Registro
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Generar la contraseña aleatoria
            contrasena_aleatoria = generar_contrasena_aleatoria()

            # Guardar el usuario con la contraseña aleatoria
            user = form.save(commit=False)
            user.set_password(contrasena_aleatoria)
            user.save()

            # Enviar la contraseña aleatoria por correo electrónico
            enviar_correo(user.email, contrasena_aleatoria)

            # Mostrar la contraseña aleatoria en pantalla
            messages.success(request, f'Registro exitoso. Se ha enviado la contraseña aleatoria al correo registrado. ¡Recuerda cambiarla después de iniciar sesión!')
            return redirect('registro')  # Redirige a la página de registro con el mensaje de éxito
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

#*************** Fin Registro Usuario ****************


# ************ Permisos ****************

def nopermiso(request):
    return render(request, 'nopermiso.html')


# ************   Pedidos ***************

@login_required (login_url='nopermiso')
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='nopermiso')
def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'lista_pedidos.html', {'pedidos': pedidos})

@login_required (login_url='nopermiso')
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='nopermiso')
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedidos = Pedido.objects.all()
    detalles = pedido.detalle_set.all()
    estados = Estado.objects.all()  # Obtener todos los estados
    return render(request, 'detalle_pedido.html', {'pedido': pedido, 'detalles': detalles, 'pedidos': pedidos, 'estados': estados})

@login_required (login_url='nopermiso')
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='nopermiso')
def cambiar_estado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        estado_id = request.POST.get('estado')
        estado = get_object_or_404(Estado, idestado=estado_id)
        pedido.estado = estado
        pedido.save()
        return redirect('detalle_pedido', pedido_id=pedido_id)
    

#************* Tomar Pedidos Super User Staff ********
@login_required (login_url='nopermiso')
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='nopermiso')
def tomar_pedido(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        vendedor = request.user  # El usuario logueado será el vendedor
        cliente_id = request.POST.get('cliente_id')
        direccion = request.POST.get('direccion')
        observaciones = request.POST.get('observaciones')

        # Obtener el estado predeterminado
        estado_predeterminado = Estado.objects.get(idestado=1)

        # Crear un nuevo pedido con el estado predeterminado
        pedido = Pedido(vendedor=vendedor, cliente_id=cliente_id, estado=estado_predeterminado, direccion=direccion, observaciones=observaciones)
        pedido.save()

        # Obtener el ID del pedido
        idpedido = pedido.id

        # Redireccionar a la vista de guardar_detalle con el ID del pedido como parámetro
        return redirect('guardar_detalle', idpedido=idpedido)

    # Obtener los datos necesarios para mostrar en el formulario
    clientes = User.objects.filter(is_staff=False, is_superuser=False, is_active=True)
    productos = Producto.objects.all()

    return render(request, 'tomar_pedido.html', {'clientes': clientes, 'productos': productos})

# **************** Fin Tomar Pedido Super User Staff 




# *****************  Guardar Detalle de Pedido Super User Staff**************
@login_required (login_url='nopermiso')
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='nopermiso')
def guardar_detalle(request, idpedido):
    detalles = None  # Asignar un valor predeterminado a la variable detalles
    

    if request.method == 'POST':
        # Obtener los datos del formulario
        cantidad = request.POST.get('cantidad')
        precio = request.POST.get('precio')
        idproducto_id = request.POST.get('producto_id')
        detalles = Detalle.objects.filter(idpedido_id=idpedido)

        # Validar si el precio no está vacío antes de convertirlo a entero
        if precio:
            precio = int(precio)

            # Crear un nuevo detalle de pedido asociado al idpedido
            detalle = Detalle(cantidad=cantidad, precio=precio, idpedido_id=idpedido, idproducto_id=idproducto_id)
            detalle.save()
            

    # Obtener los datos necesarios para mostrar en el formulario
    pedido = Pedido.objects.get(id=idpedido)  # Obtener el pedido correspondiente al idpedido
    productos = Producto.objects.all()

    return render(request, 'guardar_detalle.html', {'pedido': pedido, 'productos': productos , 'detalles': detalles})


# ************   Fin Pedidos  Super User Staff*************** *************
# **************************************************************************





# *************** Pedidos Cliente ***************
#***********************************************
#*************Tomar Pedidos Cliente ************
@login_required (login_url='nopermiso')
@user_passes_test(lambda u: u.is_active and not u.is_staff and not u.is_superuser, login_url='nopermiso')
def tomar_pedido_cliente(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        vendedor = request.user  # El usuario logueado será el vendedor
        cliente_id = request.user.id # El usuario logueado será el cliente('cliente_id')
        direccion = request.POST.get('direccion')
        observaciones = request.POST.get('observaciones')

        # Obtener el estado predeterminado
        estado_predeterminado = Estado.objects.get(idestado=1)

        # Crear un nuevo pedido con el estado predeterminado
        pedido = Pedido(vendedor=vendedor, cliente_id=cliente_id, estado=estado_predeterminado, direccion=direccion, observaciones=observaciones)
        pedido.save()

        # Obtener el ID del pedido
        idpedido = pedido.id

        # Redireccionar a la vista de guardar_detalle con el ID del pedido como parámetro
        return redirect('guardar_detalle_cliente', idpedido=idpedido)

    # Obtener los datos necesarios para mostrar en el formulario
    
    productos = Producto.objects.all()

    return render(request, 'tomar_pedido_cliente.html', {'clientes': [request.user], 'productos': productos})

# **************** Fin Tomar Pedido Cliente *****************************




# *****************  Guardar Detalle Solicitud de Pedido Cliente**************
@login_required (login_url='nopermiso')
@user_passes_test(lambda u: u.is_active and not u.is_staff and not u.is_superuser, login_url='nopermiso')
def guardar_detalle_cliente(request, idpedido):
    detalles = None  # Asignar un valor predeterminado a la variable detalles
    

    if request.method == 'POST':
        # Obtener los datos del formulario
        cantidad = request.POST.get('cantidad')
        precio = request.POST.get('precio')
        idproducto_id = request.POST.get('producto_id')
        detalles = Detalle.objects.filter(idpedido_id=idpedido)

        # Validar si el precio no está vacío antes de convertirlo a entero
        if precio:
            precio = int(precio)

            # Crear un nuevo detalle de pedido asociado al idpedido
            detalle = Detalle(cantidad=cantidad, precio=precio, idpedido_id=idpedido, idproducto_id=idproducto_id)
            detalle.save()
            
    # Obtener los datos necesarios para mostrar en el formulario
    pedido = Pedido.objects.get(id=idpedido)  # Obtener el pedido correspondiente al idpedido
    productos = Producto.objects.all()

    return render(request, 'guardar_detalle_cliente.html', {'pedido': pedido, 'productos': productos , 'detalles': detalles})



#***************** Confirmación Pedido ********************

def confirmacion_pedido(request):
    return render(request, 'confirmacion_pedido.html')
#******************* Fin Tomar Pedidos Cliente ******************





# ****************** Seguimiento Pedidos Cliente ******************

@login_required (login_url='nopermiso')
@user_passes_test(lambda u: u.is_active and not u.is_staff and not u.is_superuser, login_url='nopermiso')
def verpedidos_cliente(request):
    cliente = request.user
    pedidos = Pedido.objects.filter(cliente=cliente)

    return render(request, 'ver_pedidos_cliente.html', {'pedidos': pedidos})

def detalle_pedido_cliente(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    mensaje = ""

    if request.method == 'POST':
        if pedido.estado.idestado in [1, 2]:  # Verificar si el estado es "En Proceso"
            estado_cancelado = Estado.objects.get(idestado=5)  # Obtener el estado "Cancelado"
            pedido.estado = estado_cancelado  # Cambiar el estado del pedido a "Cancelado"
            pedido.save()  # Guardar los cambios en el pedido
            return redirect('ver_pedidos_cliente')
        else:
            mensaje = "No se puede cancelar el pedido"

    return render(request, 'detalle_pedido_cliente.html', {'pedido': pedido, 'mensaje': mensaje})
   





    





#************** Productos ******************
#   ************* CRUD *******************

@login_required (login_url='nopermiso')
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='nopermiso')
def productos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm()
    
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos, 'form': form})


@login_required (login_url='nopermiso')
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='nopermiso')
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(instance=producto)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')

    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})


@login_required (login_url='nopermiso')
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='nopermiso')
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        producto.delete()
        return redirect('productos')

    return render(request, {'producto': producto})
