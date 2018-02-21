# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import reverse
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponse
from tablib import Dataset

from .models import ContactInfo
from .forms import ContactInfoForm
from .resources import ContactInfoResource
# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@method_decorator(login_required(login_url='/'), name='dispatch')
class ContactInfoList(ListView):

	def get_queryset(self):
		return ContactInfo.objects.filter(created_by=self.request.user)
	#contact_info = ContactInfo.objects.filter(created_by=request.user)
	#return render(request,'contacts/home.html',{'contact_info':contact_info})

def redirecting(request):
	return redirect('view_home')

@method_decorator(login_required(login_url='/'), name='dispatch')
class ContactInfoCreate(CreateView):
	model = ContactInfo
	fields = ['first_name','last_name','contact_number','address']

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)
		
@method_decorator(login_required(login_url='/'), name='dispatch')
class ContactInfoUpdate(UpdateView):
	model = ContactInfo
	fields = ['first_name','last_name','contact_number','address']

@method_decorator(login_required(login_url='/'), name='dispatch')
class ContactInfoDelete(DeleteView):
	model = ContactInfo
	def get_success_url(self):
		return reverse('view_home')

def export(request):
    contacts_resource = ContactInfoResource()
    dataset = contacts_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
    return response

def simple_upload(request):
    if request.method == 'POST':
        contacts_resource = ContactInfoResource()
        dataset = Dataset()
        new_contacts = request.FILES['myfile']

        imported_data = dataset.load(new_contacts.read().decode('utf-8'))
                   
        contacts_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'contacts/import.html')
