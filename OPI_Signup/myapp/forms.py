from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import OPIForm, SLATForm
from datetime import datetime, date, time, timedelta
from calendar import TUESDAY

class SLATForm_Forms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        today = date.today()
        model = SLATForm

        fields = ('firstname', 'lastname', 'byuid', 'language', 'thesis',
                'transcript', 'opi')
        labels = {
            'firstname':'', 'lastname':'', 'byuid':'', 'language':'', 'thesis':'',
                'transcript':'', 'opi':''
        }
        widgets = {
            'firstname': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'First Name', 'name':'firstname'}),
            'lastname': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Last Name', 'name':'lastname'}),
            'byuid': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'BYU ID','minlength': '9', 'name':'byuid' }),
            'language': forms.Select(attrs={'class':'formbox, input-class','placeholder': '', 'name':'language'}),
            'thesis' : forms.DateInput(attrs={'type': 'date', 'class': 'formbox, input-class', 'min': today, 'name':'thesis'}),
            'transcript' : forms.ClearableFileInput(attrs={'type':'file', 'class':'formbox, input-class, file-input','id':'transcript', 'name':'transcript'}),
            'opi' : forms.ClearableFileInput(attrs={'type':'file', 'class':'formbox, input-class, file-input', 'id':'opi', 'name':'opi'}),
        }
        
class OPIForm_Forms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['agree'].required = True
        self.fields['language_other'].required = False
        self.fields['cannot_come'].required = False
        self.fields['reason_other'].required = False

    class Meta:

        today = date.today()
        min_days = today + timedelta(days=2)
        two_weeks = today + timedelta(days=14)
        model = OPIForm

        fields = ('agree', 'firstname', 'lastname', 'byuid', 'netid',
        'email', 'reason', 'reason_other', 'language',
        'language_other', 'experience', 'major', 'second_major',
        'minor', 'scores', 'come_to_campus',
        'cannot_come', 'testdate1', 'time1', 'time2',
        'testdate2', 'time3', 'time4', 'confirm_email', 'phone')
        labels = {
        'agree':'*I agree to the OPI Assessment Agreement as defined above.', 'firstname':'', 'lastname': "", 'byuid': "", 'netid': "",
        'email': "", 'reason': "", 'reason_other':"", 'language':"",
        'language_other': "", 'experience': "", 'major': "", 'second_major': "",
        'minor': "", 'scores':"", 'come_to_campus':"",
        'cannot_come': "", 'testdate1': "", 'time1': '', 'time2': "",
        'testdate2': "", 'time3':"", 'time4':"", 'confirm_email': "", 'phone':""
        }
        
        widgets = {
            'agree': forms.CheckboxInput(attrs={'class':'formbox, agree', 'name':'agree'}),
            'firstname': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'First Name', 'name':'firstname'}),
            'lastname': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Last Name', 'name':'lastname'}),
            'byuid': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'BYU ID','minlength': '9', 'name':'byuid' }),
            'netid': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': "BYU Net ID", 'name':'netid'}),
            'email': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Email', 'name':'email'}),
            'reason': forms.Select(attrs={'class':'fopythormbox, input-class', 'placeholder': '', 'name':'reason'}),
            'reason_other': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Category', 'name':'reason_other'}),
            'language': forms.Select(attrs={'class':'formbox, input-class','placeholder': '', 'name':'language'}),
            'language_other' : forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': '', 'name':'language_other', 'required':'False'}),
            'experience': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': '', 'name':'experience'}),
            'major' : forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Major', 'name':'major'}),
            'second_major' : forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Second Major', 'name':'second_major'}),
            'minor' : forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Minor', 'name':'minor'}),
            'scores': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': '', 'name':'scores'}),
            'come_to_campus': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': '', 'name':'come_to_campus'}),
            'cannot_come': forms.Select(attrs={'class':'formbox, input-class', 'placeholder': '', 'name':'cannot_come', 'required':'False'}),
            'testdate1' : forms.DateInput(attrs={'type': 'date', 'class': 'formbox, input-class', 'min': min_days, 'name':'testdate1'}),
            'time1': forms.TimeInput(attrs={'class':'formbox, input-class', 'type': 'time', 'min' : '08:00', 'max' : '17:00', 'step' : '900', 'autocomplete': 'on', 'value': '12:00', 'name':'time1'}),
            'time2': forms.TimeInput(attrs={'class':'formbox, input-class', 'type': 'time', 'min' : '08:00', 'max' : '17:00', 'step' : '900', 'autocomplete': 'on', 'value': '15:00', 'name':'time2'}),
            'testdate2': forms.DateInput(attrs={'type': 'date','class':'formbox, input-class', 'min': two_weeks, 'name':'testdate2'}),
            'time3': forms.TimeInput(attrs={'class':'formbox, input-class', 'type': 'time', 'min' : '08:00', 'max' : '17:00', 'step' : '900', 'autocomplete': 'on', 'value': '12:00', 'name':'time3'}),
            'time4': forms.TimeInput(attrs={'class':'formbox, input-class', 'type': 'time', 'min' : '08:00', 'max' : '17:00', 'step' : '900', 'autocomplete': 'on', 'value': '15:00', 'name':'time4'}),
            'confirm_email': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Email', 'name':'confirm_email'}),
            'phone': forms.TextInput(attrs={'class':'formbox, input-class', 'placeholder': 'Phone Number', 'name':'phone'}),
      
        }