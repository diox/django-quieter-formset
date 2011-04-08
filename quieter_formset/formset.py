from django.core.exceptions import ValidationError
from django.forms.formsets import (TOTAL_FORM_COUNT, INITIAL_FORM_COUNT,
                                   MAX_NUM_FORM_COUNT,
                                   BaseFormSet as DjangoBaseFormSet)
from django.forms.models import BaseModelFormSet as DjangoBaseModelFormSet
from django.forms.formsets import ManagementForm


__all__ = ['BaseFormSet', 'BaseModelFormSet']


err = ('ManagementForm data is missing or has been tampered with. Form data '
       'could have been lost.')

class QuieterBaseFormset:
    def _management_form(self):
        """Returns the ManagementForm instance for this FormSet."""
        if self.is_bound:
            form = ManagementForm(self.data, auto_id=self.auto_id, prefix=self.prefix)
            if not form.is_valid():
                self._non_form_errors = err
        else:
            form = ManagementForm(auto_id=self.auto_id, prefix=self.prefix, initial={
                TOTAL_FORM_COUNT: self.total_form_count(),
                INITIAL_FORM_COUNT: self.initial_form_count(),
                MAX_NUM_FORM_COUNT: self.max_num
            })
        return form
    management_form = property(_management_form)

    # Quieter handling for mangled management forms
    def total_form_count(self):
        if self.data or self.files:
            if hasattr(self.management_form, 'cleaned_data'):
                return self.management_form.cleaned_data[TOTAL_FORM_COUNT]
            else:
                return 0
        else:
            return DjangoBaseModelFormSet.total_form_count(self)


class BaseFormSet(QuieterBaseFormset, DjangoBaseFormSet):
    pass


class BaseModelFormSet(QuieterBaseFormset, DjangoBaseModelFormSet):
    # Handling of invalid data on form construction
    def _construct_forms(self):
        self.forms = []
        for i in xrange(self.total_form_count()):
            try:
                self.forms.append(self._construct_form(i))
            except (ValueError, IndexError), err:
                self._non_form_errors = err
                self.forms.append(self._construct_form(self.initial_form_count))
