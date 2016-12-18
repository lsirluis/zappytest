from django.conf.urls import url

from apps.edificios.views import index, listarList, apartamentos, listar \
                               , PropiedadCreate, UnidadCreate, BancoCreate\
                               , BancoList, BancoEdit \
                               , PropiedadEdit
from apps.pagos.views import ReciboList, DetalleFactura
urlpatterns = [

    url(r'^$', index), #mostrara el mensaje
    # url(r'^algo$', index), #otra forma, ejemplo adopcion/algo

    # url(r'^listar/$', listar, name = 'Solicitud_listar'),#listara los administradores
    url(r'^crear/$', PropiedadCreate.as_view(), name = 'Solicitud_crearpro'),#listara los administradores
    url(r'^listar/$', listarList.as_view(), name = 'Solicitud_listar'),#listara los administradores
    url(r'^edit/(?P<pk>[A-Za-z0-9-_]+)$', PropiedadEdit.as_view(), name = 'Solicitud_updatePro'),#listara los administradores

    url(r'^listar/unidad/(?P<id_propiedad>[A-Za-z0-9-_]+)/crear/$', UnidadCreate.as_view(), name = 'Solicitud_crearuni'),#listara los administradores
    url(r'^bancos/crear$', BancoCreate.as_view(), name = 'Solicitud_crearBanco'),#listara los administradores
    url(r'^bancos/listar$', BancoList.as_view(), name = 'Solicitud_listarBanco'),#listara los administradores
    url(r'^bancos/edit/(?P<pk>\d+)$', BancoEdit.as_view(), name = 'Solicitud_updateBanco'),#listara los administradores

    # url(r'^solicitud/nuevo$', SolicitudCreate.as_view(), name = 'Solicitud_crear'),
    # url(r'^solicitud/editar/(?P<pk>\d+)$', SolicitudUpdate.as_view(), name = 'Solicitud_editar'),
    # url(r'^solicitud/eliminar/(?P<pk>\d+)$', SolicitudDelete.as_view(), name = 'Solicitud_eliminar'),
    # url(r'^apartamentos$', apartamentos, name = 'Solicitud_apartamentos'),#listara los administradores
    # url(r'^listar/(?P<id_propiedad>\w+)/$', apartamentos, name = 'Solicitud_apartamentos'),#listara los administradores
    # url(r'^unidades/$', apartamentos, name = 'Solicitud_apartamentos'),#listara los administradores
    url(r'^listar/unidades/(?P<id_propiedad>[A-Za-z0-9-_]+)/$', apartamentos, name = 'Solicitud_apartamentos'),#listara los administradores
    url(r'^listar/unidades/(?P<id_propiedad>[A-Za-z0-9-_]+)/(?P<pk>[A-Za-z0-9-_]+)/pagos$', ReciboList.as_view(), name = 'Solicitud_appagos'),#listara los administradores
    url(r'^listar/unidades/(?P<id_propiedad>[A-Za-z0-9-_]+)/(?P<pk>[A-Za-z0-9-_]+)/detallefactura/(?P<factura>[A-Za-z0-9-_]+)/$', DetalleFactura.as_view(), name = 'Solicitud_pagosdetalle'),#listara los administradores

    # url(r'^editar/(?P<pk>\d+)/$', MascotaUpdate.as_view() , name ='mascota_editar'),

]
