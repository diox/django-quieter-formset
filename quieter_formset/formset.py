from django.core.exceptions import ValidationError
from django.forms.formsets import (TOTAL_FORM_COUNT, INITIAL_FORM_COUNT,
                                   MAX_NUM_FORM_COUNT,
                                   BaseFormSet as DjangoBaseFormSet)
from django.forms.models import BaseModelFormSet as DjangoBaseModelFormSet
from django.forms.formsets import ManagementForm


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
            return super(DjangoBaseFormSet, self).total_form_count()


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
            return super(DjangoBaseModelFormSet, self).total_form_count()

    # Handling of invalid data on form construction
    def _construct_forms(self):
        self.forms = []
        for i in xrange(self.total_form_count()):
            try:
                self.forms.append(self._construct_form(i))
            except (ValueError, IndexError), err:
                self._non_form_errors = err
                self.forms.append(self._construct_form(self.initial_form_count))
