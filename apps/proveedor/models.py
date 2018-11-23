from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_categoria

class Puesto(models.Model):
    nombre_puesto = models.CharField(max_length=50)
    representante_puesto = models.CharField(max_length=50)
    ubicacion_puesto = models.CharField(max_length=50)
    categoria_puesto = models.ManyToManyField(Categoria)

    def __str__(self):
        return self.nombre_puesto

class Proveedor(models.Model):
	codigo_proveedor = models.CharField(max_length=20)
	nombre_proveedor = models.CharField(max_length=50)
	categoria_proveedor = models.ManyToManyField(Categoria)
	puesto_proveedor = models.ManyToManyField(Puesto)
	estado_control = models.BooleanField(default=False)

	def __str__(self):
		return self.nombre_proveedor

class Control(models.Model):
	fecha_entrada = models.DateField(blank=True, null=True)
	fecha_salida = models.DateField(blank=True, null=True)
	hora_entrada = models.TimeField(blank=True, null=True)
	hora_salida = models.TimeField(blank=True, null=True)
	control = models.BooleanField(default=True)
	proveedor = models.ForeignKey (Proveedor, null = True , blank = True , on_delete = models.CASCADE)
	


