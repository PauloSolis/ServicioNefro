from django.template import Library

register = Library()

@register.filter
def get_obj_attr(obj, attr):
    try:
        return obj[attr]
    except:
        return "-"