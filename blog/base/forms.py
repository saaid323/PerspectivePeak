from django import forms

from .models import Blog

class BlogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["body"].required = False

    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ['author']