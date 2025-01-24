from django import template

register = template.Library()

@register.filter
def dictkey(value, key):
    """Возвращает значение из словаря по ключу."""
    try:
        return value[key]
    except KeyError:
        return None
