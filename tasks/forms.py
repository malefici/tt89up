from urllib.parse import urlparse

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


class CommaSeparatedCharField(forms.Field):
    def to_python(self, value):
        if not value:
            return []
        return list(set([item.strip() for item in value.split(',') if item.strip()]))

    def validate(self, value):
        super().validate(value)
        v = URLValidator()
        for url in value:
            v(url)
            if urlparse(url).hostname != 'petition.parliament.uk':
                raise ValidationError('URL "{}" invalid. It should be only for "petition.parliament.uk"'.format(url))


class CreateTaskBundleForm(forms.Form):
    urls = CommaSeparatedCharField(widget=forms.Textarea)
