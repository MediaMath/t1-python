import unittest
from terminalone import t1types


class TestT1Types(unittest.TestCase):
    def test_strpt(self):
        date_one = '2016-11-07T09:07:57'
        date_two = '2016-11-07T09:07:57+1000'
        date_three = '2016-11-07T09:07:57+01:00'

        dt_one = t1types.strpt(date_one)
        dt_two = t1types.strpt(date_two)
        dt_three = t1types.strpt(date_three)

        self.assertEqual(2016, dt_one.year)
        self.assertEqual(2016, dt_two.year)
        self.assertEqual(2016, dt_three.year)

        self.assertEqual(11, dt_one.month)
        self.assertEqual(11, dt_two.month)
        self.assertEqual(11, dt_three.month)

        self.assertEqual(7, dt_one.day)
        self.assertEqual(7, dt_two.day)
        self.assertEqual(7, dt_three.day)

        self.assertEqual(9, dt_one.hour)
        self.assertEqual(9, dt_two.hour)
        self.assertEqual(9, dt_three.hour)

        self.assertEqual(7, dt_one.minute)
        self.assertEqual(7, dt_two.minute)
        self.assertEqual(7, dt_three.minute)

        self.assertEqual(57, dt_one.second)
        self.assertEqual(57, dt_two.second)
        self.assertEqual(57, dt_three.second)

        self.assertEqual(0, dt_one.tzinfo.utcoffset().seconds)
        self.assertEqual(36000, dt_two.tzinfo.utcoffset().seconds)
        self.assertEqual(3600, dt_three.tzinfo.utcoffset().seconds)

    def test_strft(self):
        date_str = '2016-11-07T09:07:57+01:00'
        expected_no_offset = '2016-11-07T09:07:57'
        expected_offset = '2016-11-07T09:07:57+0100'

        dt_obj = t1types.strpt(date_str)

        self.assertEqual(expected_no_offset, t1types.strft(dt_obj))
        self.assertEqual(expected_offset, t1types.strft(dt_obj, offset=True))
        self.assertEqual("", t1types.strft(None, null_on_none=True))
        with self.assertRaises(AttributeError):
            t1types.strft(None)
