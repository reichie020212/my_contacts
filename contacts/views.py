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
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from tablib import Dataset
import csv
import shutil
import os

from .models import ContactInfo
from .forms import ContactInfoForm
from .resources import ContactInfoResource, ExportResource
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

def redirecting(request):
	return redirect('view_home')

@method_decorator(login_required(login_url='/'), name='dispatch')
class ContactInfoCreate(CreateView):
    #template_name = "contacts/createview.html"
    model = ContactInfo
    fields = (['first_name',
        'last_name',
        'contact_number',
        'address'])

    def get_success_url(self):
        return reverse('view_home')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
        setattr(request, 'view', 'views.create')

@method_decorator(login_required(login_url='/'), name='dispatch')
class ContactInfoUpdate(UpdateView):
    model = ContactInfo
    fields = (['first_name',
        'last_name',
        'contact_number',
        'address'])

    def get_success_url(self):
        return reverse('view_home')
        setattr(request, 'view', 'views.update')

@method_decorator(login_required(login_url='/'), name='dispatch')
class ContactInfoDelete(DeleteView):
	model = ContactInfo
	def get_success_url(self):
		return reverse('view_home')

def export(request):
    contacts_resource = ExportResource()
    dataset = contacts_resource.export()
    
    #convert Dataset to List
    my_list = []
    for i in dataset:
        my_list.append(list(i))

    #Replace blank to the ID of the user
    count = 0
    for x in my_list:
        my_list[count][0] = request.user
        count = count+1

    #creating new dataset then add Headers
    my_data = Dataset()
    my_data.headers = (['created_by',
        'first_name',
        'last_name',
        'contact_number',
        'address'])

    for x in my_list:
        my_data.append(x)

    response = HttpResponse(my_data.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
    return response


def simple_upload(request):
    if request.method == 'POST':
        contacts_resource = ContactInfoResource()
        contacts = ContactInfo.objects.filter(first_name="Redick")
        print(contacts)
        dataset = Dataset()
        new_contacts = request.FILES['myfile']

        dataset.load(new_contacts.read().decode('utf-8'))

        #convert Dataset to List
        my_list = []
        for i in dataset:
            my_list.append(list(i))

        #Replace blank to the ID of the user
        count = 0
        for x in my_list:
            my_list[count][5] = request.user.id
            count = count+1

        #creating new dataset then add Headers
        my_data = Dataset()
        my_data.headers = (['id',
            'first_name',
            'last_name',
            'contact_number',
            'address',
            'created_by'])

        #Append list to new dataset
        for x in my_list:
            my_data.append(x)

        contacts_resource.import_data(my_data, dry_run=False)  # Actually import now
        
    return render(request, 'contacts/import.html')