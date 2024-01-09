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
# ezform.tests

# pylint: disable=C0415,E0401
import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase


class date_range_field(TestCase):

    def get_target_cls(self):
        from ezform.fields import DateRangeField
        return DateRangeField

    def test_valid_input(self):
        CLASS = self.get_target_cls()
        obj = CLASS()

        self.assertTrue(obj.clean('2016-02-21 - 2017-01-31'))
        self.assertTupleEqual(
            tuple(),
            obj.clean('Any Date')
        )
        self.assertTrue(obj.clean('2017-2-21 - 2019-1-31'))

    def test_null_input(self):
        CLASS = self.get_target_cls()
        obj = CLASS()

        self.assertFalse(obj.clean(''))
        self.assertFalse(obj.clean('   '))
        self.assertFalse(obj.clean('some.random.text'))
        self.assertFalse(obj.clean('2017-02-21 -'))
        self.assertFalse(obj.clean('Any Date - '))
        self.assertFalse(obj.clean('2017-02-21 - '))

    def test_invalid_input(self):
        CLASS = self.get_target_cls()
        obj = CLASS()

        with self.assertRaises(ValidationError):
            obj.clean('2018-02-21 - 2018-02-29')

        with self.assertRaises(ValidationError):
            obj.clean('2018-02-21 - today')


class compact_text_field(TestCase):

    def get_target_cls(self):
        from ezform.fields import CompactTextField
        return CompactTextField


class date(TestCase):

    def test_basic(self):
        a = datetime.date(
            year=2014,
            month=12,
            day=12
        )
        b = datetime.date(
            year=2015,
            month=1,
            day=16
        )
        self.assertEqual(
            ( b - a ).days,
            35
        )

    def test_null_skip(self):
        a = datetime.date(
            year=2014,
            month=12,
            day=12
        )
        b = datetime.date(
            year=2015,
            month=1,
            day=16
        )
        from .utils import DayCount
        obj = DayCount(a, b)
        self.assertEqual(
            obj.do(),
            35
        )

    def test_existing_skip(self):
        a = datetime.date(
            year=2014,
            month=12,
            day=12
        )
        b = datetime.date(
            year=2015,
            month=1,
            day=16
        )

        from dummyapp.models import SkipDate
        rec = SkipDate(
            actual=datetime.date(
                year=2014,
                month=12,
                day=25
            )
        )
        rec.save()

        from .utils import DayCount
        obj = DayCount(a, b)
        self.assertEqual(
            obj.do(),
            34
        )
