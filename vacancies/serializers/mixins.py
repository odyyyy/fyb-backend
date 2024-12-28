import re
from typing import List

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class VacancyWithDateTimeMixin:
    date = serializers.DateTimeField(write_only=True)


class VacancyContactsValidatorMixin:
    def validate_contacts(self, contacts: List[str]):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_pattern = r'/^(\+|)(7|8)( |)\d{3}( |)\d{3}( |)(\d{2}( |)){2}$/'
        socials_nickname_pattern = r'^[A-Za-z0-9]+([A-Za-z0-9]*|[._-]?[A-Za-z0-9]+)*$'

        contacts_regex_patterns = (
            phone_pattern,
            email_pattern,
            socials_nickname_pattern
        )

        for i in range(len(contacts)):
            if not re.match(contacts_regex_patterns[i], contacts[i]):
                raise serializers.ValidationError(
                    _("Invalid contacts format or order. Example: ['+7123456789','mail@example.com' 'username123']"))

        return contacts
