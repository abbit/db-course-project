from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_not_zero(value):
    if value == 0:
        raise ValidationError('Value cannot be zero')


def validate_date_in_past(date):
    if date > now():
        raise ValidationError("The date cannot be in the future!")
