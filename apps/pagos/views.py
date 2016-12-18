from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.pagos.models import Recibo , Detalle
from apps.edificios.models import Unidad, Propiedad
from django.contrib import messages

# Create your views here.
def ReciboLists(request, id_propiedad, pk):

	contexto = {'propiedades': "hola",'messages':["hola"],'title':"nuevotitulo"}
	# return render(request, 'Propiedad/Propiedad_List.html',contexto)
	return render(request, 'Pagos/Factura_list.html',contexto)


class ReciboList(ListView):
	model = Recibo
	template_name = 'Pagos/Factura_list.html'	
	def get_context_data(self, *args,**kwargs):
		context = super(ReciboList, self).get_context_data(*args,**kwargs)
		uid = self.request.user.id
		idpro = self.kwargs.get('id_propiedad',0)
		pkunidad= self.kwargs.get('pk',0)
		if (Recibo.objects.filter(unidad=pkunidad,unidad__propiedad=idpro, unidad__propiedad__administrador__idu = uid)) and (Unidad.objects.filter(id=pkunidad, propiedad=idpro, propiedad__administrador=uid)[0]):
			context['object_list']= Recibo.objects.filter(unidad=pkunidad,unidad__propiedad=idpro, unidad__propiedad__administrador__idu = uid)
			context['DatosUnidad']= Unidad.objects.filter(id=pkunidad, propiedad=idpro, propiedad__administrador=uid)[0]	
			context['title']= ("Historial Pagos en la Torre : "+(context['DatosUnidad'].torre)+" - Apto : "+(str(context['DatosUnidad'].numero))+"")
			context['breadurl']=[{'nombre':'Propiedades','url':"Propiedad:Solicitud_listar"},\
								 {'nombre':context['DatosUnidad'].propiedad.nombre,'url':"Propiedad:Solicitud_apartamentos",'arg':context['DatosUnidad'].propiedad.idlegal},{'nombre':context['title'],'url':"j"}]
		else:
			context['title']= "Unidad o Propiedad no encontrada"
			messages.add_message(self.request, messages.ERROR, 'Lo sentimos, esta Unidad no esta Registrada')


		context['variable1']=idpro
		context['variable2']=pkunidad
		return context

class DetalleFactura(ListView):
	model = Detalle
	template_name = 'Pagos/DetalleFactura.html'
	def get_context_data(self, *args,**kwargs):
		context = super(DetalleFactura, self).get_context_data(*args,**kwargs)
		uid = self.request.user.id
		idpro = self.kwargs.get('id_propiedad',0)
		pkunidad= self.kwargs.get('pk',0)
		factura = self.kwargs.get('factura',0)
		# realizamos la consulta para obtener el detalle de la factura
		qs= Detalle.objects.filter(idRecibo__unidad__propiedad__administrador=uid, idRecibo= factura, idRecibo__unidad=pkunidad, idRecibo__unidad__propiedad = idpro)
		context['object_list']= qs
		context['DatosUnidad']= Unidad.objects.filter(id=pkunidad, propiedad=idpro, propiedad__administrador=uid)[0]	
		if not qs :
			messages.add_message(self.request, messages.ERROR, 'Lo Sentimos no hay detalles para esta factura')
		context['title'] = "Detalle de Factura"
		aux = ("Historial Pagos en la Torre : "+(context['DatosUnidad'].torre)+" - Apto : "+(str(context['DatosUnidad'].numero))+"")
		context['breadurl']=[{'nombre':'Propiedades','url':"Propiedad:Solicitud_listar"},\
							 {'nombre':context['DatosUnidad'].propiedad.nombre,'url':"Propiedad:Solicitud_apartamentos",'arg':context['DatosUnidad'].propiedad.idlegal},\
							 {'nombre':aux,'url':"Propiedad:Solicitud_appagos",'arg':context['DatosUnidad'].propiedad.idlegal,'arg2':context['DatosUnidad'].id},\
							 {'nombre':context['title']}]

		return context