import nh3

from django import forms
from django.forms import Textarea

NH3_TAGS = {
    "a",
    "p",
    "strong",
    "img",
    "ul",
    "ol",
    "li",
    "b",
    "s",
    "u",
}

NH3_ATTR = {
    "a": {
        "href",
        "target",
    },
    "img": {
        "alt",
        "src",
    },
}


class HtmlTextField(forms.CharField):
    widget = Textarea

    def to_python(self, value):
        value = super().to_python(value)
        if value not in self.empty_values:
            value = nh3.clean(
                value,
                tags=NH3_TAGS,
                attributes=NH3_ATTR,
            )
        return value
