from django import forms
from .models import Blog
from django_ckeditor_5.widgets import CKEditor5Widget


class BlogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["body"].required = False

    class Meta:
        model = Blog
        fields = '__all__'
        widgets = {
            "text": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="comment"
                )
        }
        exclude = ['author']