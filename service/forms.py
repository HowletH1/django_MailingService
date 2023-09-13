import datetime

from django import forms
from service import models


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ('name', 'email', 'comment')


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ('title', 'body')


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = models.Mailing
        fields = ('date', 'time', 'frequency', 'clients', 'message')

    # def clean(self):
    #    cleaned_data = super().clean()
    #    if datetime.datetime.now() > datetime.datetime.combine(self.cleaned_data['date'], self.cleaned_data['time']):
    #       self.cleaned_data['date'] = datetime.datetime.now().date()
    #        self.cleaned_data['time'] = datetime.datetime.now().time().replace(microsecond=0)
    #    return cleaned_data


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = models.Blog
        fields = ('title', 'content', 'preview', 'published')
