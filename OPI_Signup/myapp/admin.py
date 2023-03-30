from django.contrib import admin
from django.shortcuts import render
from .models import OPIForm, Languages, Reasons
from .forms import OPIForm_Forms
import myapp.filemaker_api.filemaker_api as filemaker
import myapp.box_api.box_api as box
import pandas as pd


class LanguagesAdmin(admin.ModelAdmin):
    model = Languages
    def save_model(self, request, obj, form, change):        
        client = box.create_client()

        super().save_model(request, obj, form, change)

        box.add_delete_language_form_box(client)
                
        return obj.full_language
    def delete_model(self, request, obj):

        obj.delete()
        client = box.create_client()
        box.add_delete_language_form_box(client)
    
admin.site.register(Languages, LanguagesAdmin)


# mariah saves object
# pull csv from box into temp folder
# erase everything in csv
# for object add to csv
# upload back to box
# delete tmp item

