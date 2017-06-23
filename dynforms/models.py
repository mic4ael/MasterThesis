from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)


class FormModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    languages = models.ManyToManyField(Language, related_name='+')
    max_submissions = models.PositiveIntegerField(default=0)

    def languages_names(self):
        return [lang.name for lang in self.languages.all()]

