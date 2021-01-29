from django.forms import ModelForm
from .models import Money

class ParseForm(ModelForm):
  class Meta:
    model = Money
    fields = ['value', 'hasNds', 'nds', 'parsed']

  def __init__(self, *args, **kwargs):
    super(ParseForm, self).__init__(*args, **kwargs)
    self.fields['value'].widget.attrs.update({'class' : 'input-form__input', 'placeholder': ' '})
    self.fields['hasNds'].widget.attrs.update({'class' : 'checkbox', 'id': 'check_1'})
    self.fields['nds'].widget.attrs.update({'class' : 'input-form__input', 'placeholder': ' '})