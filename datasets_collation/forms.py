from django import forms

class MergeDatasetForm(forms.Form):
    COUNTRY_CHOICES = [
        ('Netherlands', 'Netherlands'),
        ('United Kingdom', 'United Kingdom'),
    ]

    dataset_1 = forms.FileField(label="Dataset 1")
    dataset_2 = forms.FileField(label="Dataset 2")
    countries = forms.MultipleChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'select2-multi'})
    )
