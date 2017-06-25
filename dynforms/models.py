import json

from django.contrib.postgres.fields import JSONField
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

    def languages_tuples(self):
        return [(lang.code, lang.name) for lang in self.languages.all()]

    def fields(self):
        return json.dumps([field.as_dict() for field in self.formfield_set.all()])

    @property
    def submission_count(self):
        return len(self.formsubmission_set.all())


class FormField(models.Model):
    field_type = models.CharField(max_length=20)
    field_label = models.CharField(max_length=100)
    field_placeholder = models.CharField(max_length=500, null=True)
    field_required = models.BooleanField()
    form = models.ForeignKey(FormModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def as_dict(self):
        return {
            'id': self.id,
            'type': self.field_type,
            'label': self.field_label,
            'placeholder': self.field_placeholder,
            'required': self.field_required
        }


class TextTranslation(models.Model):
    text = models.CharField(max_length=1000)
    translated = models.CharField(max_length=1000, null=True)
    language = models.ForeignKey(Language)

    @classmethod
    def get_translation_for_text_and_lang(cls, text, language):
        if language is None:
            return text
        translation = cls.objects.filter(text=text, language=language).first()
        return translation.translated if translation is not None else text


class FormSubmission(models.Model):
    form = models.ForeignKey(FormModel, on_delete=models.CASCADE)
    submission_data = JSONField()
