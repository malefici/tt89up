from urllib.parse import urlparse

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


class CommaSeparatedCharField(forms.Field):
    """
    Custom field for comma separated links for petitions site only.
    """
    def to_python(self, value):
        if not value:
            return []
        return list(set([item.strip() for item in value.split(',') if item.strip()]))

    def validate(self, value):
        super().validate(value)
        v = URLValidator()
        for url in value:
            v(url)  # it's must be url...
            if urlparse(url).hostname != 'petition.parliament.uk':  # ...from petitions site
                raise ValidationError('URL "{}" invalid. It should be only for "petition.parliament.uk"'.format(url))


class CreateTaskBundleForm(forms.Form):
    """
    Very simple form for parsing URLs.
    """
    urls = CommaSeparatedCharField(widget=forms.Textarea)
