from django import forms
from django.utils.translation import gettext as _
from .models import Allotment


class TagForm(forms.Form):
    error_css_class = "errors"
    # css_classes = "form-row"
    quantity = forms.IntegerField(
        #initial="",
        required=True,
        error_messages={"required": "this field is required."},
        # widget=forms.TextInput(attrs={'class': 'form-row'})
    )
    allotment = forms.ModelChoiceField(
        queryset=Allotment.objects.filter(quantity__gte=0),
        to_field_name='lot_number',
        required=True,
        # widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_quantity(self,):
        value = self.cleaned_data["quantity"]
        if value <= 0:
            raise forms.ValidationError(
                _("This field must be greater than 0"),
                code='invalid',
            )
        return value

    def clean_allotment(self,):
        alot = self.cleaned_data["allotment"]
        value = self.cleaned_data["quantity"]
        if not alot.active:
            raise forms.ValidationError(
                _("This allotment is inactive."),
                code="invalid"
            )
        if value > alot.quantity:
            raise forms.ValidationError(
                _("This allotment does not have enough tag available"),
                code="invalid"
            )
        return alot


class ExportTagForm(forms.Form):
    error_css_class = "errors"

    quantity = forms.IntegerField(
        min_value=1,
        max_value=100,
        required=True,
        error_messages={"required": "This field is required."},
    )
    
    def clean_quantity(self,):
        value = self.cleaned_data["quantity"]
        if value <= 0:
            raise forms.ValidationError(
                _("This field must be greater than 0"),
                code='invalid',
            )
        return value
