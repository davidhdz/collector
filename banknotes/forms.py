from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .models import Album, Banknote

User = settings.AUTH_USER_MODEL

CONDITION_CHOICES = (
    ("UNC", _("Uncirculated")),
    ("AU", _("About Uncirculated")),
    ("XF", _("Extremely Fine")),
    ("VF", _("Very Fine")),
    ("F", _("Fine")),
    ("VG", _("Very Good")),
    ("G", _("Good")),
    ("PR", _("Poor")),
)


class AddRemoveAlbumForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    album = forms.ModelChoiceField(Album.objects.all())


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = (
            "name",
            "description",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"style": "width: 50%;", "class": "form-control"}
            ),
            "description": forms.TextInput(
                attrs={"style": "width: 50%;", "class": "form-control"}
            ),
        }


class BanknoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["album"].queryset = Album.objects.filter(owner=user)

    class Meta:
        model = Banknote
        fields = (
            "country",
            "denomination",
            "currency",
            "pick_number",
            "issued_date",
            "year",
            "description_front",
            "description_back",
            "serial_number",
            "size",
            "observations",
            "image_front",
            "image_back",
            "commemorative",
            "polymer",
            "overprint",
            "specimen",
            "notgeld",
            "grading",
            "album",
        )
        widgets = {
            "country": forms.TextInput(
                attrs={"style": "width: 50%;", "class": "form-control"}
            ),
            "denomination": forms.TextInput(
                attrs={"style": "width: 50%;", "class": "form-control"}
            ),
            "currency": forms.TextInput(
                attrs={"style": "width: 50%;", "class": "form-control"}
            ),
            "pick_number": forms.TextInput(
                attrs={"style": "width: 50%;", "class": "form-control"}
            ),
            "issued_date": forms.TextInput(
                attrs={"style": "width: 50%;", "class": "form-control"}
            ),
            "year": forms.TextInput(
                attrs={
                    "type": "number",
                    "style": "width: 50%;",
                    "class": "form-control",
                }
            ),
            "description_front": forms.TextInput(
                attrs={"style": "width: 50%;", "class": "form-control"}
            ),
            "description_back": forms.TextInput(
                attrs={"style": "width: 50%;", "class": "form-control"}
            ),
            "serial_number": forms.TextInput(
                attrs={"style": "width: 50%;", "class": "form-control"}
            ),
            "size": forms.TextInput(
                attrs={"style": "width: 50%;", "class": "form-control"}
            ),
            "observations": forms.Textarea(
                attrs={"style": "width: 50%;", "class": "form-control", "rows": "3"}
            ),
            "grading": forms.Select(
                choices=CONDITION_CHOICES,
                attrs={"style": "width: 50%;", "class": "form-control"},
            ),
            "commemorative": forms.CheckboxInput,
            "polymer": forms.CheckboxInput,
            "overprint": forms.CheckboxInput,
            "specimen": forms.CheckboxInput,
            "notgeld": forms.CheckboxInput,
            "album": forms.CheckboxSelectMultiple(),
        }
