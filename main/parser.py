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


def parse(value: float, nds: float = 0) -> str:
  """
  Переводит число, записаное в цифровой форме, в рукописную

  Вызывает исключение ValueError:
    --число больше 10**12
    --неверная запись числа (допускается использовать '.' или ',' для дробных чисел)
  """
  if value < 0:
    value = -value
  if nds < 0:
    nds = -nds
  full_price = value

  if nds:
    nds_value = round((value * nds / 100 ), 2)
    full_price = round(full_price + nds_value, 2)

    nds_in_words = f", включая НДС ({nds}%) в сумме {'{:,}'.format(nds_value).replace(',', ' ').replace('.', ',')} \
      руб. {say_big_number(nds_value)}"

  processed_value = f"{'{:,}'.format(full_price).replace(',', ' ').replace('.', ',')} \
  {say_big_number(full_price)}{nds_in_words if nds else ''}."

  return processed_value

def say_big_number(value: float):
  if value >= 10**12:
    raise ValueError("Я не умею считать тириллионы")
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
    value_in_words.append('{:0>2}'.format(kopeyka))
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
  if (last_two <= 20 and last_two > 0):
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


if __name__ == "__main__":
  print("testing")
  print(parse(100))