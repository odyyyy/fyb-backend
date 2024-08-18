from django import forms
from django.contrib import admin
from django.forms import CharField

from .models import MusicianVacancy, BandVacancy, INSTRUMENTS, GENRES


class ContactsWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.TextInput(attrs={'placeholder': 'Контакт 1'}),
            forms.TextInput(attrs={'placeholder': 'Контакт 2'}),
            forms.TextInput(attrs={'placeholder': 'Контакт 3'}),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value
        return ["", "", ""]


class ContactsField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.CharField(required=False),
            forms.CharField(required=False),
            forms.CharField(required=False),
        )
        super().__init__(fields, widget=ContactsWidget, *args, **kwargs)

    def compress(self, data_list):
        return [item for item in data_list if item]


class MusicianVacancyForm(forms.ModelForm):
    instruments = forms.MultipleChoiceField(
        choices=INSTRUMENTS,
        widget=forms.CheckboxSelectMultiple,
        label="Инструменты"
    )

    genres = forms.MultipleChoiceField(
        choices=GENRES,
        widget=forms.CheckboxSelectMultiple,
        label="Жанры"
    )

    contacts = ContactsField(
        label="Контакты",
        required=False,
        help_text="Введите до трех контактов",
    )

    class Meta:
        model = MusicianVacancy
        fields = '__all__'


class BandVacancyForm(forms.ModelForm):

    contacts = ContactsField(
        label="Контакты",
        required=False,
        help_text="Введите до трех контактов",
    )

    class Meta:
        model = BandVacancy
        fields = '__all__'
