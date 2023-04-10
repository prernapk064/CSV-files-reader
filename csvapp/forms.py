from django import forms


class CSVUploadForm(forms.Form):
    csv_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
