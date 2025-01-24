from django import template

register = template.Library()

@register.filter
def dictkey(value, key):
    """Фильтр для получения значения из словаря по ключу"""
    return value.get(str(key), None)
