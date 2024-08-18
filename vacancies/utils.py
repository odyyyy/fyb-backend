from importlib.resources._common import _

from django.contrib.postgres.fields import ArrayField
from django.forms import MultipleChoiceField
from django.utils.functional import cached_property
from django.utils.text import capfirst


class ChoiceArrayField(ArrayField):
    """
    Postgres Array field with choices.
    This will change the default form field to `MultipleChoiceField`.

    Usage:
    1) `base_field` should match the type of choices.
    2) `choices` should be specified on the `ChoiceArrayField` instead of inside `base_field`.
    3) `default` is supported (also specify on the `ChoiceArrayField`); either a single value or a list/tuple is ok.
    4) The django admin hint for M2M fields is appended to help text when rendering the form.

    Example:

        class MyChoices(models.TextChoices):
            A = ('a', 'A')
            B = ('b', 'B')

        my_choices = ChoiceArrayField(
            CharField(max_length=16),
            choices=MyChoices.choices,
            default=MyChoices.A,
        )
    """

    def _initial(self):
        """
        MultipleChoiceField wants a callable for `initial` arg.
        """
        return self.default

    FORM_HELP_TEXT_APPEND = _('Hold down “Control”, or “Command” on a Mac, to select more than one.')

    @cached_property
    def _help_text(self) -> str:
        if self.help_text:
            return f'{self.help_text} {self.FORM_HELP_TEXT_APPEND}'
        else:
            return self.FORM_HELP_TEXT_APPEND

    def formfield(
            self,
            *,
            form_class=None,
            choices_form_class=None,
            **kwargs,
    ):
        if form_class is not None or choices_form_class is not None:
            # do not attempt override
            return super().formfield(form_class=form_class, **kwargs)

        return MultipleChoiceField(**{
            'required': not self.blank,
            'label': capfirst(self.verbose_name),
            'choices': self.choices,
            'initial': self._initial,
            'help_text': self._help_text,
            **kwargs,
        })