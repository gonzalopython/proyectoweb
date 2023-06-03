from django import forms
from django.contrib.auth.models import User
from .models import Producto
from .models import User

class RegistroForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'  # Utiliza todos los campos del modelo Producto


        