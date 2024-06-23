# main/templatetags/custom_filters.py

from django import template
from django.forms.boundfield import BoundField

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css_class):
    if isinstance(field, BoundField):
        existing_classes = field.field.widget.attrs.get("class", "")
        new_classes = f"{existing_classes} {css_class}"
        return field.as_widget(attrs={"class": new_classes})
    return field


@register.filter(name="add_attribute")
def add_attribute(field, attr_value):
    if isinstance(field, BoundField):
        attrs = {}
        definition = attr_value.split(":", 1)
        if len(definition) == 2:
            attrs[definition[0]] = definition[1]
        return field.as_widget(attrs=attrs)
    return field
