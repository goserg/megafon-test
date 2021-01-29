from django.shortcuts import render
from .models import Money
from .forms import ParseForm

# Create your views here.
def home_view(request):
  money = Money.objects.all()
  form = ParseForm()
  if request.method == 'POST':
    print('printing post', request.POST)
    form = ParseForm(request.POST)
    if form.is_valid():
      new_money = form.save(commit=False)
      new_money.parsed = parse(str(new_money.value), str(new_money.nds))

      new_money.save()
  return render(request, "index.html", {'money': money, 'form': form})


from typing import Union

HUNDREDS = ("сто", "двести", "триста", "четыреста", "пятьсот", "шестьсот", "семьсот", "восемьсот", "девятьсот",)
TENTHS = ("двадцать", "тридцать", "сорок", "пятьдесят", "шестьдесят", "семдесят", "восемдесят", "девяносто",)
NUMBERS = (
  "один",
  "два",
  "три",
  "четыре",
  "пять",
  "шесть",
  "семь",
  "весемь",
  "девять",
  "десять",
  "одинадцать",
  "двенадцать",
  "тринадцать",
  "четырнадцать",
  "пятнадцать",
  "шестнадцать",
  "семнадцать",
  "восемнадцать",
  "девятнадцать",
  "двадцать"
)


def parse(raw_value: str, raw_nds: str) -> str:
  """
  Переводит число, записаное в цифровой форме, в рукописную

  Вызывает исключение ValueError:
    --число больше 10**12
    --неверная запись числа (допускается использовать '.' или ',' для дробных чисел)
  """
  nds = 0
  try:
    value = str_to_value(raw_value)
    if raw_nds:
      nds = str_to_value(raw_nds)
  except:
    raise ValueError("Ошибка в записи числа")
  
  full_price = value

  if nds:
    nds_value = round((value * nds / 100 ) * 100) / 100
    full_price += nds_value

    nds_in_words = f", включая НДС ({nds}%) в сумме {nds_value} руб. {say_big_number(nds_value)}"

  processed_value = f"{full_price} {say_big_number(full_price)}{nds_in_words if nds else ''}."

  return processed_value

def say_big_number(value: int):
  if value >= 10**12:
    raise ValueError("Я еще не умею считать тириллионы")
  rubles = int(value)

  billions = rubles // 10**9
  millions = rubles // 10**6 - (billions * 1000)
  thousands = rubles // 1000 - (millions * 1000 + billions * 10**6)
  units = rubles % 1000
  kopeyka = round(value % 1 * 100)

  value_in_words = []
  if rubles:
    rubles_in_words = []
    if billions:
      rubles_in_words.append(say(billions))
      rubles_in_words.append(modifyScale("миллиард", billions))
    if millions:
      rubles_in_words.append(say(millions))
      rubles_in_words.append(modifyScale("миллион", millions))
    if thousands:
      rubles_in_words.append(say(thousands, True))
      rubles_in_words.append(modifyScale("тысяча", thousands))
    if units:
      rubles_in_words.append(say(units))
    value_in_words.append(f'({" ".join(rubles_in_words)}) {modifyScale("рубль", units)}')

  if kopeyka > 0:
    value_in_words.append(str(kopeyka))
    value_in_words.append(modifyScale("копейка", kopeyka))
  return " ".join(value_in_words)

def say(n: int, isFem: bool = False) -> str:
  """
  Первеводит целое число до 3 знаков в прописную форму.

  Аргумент isFem для корректного отображения единцы и двойки в жеском роде,
  isFem == True для тысяч рублей и коппеек,
  isFem == False должен быть во всех остальных случаях.
  """
  hundreds = n // 100
  last_two = n - hundreds * 100 # две последние цифры числа
  tenth = last_two // 10
  unit = last_two % 10 # единицы

  result = []
  if hundreds != 0:
    result.append(HUNDREDS[hundreds - 1])
  if (last_two <= 20):
    if isFem:
      if last_two == 1:
        result.append("одна")
      elif last_two == 2:
        result.append("две")
      else:
        result.append(NUMBERS[last_two - 1])
    else:
      result.append(NUMBERS[last_two - 1])
    return " ".join(result)

  if tenth != 0:
    result.append(TENTHS[tenth - 2])

  if isFem:
    if unit == 1:
      result.append("одна")
      return " ".join(result)
    if unit == 2:
      result.append("две")
      return " ".join(result)

  if unit != 0:
    result.append(NUMBERS[unit - 1])

  return " ".join(result)


def modifyScale(scale: str, n: int) -> str:
  """
  Модицикация склонения единиц
  """

  SCALES = {
    "тысяча": ("тысячa", "тысячи", "тысяч"),
    "миллион": ("миллион", "миллиона", "миллионов"),
    "миллиард": ("миллиард", "миллиарда", "миллиардов"),
    "рубль": ("рубль", "рубля", "рублей"),
    "копейка": ("копейка", "копейки", "копеек"),
  }

  if n == 1 or n % 10 == 1 and n != 11:
    return SCALES[scale][0]
  if n in (2, 3, 4) or n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
    return SCALES[scale][1]
  return SCALES[scale][2]


def str_to_value(string: str) -> Union[int, float]:
  """
  Перевод строки в int или float

  Использовать в блоке try except, или предварительно проверить строку
  на возможность отображения в виде числа
  """
  string = string.replace(' ', '')
  if ',' in string:
    string = string.replace(',', '.')

  return float(string) if '.' in string else int(string)