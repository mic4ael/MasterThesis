from django.db import models


# class Form(models.Model):
#     pass


# class BaseFormField(models.Model):
#     pass


# class FormFieldAnswer(models.Model):
#     pass


class Language(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
