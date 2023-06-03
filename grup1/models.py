from django.db import models
from django.contrib.auth.models import User


# Create your models here.



class Producto(models.Model):
    nombre = models.CharField(max_length=45)
    precio = models.IntegerField()
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='img/', blank=True, null=True)
    

    def __str__(self):
        return f'ID: {self.id} Nombre : {self.nombre}'


class Estado(models.Model):
    idestado = models.IntegerField(primary_key=True)
    estado = models.CharField(max_length=15)
    
    def __str__(self):
        return f'ID: {self.idestado} Nombre : {self.estado}' #Asignamos el ID y nombre de Estado para mostrar en Panel Admin

class Pedido(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedido_vendedor')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedido_cliente')
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=100)
    observaciones = models.TextField()
    

    def __str__(self):
       return f'ID: {self.id} Cliente: {self.cliente} Estado: {self.estado.idestado} {self.estado.estado}'
    
class Detalle(models.Model):
    idpedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    idproducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.IntegerField()

    def __str__(self):
        return f'ID: {self.idpedido_id} Producto: {self.idproducto.nombre} Cantidad: {self.cantidad} Precio:{self.precio}'

class Etiqueta(models.Model):
    # Define los campos del modelo aquí
    nombre = models.CharField(max_length=50)
    # Otros campos opcionales
    # ...

    def __str__(self):
        return self.nombre
    



