from django import template

register = template.Library()

CURRENCIES_SYMBOLS = {
    'rub': 'Р',
    'usd': '$',
}


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def currency(value):
    """
   Value: значение, к которому нужно применить фильтр
   """
    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value} Р'
