from django import forms

class MergeDatasetForm(forms.Form):
    dataset1 = forms.FileField(label="Dataset 1")
    dataset2 = forms.FileField(label="Dataset 2")
