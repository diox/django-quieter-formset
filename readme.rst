django-quieter-formset
===========================

A formset that validates its data and puts them into non-form errors
as opposed to raising 500 errors.

Usage:

from quieter_formset.formset import BaseFormSet, BaseModelFormSet

modelformset_factory(User, formset=BaseModelFormSet)
formset_factory(ArticleForm, formset=BaseFormSet)

License: BSD

Author: Andy McKay amckay@mozilla.com
