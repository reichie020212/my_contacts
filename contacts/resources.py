from import_export import resources
from .models import ContactInfo

class ContactInfoResource(resources.ModelResource):
    class Meta:
        model = ContactInfo