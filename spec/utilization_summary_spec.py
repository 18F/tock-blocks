import datetime
import unittest
import sys
from collections import namedtuple
import utilization_summary
sys.path.append('..')

today = datetime.date.today()

class UtilizationSummaryTestCase(unittest.TestCase):
    """Tests for `utilization_summary.py`."""
    # def test_all_users_from_file(self):

    # def test_util_csv(self):
    #

    def test_calc_billable_hours(self):
        test_entry_list = [{'project_name': 'TTS Acq / Internal Acq', 'hours_spent': 1, 'billable': False}, {'project_name': '18F / Learn', 'hours_spent': 1, 'billable': False}, {'project_name': 'TTS Acq / Internal Acq', 'hours_spent': 1, 'billable': True}, {'project_name': 'TTS Acq / Learn', 'hours_spent': 4, 'billable': True}]
        self.assertEqual(utilization_summary.calc_billable_hours(test_entry_list), 5)

    def test_calc_internal_hours(self):
        test_entry_list = [{'project_name': 'TTS Acq / Internal Acq', 'hours_spent': 1, 'billable': False}, {'project_name': 'TTS Acq / Internal Acq', 'hours_spent': 1, 'billable': True}, {'project_name': 'TTS Acq / Learn', 'hours_spent': 4, 'billable': True}]
        self.assertEqual(utilization_summary.calc_internal_hours(test_entry_list), 1)

    def test_calc_total_hours(self):
        """Does the sample list of entries return a total number of hours equal to the sum?"""
        test_entry_list = [{'hours_spent': 1}, {'hours_spent': 1}, {'hours_spent': 1}, {'hours_spent': 4}]
        self.assertEqual(utilization_summary.calc_total_hours(test_entry_list), 7)

    def test_month_average_and_goal_row(self):
        test_user_list_row = ['name', 'type', 'team', [0.5, 4.0, 4.5], [1.5, 2.0, 4.5], [0.5, 3.0, 4.5], [0.5, 3.0, 4.5]]
        result = [4.0, 2.0, 3.0, 3.0, 2.7, '', '58.9', '78.9']
        self.assertEqual(utilization_summary.month_average_and_goal_row(
            test_user_list_row, 1), result)

    def test_mean(self):
        """Does a list of 4 2s have a mean of 2?"""
        self.assertEqual(utilization_summary.mean([2, 2, 2, 2]), 2)

    def test_find_months_raise_error(self):
        """Does August and Oktoberfest render an error?"""
        Args = namedtuple('MyStruct', 'beginmonth lastmonth')
        args = Args(beginmonth='August', lastmonth='Oktoberfest')
        self.assertRaises(ValueError, lambda: utilization_summary.find_months(today, args))

    def test_find_months_december(self):
        """Does January and December render a list of [1,13]?"""
        Args = namedtuple('MyStruct', 'beginmonth lastmonth')
        args = Args(beginmonth='January', lastmonth='December')
        self.assertEqual(utilization_summary.find_months(today, args), [1, 12])

    def test_find_months(self):
        """Does August and October render a list of [8,10]?"""
        Args = namedtuple('MyStruct', 'beginmonth lastmonth')
        args = Args(beginmonth='August', lastmonth='October')
        self.assertEqual(utilization_summary.find_months(today, args), [8, 10])

if __name__ == '__main__':
    unittest.main()
