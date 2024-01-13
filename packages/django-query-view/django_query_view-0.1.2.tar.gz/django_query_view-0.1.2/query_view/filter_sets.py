import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Submit
from django.utils.translation import gettext_lazy as _


class FilterSet(django_filters.FilterSet):
    layout_fields = []

    @property
    def form(self):
        form = super().form
        form.helper = self.get_form_helper(form)
        return form

    def get_form_helper(self, form):
        helper = FormHelper()
        helper.form_method = 'GET'
        helper.template_pack = 'bootstrap4'

        if self.layout_fields:
            layout_components = list(self.layout_fields)
        else:
            layout_components = list(form.fields.keys())
        layout_components.append(Submit('', _('Submit'), css_class='btn-default'))
        helper.layout = Layout(*layout_components)
        return helper
