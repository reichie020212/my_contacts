# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator
from django.shortcuts import reverse
from django.contrib.auth.models import User

from django.db import models

# Create your models here.

class ContactInfo(models.Model):
	numeric = RegexValidator(r'^[0-9]*$','Only numbers are allowed.')
	
	created_by = models.ForeignKey('auth.User')
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	contact_number = models.CharField(max_length=15,
	                                  validators=[numeric]) #upon searching, longest contact number in the world is 15 digits
	address = models.CharField(max_length=150)

	def __str__(self):
		return self.last_name

	def get_absolute_url(self):
		return reverse('view_home')