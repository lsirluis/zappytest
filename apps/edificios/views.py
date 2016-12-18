from django.shortcuts import render, reverse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect ,HttpRequest
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages

from django.db.models import Q


from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.edificios.models import Propiedad, Unidad, Persona, Banco
from apps.usuarios.models import Administrador

from apps.edificios.forms import PropiedadForm,UnidadForm, BancoForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def index(request):
	return HttpResponse("Hola esta es la pagina de edificios")
@login_required()
def listar(request):
	uid = request.user.id
	usuario = User.objects.raw('SELECT * FROM auth_User where id=%s',([uid]))[0]
	propiedad = Propiedad.objects.filter(administrador=usuario.identificacion)

	contexto = {'propiedades': propiedad,'messages':["hola"],'title':"nuevotitulo"}
	# return render(request, 'Propiedad/Propiedad_List.html',contexto)
	return render(request, 'Propiedad/MisPropiedades.html',contexto)

def usuarioId(id): 
	uid = id
	usuario = User.objects.raw('SELECT * FROM auth_User where id=%s',([uid]))[0]
	return usuario


class listarList(ListView):
	paginate_by =9
	model = Propiedad
	# queryset = Propiedad.objects.filter(administrador=usuario)
	template_name = 'Propiedad/MisPropiedades.html'

	# def get_queryset(self):
		# uid = self.request.user.id
		# usuario = User.objects.raw('SELECT * FROM auth_User where id=%s',([uid]))[0]
		# usuario = usuarioId(self.request.user.id)
		# contexto = Propiedad.objects.filter(administrador=usuario.identificacion)

	def get_context_data(self, **kwargs):
		context = super(listarList, self).get_context_data(**kwargs)
		# usuario = usuarioId(self.request.user.id)
		# context['object_list'] = Propiedad.objects.filter(administrador=usuario.identificacion)
		uid = self.request.user.id
		# context['object_list'] = Propiedad.objects.filter(administrador__idu = uid)
		p = Paginator( Propiedad.objects.filter(administrador__idu = uid).order_by('-fecha_registro'), self.paginate_by)
		page = self.request.GET.get('page')
		try:
			context['object_list'] = p.page(page)
		except PageNotAnInteger:
        # If page is not an integer, deliver first page.
			context['object_list'] = p.page(1)
		except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
			context['object_list'] = p.page(p.num_pages)

		# context['object_list'] = p.page(context['page_obj'].number)
		context['title']="Mis Propiedades"
		
		return context
	# paginate_by = 1	
		# return contexto

@login_required()
def apartamentos(request,id_propiedad):
	# uid = request.user.id
	# usuario = User.objects.raw('SELECT * FROM auth_User where id=%s',([uid]))[0]

	# propiedades = Propiedad.objects.filter(administrador=usuario.identificacion)
	# apartamento = Unidad.objects.filter(propiedad_id=propiedades)
	# return HttpResponse(id_propiedad)
	# usuario=usuarioId(uid)
	uid = request.user.id
	url = {}
	apartamento=""
	nombre=""
	# mensaje = {}
	# messages.add_message(request, messages.INFO, 'Hello world.')
	if id_propiedad != "TOTALUNIDADES":
		# a=2
		# apartamento=Unidad.objects.filter(propiedad__identificacion=id_propiedad,propiedad__administrador=usuario.identificacion)
		# apartamento=Unidad.objects.filter(propiedad=id_propiedad,propiedad__administrador=usuario.identificacion)
		#si existe la propiedad 
		if Propiedad.objects.filter(administrador__idu = uid, idlegal=id_propiedad):
			url = Propiedad.objects.filter(idlegal=id_propiedad)[0]
			titulo = "Unidades en "+url.nombre
			apartamento=Unidad.objects.filter(propiedad__administrador__idu=uid, propiedad=id_propiedad)
			if apartamento :
				titulo = "Unidades en "+url.nombre
				nombre=url.nombre
				
			else:
			# titulo = "no hay unidades"
				messages.add_message(request, messages.ERROR, 'No tiene ningun Apartamento en esta propiedad')
		
		else:
			titulo = "No Existe esta propiedad"
			nombre = titulo
			messages.add_message(request, messages.ERROR, 'Lo sentimos, está Propiedad no esta registrada')


		

			# messages.warning(request, 'Your account expires in three days.')
		# apartamento = Unidad.objects.raw('SELECT * FROM auth_User, edificios_propiedad, edificios_unidad \
									  # WHERE auth_User.id=%s\
									  # and auth_User.identificacion = edificios_propiedad.administrador_id \
									  # and edificios_propiedad.identificacion = edificios_unidad.propiedad_id and edificios_unidad.propiedad_id = %s',[uid,id_propiedad])
	else:
		url['Imagen']= "/IMG/Propiedad/default_building_zappy.jpg"
		titulo = "Todas mis Unidades"
		apartamento=Unidad.objects.filter(propiedad__administrador__idu=uid)
		# apartamento = Unidad.objects.filter(propiedad__administrador=usuario.identificacion).order_by("propiedad__nombre","torre","numero")
		# apartamento = Unidad.objects.raw('SELECT * FROM auth_User, edificios_propiedad, edificios_unidad \
									  # WHERE auth_User.id=%s \
									  # and auth_User.identificacion = edificios_propiedad.administrador_id \
									  # and edificios_propiedad.identificacion = edificios_unidad.propiedad_id',[uid])
	# return HttpResponse(apartamento)



	contexto = {'apartamentos': apartamento,'title':titulo,'DatosPropiedad':url}
	if "Unidades en " in titulo :
		contexto['breadurl']=[{'nombre':'Propiedades','url':"Propiedad:Solicitud_listar"},\
								 {'nombre':nombre,'url':"Propiedad:Solicitud_apartamentos",'arg':id_propiedad}]	
	
	return render(request, 'Propiedad/MisApartamentos.html',contexto)


# vista para crear una nueva propiedad
class PropiedadCreate(CreateView):
	model = Propiedad
	form_class = PropiedadForm
	template_name = 'Propiedad/Propiedad_form.html'
	success_url = reverse_lazy('Propiedad:Solicitud_listar')
	def get_context_data(self, **kwargs):
		context = super(PropiedadCreate, self).get_context_data(**kwargs)
		context['title']= "Agregar Nueva Propiedad"
		return context
	#metodo post, aqui agregaremos el administrador 
	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		# quien es el administrador al que se le guardara? pues este:
		uid = request.user.id
		admin = Administrador.objects.get(idu=uid)
		form = self.form_class(request.POST)
		if form.is_valid() :
			solicitud = form.save(commit=False)
			solicitud.administrador = admin
			solicitud.save()		
			# form.administrador=1
			# form.save()			
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form))	

class PropiedadEdit(UpdateView):
	model = Propiedad
	form_class = PropiedadForm
	template_name = 'Propiedad/Propiedad_form.html'
	success_url = reverse_lazy('Propiedad:Solicitud_listar')
	# def get_initial(self):
	# 	self.initial.update({ 'requests': self.request})
	# 	return self.initial
	# filtraremos los datos para que no se pueda editar un banco que no nos pertenezca
	def get_context_data(self, **kwargs):
		context = super(PropiedadEdit, self).get_context_data(**kwargs)
		uid = self.request.user.id
		pk = self.kwargs.get('pk',0)
		if Propiedad.objects.filter(idlegal=pk, administrador=uid):
			return context
		else:
			messages.add_message(self.request, messages.ERROR, 'Lo sentimos, esta Propiedad no está registrada')
			# context = ""
			context['title']="Propiedad no registrada"
			return context


class UnidadCreate(CreateView):
	model = Unidad
	form_class = UnidadForm
	def get_initial(self):
		self.initial.update({ 'request': self.request})
		return self.initial
	def get_context_data(self, **kwargs):
		context = super(UnidadCreate, self).get_context_data(**kwargs)
		# usuario = usuarioId(self.request.user.id)
		# context['object_list'] = Propiedad.objects.filter(administrador=usuario.identificacion)
		uid = self.request.user.id
		self.propiedad = self.kwargs.get('id_propiedad',0)
		# qs = Propiedad.objects.filter(administrador__idu = uid, idlegal=propiedad)
		if(Propiedad.objects.filter(administrador__idu = uid, idlegal=self.propiedad)):
			qs = Propiedad.objects.filter(administrador__idu = uid, idlegal=self.propiedad)[0]
		else:
			qs=""
			messages.add_message(self.request, messages.ERROR, 'Lo sentimos, está Propiedad no esta registrada')

		context['object_list'] = qs
		context['title'] = "Crear Unidad en - "+qs.nombre

		return context
	# def post(self, request, *args, **kwargs):
		# self.object = self.get_object
		# context = super(UnidadCreate, self).get_context_data(**kwargs)
	# 	uid = request.user.id
	# 	propiedad = self.kwargs.get('id_propiedad',0)
	# 	if(Propiedad.objects.filter(administrador__idu = uid, idlegal=propiedad)):
	
	# 	else:
	# 		return self.render_to_response(self.get_context_data(form=form))	
	# 	# quien es el administrador al que se le guardara? pues este:
	# 	admin = Administrador.objects.get(idu=uid)
		# form = self.form_class(request.POST)
		# if form.is_valid() :

			# solicitud = form.save(commit=False)
			# solicitud.administrador = admin
			# solicitud.save()		
			# form.administrador=1
			# form.save()			
			# return HttpResponseRedirect(reverse('Propiedad:Solicitud_apartamentos', args=["mont"]))
		# else:
			# return self.render_to_response(self.get_context_data(form=form))	



	template_name = 'Propiedad/Unidad_form.html'
	success_url = reverse_lazy('Propiedad:Solicitud_listar')
# reverse('arch-summary', args=[1945])
class BancoCreate(CreateView):
	model = Banco
	form_class = BancoForm
	template_name = 'Propiedad/Banco_form.html'
	success_url = reverse_lazy('Propiedad:Solicitud_listarBanco')

	def get_initial(self):
		self.initial.update({ 'requests': self.request})
		return self.initial

	def get_context_data(self, **kwargs):
		context = super(BancoCreate, self).get_context_data(**kwargs)
		uid = self.request.user.id
		context['administrador'] = uid
		context['title'] = "Crear Banco "
		return context


	# def post(self, request, *args, **kwargs):
	# 	self.object = self.get_object
	# 	# quien es el administrador al que se le guardara? pues este:
	# 	# initial.update({ 'request': self.request})
	# 	# return self.initial
	# 	# initial= self.initial
	# 	# initial.update({ 'requests': self.request})
	# 	kwargs.update({'initial':{'requests': self.request}})
	# 	uid = request.user.id
	# 	admin = Administrador.objects.get(idu=uid)
	# 	form['initial']='h'

	# 	if form.is_valid("hola") :
	# 		solicitud = form.save(commit=False)
	# 		solicitud.administrador = admin
	# 		solicitud.save()		
	# 		# form.administrador=1
	# 		# form.save()			
	# 		return HttpResponseRedirect(self.get_success_url())
	# 	else:
	# 		return self.render_to_response(self.get_context_data(form=form))	


class BancoList(ListView):
	model = Banco
	template_name = 'Propiedad/MisBancos.html'	
	def get_context_data(self, **kwargs):
		context = super(BancoList, self).get_context_data(**kwargs)
		uid = self.request.user.id
		context['object_list']= Banco.objects.filter(administrador = uid)
		context['title']= "Mis Bancos"
		return context
class BancoEdit(UpdateView):
	model = Banco
	form_class = BancoForm
	template_name = 'Propiedad/Banco_form.html'
	success_url = reverse_lazy('Propiedad:Solicitud_listarBanco')
	def get_initial(self):
		self.initial.update({ 'requests': self.request})
		return self.initial
	# filtraremos los datos para que no se pueda editar un banco que no nos pertenezca
	def get_context_data(self, **kwargs):
		context = super(BancoEdit, self).get_context_data(**kwargs)
		uid = self.request.user.id
		pk = self.kwargs.get('pk',0)
		if Banco.objects.filter(id=pk, administrador=uid):
			return context
		else:
			messages.add_message(self.request, messages.ERROR, 'Lo sentimos, este Banco no está registrado')
			# context = ""
			context['title']="Banco no registrado"
			return context

