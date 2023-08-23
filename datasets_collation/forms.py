from django import forms

class MergeDatasetForm(forms.Form):
    dataset_1 = forms.FileField(label="Dataset 1")
    dataset_2 = forms.FileField(label="Dataset 2")
