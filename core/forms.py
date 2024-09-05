from django import forms
from .models import Report, Subcategory

class NewReportForm(forms.Form):
    subcategory_choices = [('', '------------')]  # Blank option
    subcategory_choices += [(sub.id, f"{sub.subcategory}") for sub in Subcategory.objects.all()]
    

    description = forms.CharField(required=True, max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control form-control-sm'}))
    subcategory = forms.ChoiceField(choices=subcategory_choices, required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    location = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Describe the location as accurately as possible"}))
    responsible_party = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    responsible_party_contact = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    reporter_name = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    reporter_contact = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    files = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*, video/*'}), required=False)
    latitude = forms.DecimalField(required=False, widget=forms.HiddenInput())
    longitude = forms.DecimalField(required=False, widget=forms.HiddenInput())


