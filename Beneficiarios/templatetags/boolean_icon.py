
from django.template import Library, Node
from django.utils.html import format_html

register = Library()

# NEF-35
@register.simple_tag
def boolean_icon(value):
    return format_html('<i class="fas fa-check-square fa-lg"></i>&nbsp;&nbsp;&nbsp;') \
        if value else format_html('<i class="far fa-square fa-lg"></i>&nbsp;&nbsp;&nbsp;')
