# main/templatetags/custom_filters.py

from django import template
from django.forms.boundfield import BoundField

register = template.Library()


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name="add_class")
def add_class(field, css_class):
    if isinstance(field, BoundField):
        existing_classes = field.field.widget.attrs.get("class", "")
        new_classes = f"{existing_classes} {css_class}".strip()
        attrs = {"class": new_classes}
        # Preserve the existing id attribute
        if "id" in field.field.widget.attrs:
            attrs["id"] = field.field.widget.attrs["id"]
        return field.as_widget(attrs=attrs)
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


@register.filter(name="add_percent")
def add_percent(value):
    try:
        return f"{value}%"
    except (ValueError, TypeError):
        return "0%"
