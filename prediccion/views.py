from django.shortcuts import render
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from .forms import RegistroVentaForm, CustomUserCreationForm, EntrenarRedForm, ServicioForm
from django.views.generic import ListView
from django.views.generic import TemplateView

from bootstrap_modal_forms.generic import (BSModalLoginView,
                                           BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalReadView,
                                           BSModalDeleteView)

from .models import RedNeuronalResultados, RegistroVenta, Servicio

# User manage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy

from .func import train_nn, populate_days, get_weeks, get_months, get_nn_tipos
from multiprocessing import Pool

@method_decorator(login_required, name='dispatch')
class VentasPronostico(TemplateView):
    template_name = "ventas_pronostico.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = self.kwargs['periodo']
        queryset = RedNeuronalResultados.objects.filter(periodo=periodo, clasificacion='GENERAL').order_by('-id')[:1]
        context['objects'] = queryset
        return context

@method_decorator(login_required, name='dispatch')
class PronosticoCompra(TemplateView):
    template_name = "pronostico_compra.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = self.kwargs['periodo']
        queryset = RedNeuronalResultados.objects.filter(periodo=periodo, clasificacion='GENERAL').order_by('-id')[:1]
        context['objects'] = queryset
        return context

@method_decorator(login_required, name='dispatch')
class PronosticoGeneral(TemplateView):
    template_name = "pronostico_general.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = self.kwargs['periodo']
        clasificacion = self.kwargs['clasificacion']
        queryset = RedNeuronalResultados.objects.filter(periodo=periodo, clasificacion=clasificacion).order_by('-id')[:1]
        queryset2 = Servicio.objects.all()
        context['periodo_anterior'] = periodo
        context['clasificacion_anterior'] = clasificacion
        context['objects'] = queryset
        context['servicios'] = queryset2
        return context

@method_decorator(login_required, name='dispatch')
class ErrorPronostico(TemplateView):
    template_name = "error_pronostico.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        periodo = self.kwargs['periodo']
        queryset = RedNeuronalResultados.objects.filter(periodo=periodo, clasificacion='GENERAL').order_by('-id')[:1]
        context['objects'] = queryset
        return context

@method_decorator(login_required, name='dispatch')
class RegistroVentaView(CreateView):
    template_name = 'registro_venta.html'
    form_class = RegistroVentaForm

    def get_success_url(self):
        return reverse_lazy('registro_venta')


@method_decorator(login_required, name='dispatch')
class ServicioView(CreateView):
    template_name = 'servicio.html'
    form_class = ServicioForm

    def get_success_url(self):
        return reverse_lazy('servicio')
        

@method_decorator(login_required, name='dispatch')
class ServicioUpdateView(UpdateView):
    template_name = 'servicio_update.html'
    form_class = ServicioForm

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Servicio.objects.filter(id=pk)
        return queryset
    
    def get_success_url(self):
        return reverse_lazy('servicios')

@method_decorator(login_required, name='dispatch')
class ServicioDeleteView(DeleteView):
    model = Servicio
    succes_url = reverse_lazy('servicios')

@method_decorator(login_required, name='dispatch')
class ServiciosView(TemplateView):
    template_name = "servicios.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Servicio.objects.all()
        context['objects'] = queryset
        return context

@method_decorator(login_required, name='dispatch')
class VentasView(TemplateView):
    template_name = "ventas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = RegistroVenta.objects.all()
        context['objects'] = queryset
        return context
        

@method_decorator(login_required, name='dispatch')
class VentaUpdateView(UpdateView):
    template_name = 'venta_update.html'
    form_class = RegistroVentaForm

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = RegistroVenta.objects.filter(id=pk)
        return queryset
    
    def get_success_url(self):
        return reverse_lazy('ventas')

@method_decorator(login_required, name='dispatch')
class VentaDeleteView(DeleteView):
    model = RegistroVenta
    succes_url = reverse_lazy('ventas')

@method_decorator(login_required, name='dispatch')
class EntrenarRedView(CreateView):
    template_name = 'entrenar_red.html'
    form_class = EntrenarRedForm

    def form_valid(self, form):
        periodo = form.cleaned_data['periodo']
        look_back = form.cleaned_data['look_back']
        neuronas = form.cleaned_data['neuronas']
        epocas = form.cleaned_data['epocas']
        clasificacion = form.cleaned_data['clasificacion']
        data_date = []
        data_price = []
        data_type = []

        if clasificacion=='GENERAL':
            ventas = RegistroVenta.objects.all().order_by('fecha')
            clasificacion = "VENTAS"
        else:
            ventas = RegistroVenta.objects.filter(tipo=clasificacion).order_by('fecha')

        for i in ventas:
            data_date.append(i.fecha)
            data_price.append(i.precio)
            data_type.append(i.tipo)

        #if clasificacion == "PRECIOS":
        if periodo == 'DIAS':
            data = populate_days(data_date, data_price)
            future = data[2]
            
        if periodo == 'SEMANAS':
            data = populate_days(data_date, data_price)
            future = get_weeks(data[2], data[1])[0]
            data = get_weeks(data[0], data[1])

        if periodo == 'MESES':
            data = populate_days(data_date, data_price)
            future = get_months(data[2], data[1])[0]
            data = get_months(data[0], data[1])
        #else:
        #   data = get_nn_tipos(data_date, data_type)
 
        pool = Pool(processes=1)   
        rmse, dam, pema, eval_dir, pred_dir, dam_dir, pema_dir, rmse_dir = pool.apply(train_nn, [data[1], data[0], look_back, neuronas, epocas, periodo, clasificacion, future])


        form.instance.dam = dam
        form.instance.rmse = rmse
        form.instance.pema = pema
        form.instance.eval_dir = eval_dir
        form.instance.pred_dir = pred_dir
        form.instance.dam_dir = dam_dir
        form.instance.pema_dir = pema_dir
        form.instance.rmse_dir = rmse_dir

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('entrenar_red')


# Vistors register (Sign up)


class UserCreateView(BSModalCreateView):
    template_name = "registration/create_user.html"
    form_class = CustomUserCreationForm
    success_message = 'Éxito: La cuenta fue creada.'

    def get_success_url(self, **kwargs):
        return reverse_lazy('login')

@method_decorator(login_required, name='dispatch')
class UserUpdateView(BSModalUpdateView):
    model = User
    template_name = 'registration/update.html'
    form_class = CustomUserCreationForm
    success_message = 'Éxito: La cuenta fue editada.'

    def get_success_url(self, **kwargs):
        return reverse_lazy('login')

@method_decorator(login_required, name='dispatch')
class UserDeleteView(BSModalDeleteView):
    model = User
    template_name = 'registration/delete.html'
    success_message = 'Éxito: La cuenta fue eliminada.'

    def get_success_url(self, **kwargs):
        return reverse_lazy('login')




