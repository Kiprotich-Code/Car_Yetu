from django import forms

# forms 
class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    title = forms.CharField(max_length=255)