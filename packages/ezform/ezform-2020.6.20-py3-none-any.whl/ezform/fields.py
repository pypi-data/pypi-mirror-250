# -*- python -*-
#
# Copyright 2016, 2017, 2018, 2019, 2020 Xingeng Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ezform.fields

import datetime

from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.utils import formats
from django.utils.translation import gettext_lazy as _

from .encoding import StringEncoding


class CompactTextField(CharField):
    '''
    compact text field
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.backend = StringEncoding()

    def to_python(self, value):
        rval = None

        if value in self.empty_values:
            return rval

        try:
            rval = self.backend.decode(value)
        except Exception as _ex:  # pylint: disable=W0718
            self.onError(_ex)
        return rval

    def onError(self, exc=None):  # pylint: disable=W0613
        return


class DateRangeField(CharField):
    '''
    customized date range field

    This class combines the logics from `CharField` and `DateField`.
    '''

    VALUE_ANYDATE = 'Any Date'
    SEP = ' - '
    input_formats = formats.get_format_lazy('DATE_INPUT_FORMATS')
    default_error_messages = {
        'invalid': _('Enter a valid date.'),
    }

    def __init__(self, input_formats=None, **kwargs):
        super().__init__(**kwargs)
        if input_formats is not None:
            self.input_formats = input_formats

    def strptime(self, value, format):
        '''
        adapted from `DateField`
        '''

        return datetime.datetime.strptime(value, format).date()

    def token_to_date(self, value):
        '''
        adapted from `BaseTemporalField`
        '''

        value = value.strip()
        for format in self.input_formats:
            try:
                return self.strptime(value, format)
            except (ValueError, TypeError):
                continue
        raise ValidationError(self.error_messages['invalid'], code='invalid')

    def to_python(self, value):
        rval = None

        if value in self.empty_values:
            return rval
        if isinstance(value, tuple):
            return value

        value = value.strip()
        if value:
            if value == self.VALUE_ANYDATE:
                rval = tuple()
            elif self.SEP in value:
                tokens = value.split(self.SEP)
                rval = (
                    self.token_to_date(tokens[0]),
                    self.token_to_date(tokens[1])
                )
        return rval

    def validate(self, value):
        if value in self.empty_values:
            return None
        ex = ValidationError(
            self.error_messages['invalid'],
            code='invalid'
        )
        if len(value) not in (0, 2):
            raise ex
        for item in value:
            if not isinstance(item, datetime.date):
                raise ex
