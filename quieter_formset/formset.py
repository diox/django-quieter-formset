from django.core.exceptions import ValidationError
from django.forms.formsets import (TOTAL_FORM_COUNT,
                                   BaseFormSet as DjangoBaseFormSet)
from django.forms.models import BaseModelFormSet as DjangoBaseModelFormSet
from django.forms.formsets import ManagementForm


__all__ = ['BaseFormSet', 'BaseModelFormSet']


class BaseFormSet(DjangoBaseFormSet):
    # Quieter handling for mangled management forms
    def total_form_count(self):
        if self.data or self.files:
            try:
                return self.management_form.cleaned_data[TOTAL_FORM_COUNT]
            except ValidationError, err:
                self._non_form_errors = err
                return 0
        else:
            return DjangoBaseFormSet.total_form_count(self)


class BaseModelFormSet(DjangoBaseModelFormSet):
    # Quieter handling for mangled management forms
    def total_form_count(self):
        if self.data or self.files:
            try:
                return self.management_form.cleaned_data[TOTAL_FORM_COUNT]
            except ValidationError, err:
                self._non_form_errors = err
                return 0
        else:
            return DjangoBaseModelFormSet.total_form_count(self)

    # Handling of invalid data on form construction
    def _construct_forms(self):
        self.forms = []
        for i in xrange(self.total_form_count()):
            try:
                self.forms.append(self._construct_form(i))
            except (ValueError, IndexError), err:
                self._non_form_errors = err
                self.forms.append(self._construct_form(self.initial_form_count))
