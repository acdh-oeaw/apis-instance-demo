# fields.py

from django.db import models
from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.template.loader import render_to_string
import json


class AlternativeLabelsWidget(forms.Widget):
    def format_value(self, value):
        if value is None:
            return '[]'
        if isinstance(value, str):
            try:
                # ensure it's valid JSON
                json.loads(value)
                return value
            except Exception:
                return json.dumps([])
        try:
            return json.dumps(value)
        except Exception:
            return json.dumps([])

    def render(self, name, value, attrs=None, renderer=None):
        val = self.format_value(value)
        # parse into list of {'language':..,'label':..}
        parsed = []
        try:
            parsed = json.loads(val)
            if isinstance(parsed, dict):
                parsed = [{'language': k, 'label': v} for k, v in parsed.items()]
        except Exception:
            parsed = []

        context = {
            'name': name,
            'value': val,
            'items': parsed,
        }
        html = render_to_string('apis_ontology/altlabels_widget.html', context)
        return mark_safe(html)

    def value_from_datadict(self, data, files, name):
        # widget stores JSON string in hidden input with the field name
        return data.get(name, '[]')


class AlternativeLabelsWidgetFormField(forms.JSONField):
    widget = AlternativeLabelsWidget


class AlternativeLabelsField(models.JSONField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": AlternativeLabelsWidgetFormField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self._stringify(value)

    def _stringify(self, value):
        # value can be None, a dict, or a list of dicts
        import json
        if not value:
            return ""
        try:
            if isinstance(value, str):
                value = json.loads(value)
        except Exception:
            return str(value)
        if isinstance(value, dict):
            items = [f"{v} ({k})" for k, v in value.items()]
        elif isinstance(value, list):
            items = [
                f"{item.get('label','')} ({item.get('language','')})".strip()
                for item in value if item.get('label') or item.get('language')
            ]
        else:
            return str(value)
        return ", ".join(items)
