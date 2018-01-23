import unittest

import sys
sys.path.append('..')
import datetime
import utilization_summary
from collections import namedtuple

today = datetime.date.today()

class UtilizationSummaryTestCase(unittest.TestCase):
    """Tests for `utilization_summary.py`."""
    # def test_all_users_from_file(self):

    # def test_util_csv(self):
    #

    def test_calc_billable_hours(self):
        test_entry_list = [["TTS Acq / Internal Acq",0,0,0,0,1, "False"],["18F / Learn",0,0,0,0,1, "False"],["TTS Acq / Internal Acq",0,0,0,0,1, "True"],["TTS Acq / Learn",0,0,0,0,4, "True"]]
        self.assertEqual(utilization_summary.calc_billable_hours(test_entry_list), 5)

    def test_calc_internal_hours(self):
        test_entry_list = [["TTS Acq / Internal Acq",0,0,0,0,1, "False"],["18F / Learn",0,0,0,0,1, "False"],["TTS Acq / Internal Acq",0,0,0,0,1, "True"],["TTS Acq / Learn",0,0,0,0,4, "True"]]
        self.assertEqual(utilization_summary.calc_internal_hours(test_entry_list), 1)

    def test_calc_total_hours(self):
        """Does the sample list of entries return a total number of hours equal to the sum?"""
        test_entry_list = [[0,0,0,0,0,1],[0,0,0,0,0,1],[0,0,0,0,0,1],[0,0,0,0,0,4]]
        self.assertEqual(utilization_summary.calc_total_hours(test_entry_list), 7)

    def test_monthly_and_average(self):
        test_user_list_row = ['name', 'type', 'team', [0.5, 4.0, 4.5], [1.5, 2.0, 4.5], [0.5, 3.0, 4.5], [0.5, 3.0, 4.5]]
        result = [4.0, 2.0, 3.0, 3.0, 2.7]
        self.assertEqual(utilization_summary.monthly_and_average(test_user_list_row, 1), result)

    def test_mean(self):
        """Does a list of 4 2s have a mean of 2?"""
        self.assertEqual(utilization_summary.mean([2,2,2,2]), 2)

    def test_find_months_raise_error(self):
        """Does August and Oktoberfest render an error?"""
        Args = namedtuple('MyStruct', 'beginmonth lastmonth')
        args = Args(beginmonth='August', lastmonth='Oktoberfest')
        self.assertRaises(ValueError, lambda: utilization_summary.find_months(today, args))

    def test_find_months_december(self):
        """Does January and December render a list of [1,13]?"""
        Args = namedtuple('MyStruct', 'beginmonth lastmonth')
        args = Args(beginmonth='January', lastmonth='December')
        self.assertEqual(utilization_summary.find_months(today, args), [1,12])

    def test_find_months(self):
        """Does August and October render a list of [8,10]?"""
        Args = namedtuple('MyStruct', 'beginmonth lastmonth')
        args = Args(beginmonth='August', lastmonth='October')
        self.assertEqual(utilization_summary.find_months(today, args), [8,10])

if __name__ == '__main__':
    unittest.main()
