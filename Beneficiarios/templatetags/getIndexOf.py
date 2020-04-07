from django.template import Library

register = Library()

@register.filter
def get_index_of(List, obj):
    return List.index(obj)