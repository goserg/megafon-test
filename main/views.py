from django.shortcuts import render
from .models import Money
from .forms import ParseForm

from .parser import parse

# Create your views here.
def home_view(request):
  money = Money.objects.all()
  form = ParseForm()
  if request.method == 'POST':
    form = ParseForm(request.POST)
    if form.is_valid():
      new_money = form.save(commit=False)
      nds = new_money.nds if (new_money.nds and new_money.hasNds) else 0
      new_money.parsed = parse(new_money.value, nds)
      
      new_money.save()
      form = ParseForm()
  return render(request, "index.html", {'money': money, 'form': form})