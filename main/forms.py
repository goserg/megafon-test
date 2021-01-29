from django.forms import ModelForm
from .models import Money

class ParseForm(ModelForm):
  class Meta:
    model = Money
    fields = ['value', 'hasNds', 'nds', 'parsed']

  def __init__(self, *args, **kwargs):
    super(ParseForm, self).__init__(*args, **kwargs)
    self.fields['value'].widget.attrs.update({'class' : 'input-form__input'})
    self.fields['hasNds'].widget.attrs.update({'class' : 'checkbox'})
    self.fields['nds'].widget.attrs.update({'class' : 'input-form__input'})