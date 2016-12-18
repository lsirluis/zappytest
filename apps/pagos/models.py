from django.db import models
from apps.edificios.models import Unidad
# Create your models here.
class Recibo(models.Model):

	id = models.AutoField(primary_key=True)
	unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
	estado = models.PositiveIntegerField(null=False, blank=False)
	descripcion = models.CharField(max_length = 120, null=True, blank=True)
	numConsecutivo= models.IntegerField()
	fecha_generacion = models.DateTimeField(auto_now=True)
	fecha_cobrada = models.DateTimeField()
	class Meta:
		verbose_name='Recibo'
		verbose_name_plural='Recibos'
	def __str__(self): #forma 2
		return '{}-{}'.format(self.unidad,self.fecha_cobrada)	

class Detalle(models.Model):
	id = models.AutoField(primary_key=True)
	idRecibo = models.ForeignKey(Recibo, on_delete= models.CASCADE)
	valor = models.BigIntegerField(blank=False, null=False)
	tipo = models.CharField(max_length= 100)
	descripcion = models.CharField(max_length = 120)
	class Meta:
		verbose_name='Detalle'
		verbose_name_plural='Detalles'
	def __str__(self): #forma 2
		return '{}-{}'.format(self.tipo,self.valor)	