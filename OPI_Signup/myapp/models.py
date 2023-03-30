from django.db import models
import myapp.model_choices as mc
from django import forms
from django.contrib.auth.models import User
import subprocess


class Languages(models.Model):
    full_language = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Languages"
    def __str__(self):
        return self.full_language

class Reasons(models.Model):
    reason = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Reasons"
    def __str__(self):
        return '{}'.format(self.reason)

class SLATForm(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    byuid = models.CharField(max_length=9)
    language = models.CharField(max_length=100, choices= mc.slat.languages, default='')
    thesis = models.DateField()
    transcript = models.FileField()
    opi = models.FileField()


class OPIForm(models.Model):
    
    agree = models.BooleanField()
    entry_date = models.DateField(auto_now_add=True)
    entry_time = models.TimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    byuid = models.CharField(max_length=9)
    netid = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    reason = models.CharField(max_length=100, choices= mc.choices.reasons, default='')
    reason_other = models.CharField(max_length=100)
    language = models.CharField(max_length=100, choices=mc.choices.languages, default='')
    #language = models.ForeignKey('AvailableLanguages', on_delete=models.CASCADE)
    language_other = models.CharField(max_length=100)
    experience = models.CharField(max_length=100, choices= mc.choices.language_background, default='')
    major = models.CharField(max_length=100)
    second_major = models.CharField(max_length=100)
    minor = models.CharField(max_length=100)
    scores = models.CharField(choices= mc.choices.yes_no, max_length=10)
    come_to_campus = models.CharField(choices= mc.choices.yes_no, max_length=10)
    cannot_come = models.CharField(choices= mc.choices.cannot_come_choice, max_length=100)
    testdate1 = models.DateField(max_length=100)
    time1 = models.TimeField()
    time2 = models.TimeField()
    testdate2 = models.DateField(max_length=100)
    time3 = models.TimeField()
    time4 = models.TimeField()
    confirm_email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)

    #This is how the objects display on the admin frontend
    def __str__(self):
        return '{} {} {} {}'.format(self.firstname, self.lastname, self.entry_date, self.entry_time)

# class OPI_Signin(models.Model):
#     password = models.CharField(max_length=6)

