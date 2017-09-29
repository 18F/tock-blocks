import unittest

import sys
sys.path.append('..')
import tock_blocks
import io

class TockBlocksTestCase(unittest.TestCase):
    """Tests for `utilization_summary.py`."""

    # def test_read_CSV_to_list(selfs):

    # def test_block_for_one_person(self):

    def test_remove_leave_removing(self):
        test_entries = [["Out of Office - Other", 0, 0, 0, 0, 0], ["Out of Office - Other", 0, 0, 0, 0, 0], ["Easting", 0, 0, 0, 0, 0]]
        result = [["Easting", 0, 0, 0, 0, 0]]
        self.assertEqual(tock_blocks.remove_leave(test_entries), result)

    def test_remove_leave_not_removing(self):
        test_entries = [["moe", 0, 0, 0, 0, 0], ["ruer", 0, 0, 0, 0, 0], ["Easting", 0, 0, 0, 0, 0]]
        self.assertEqual(tock_blocks.remove_leave(test_entries), test_entries)

    def test_get_user_entries_removing(self):
        test_entries = [["Out of Office - Other", 0, "hi.me", 0, 0, 0], ["Out of Office - Other", 0, "jes.mick", 0, 0, 0], ["Easting", 0, "hi.me", 0, 0, 0]]
        result = [["Out of Office - Other", 0, "hi.me", 0, 0, 0], ["Easting", 0, "hi.me", 0, 0, 0]]
        self.assertEqual(tock_blocks.get_user_entries("hi.me", test_entries), result)

    def test_get_user_entries_not_removing(self):
        test_entries = [["Out of Office - Other", 0, "hi.me", 0, 0, 0], ["Out of Office - Other", 0, "hi.me", 0, 0, 0], ["Easting", 0, "hi.me", 0, 0, 0]]
        self.assertEqual(tock_blocks.get_user_entries("hi.me", test_entries), test_entries)

    def get_entries_in_time_period_util(self):
        test_entries = [["Out of Office - Other", 0, "hi.me", "2016-10-02","2016-10-08",30.50, 0], ["Out of Office - Admin", 0, "hi.me", "2016-11-02","2016-11-08",30.50, 0], ["Out of Office - Other", 0, "hi.me", "2016-12-02","2016-12-08", 0], ["Easting", 0, "hi.me", "2016-11-02","2016-11-08", 0]]
        result = [["Out of Office - Admin", 0, "hi.me", "2016-11-02","2016-11-08",30.50, 0],["Easting", 0, "hi.me", "2016-11-02","2016-11-08", 0]]
        self.assertCountEqual(tock_blocks.get_entries_in_time_period("2016-11-01", "2016-11-30", test_entries, 'util'), result)

    def get_entries_in_time_period_tock_blocks(self):
        test_entries = [["Out of Office - Other", 0, "hi.me", "2016-10-02","2016-10-08",30.50, 0], ["Out of Office - Admin", 0, "hi.me", "2016-11-02","2016-11-08",30.50, 0], ["Out of Office - Other", 0, "hi.me", "2016-12-02","2016-12-08", 0], ["Easting", 0, "hi.me", "2016-11-02","2016-11-08", 0]]
        result = [["Out of Office - Admin", 0, "hi.me", "2016-11-02","2016-11-08",30.50, 0],["Easting", 0, "hi.me", "2016-11-02","2016-11-08", 0]]
        self.assertCountEqual(tock_blocks.get_entries_in_time_period("2016-11-01", "2016-11-30", test_entries, 'tb'), result)

    def test_create_project_dic(self):
        test_entries = [["meow", 0, 0, 0, 0, 5], ["meow", 0, 0, 0, 0, 5], ["tom", 0, 0, 0, 0, 3], ["travel", 0, 0, 0, 0, 5], ["box", 0, 0, 0, 0, 2], ["meow", 0, 0, 0, 0, 4]]
        result = {'meow': 14, "tom": 3, "travel": 5, "box":2}
        self.assertCountEqual(tock_blocks.create_project_dict(test_entries), result)

    def test_calc_project_perc(self):
        test_project_dict = {'meow': 3, 'travel': 5, 'eating': 6.25, 'toxic': 10.5}
        result = {'meow': 10, 'travel': 20, 'eating': 25, 'toxic': 40}
        self.assertEqual(tock_blocks.calculate_projects_percentage(test_project_dict, 24.75), result)

    def test_myRound(self):
        self.assertEqual(tock_blocks.myRound(32), 30)
        self.assertEqual(tock_blocks.myRound(33), 35)

    def test_reduce_dict_to_hours(self):
        test_project_dict = {'meow': 3, 'travel': 5, 'eating': 6.25, 'toxic': 10.5}
        self.assertEqual(tock_blocks.reduce_dict_to_hours(test_project_dict), 24.75)

    def test_reduce_dict_to_hours_fail(self):
        test_project_dict = [3, 5, 6.25, 10.5]
        self.assertRaises(IndexError, lambda: tock_blocks.reduce_dict_to_hours(test_project_dict))

    def test_blockify_projects(self):
        test_percentage_block = {'meow': 10, 'travel': 20, 'eating': 25, 'toxic': 40}
        result = [{'travel': 20}, {'eating': 25}, {'toxic': 40}, {'Other': [{'meow': 10}]}]
        self.assertCountEqual(tock_blocks.blockify_projects(test_percentage_block), result)

    # def test_block_by_array(self):

    def test_print_nice_markdown(self):
        test_block = [{'meow': 90}, {'Other': [{'cow': 5}, {'rut': 5}]}]
        markdown_result = "meow 90\n\n\n*Other*\n{'cow': 5}\n\n\n{'rut': 5}\n\n\n\n\n"
        capturedOutput = io.StringIO()                     # Create StringIO object
        sys.stdout = capturedOutput
        tock_blocks.print_nice(test_block, "markdown")
        self.assertEqual(capturedOutput.getvalue(), markdown_result)
        sys.stdout = sys.__stdout__

    def test_print_nice_pretty(self):
        test_block = [{'meow': 90}, {'Other': [{'cow': 5}, {'rut': 5}]}]
        pretty_result = "meow 90\n\033[1mOther\033[0m\n{'cow': 5}\n{'rut': 5}\n\n\n"
        capturedOutput = io.StringIO()                     # Create StringIO object
        sys.stdout = capturedOutput
        tock_blocks.print_nice(test_block, "pretty")
        self.assertEqual(capturedOutput.getvalue(), pretty_result)
        sys.stdout = sys.__stdout__

    def test_print_handler(self):
        capturedOutput = io.StringIO()                     # Create StringIO object
        sys.stdout = capturedOutput                        #  and redirect stdout.
        tock_blocks.print_handler("hi", "pretty", "bold")  # Call function.
        self.assertEqual(capturedOutput.getvalue(), "\033[1mOther\033[0m\n")
        sys.stdout = sys.__stdout__                    # Reset redirect.

    def test_print_handler_2(self):
        capturedOutput = io.StringIO()                     # Create StringIO object
        sys.stdout = capturedOutput                        #  and redirect stdout.
        tock_blocks.print_handler("hi", "pretty", "false")  # Call function.
        self.assertEqual(capturedOutput.getvalue(), "\033[95mhi\033[0m\n")
        sys.stdout = sys.__stdout__                    # Reset redirect.

    def test_print_handler_3(self):
        capturedOutput = io.StringIO()                     # Create StringIO object
        sys.stdout = capturedOutput                        #  and redirect stdout.
        tock_blocks.print_handler("hi", "markdown", "bold")  # Call function.
        self.assertEqual(capturedOutput.getvalue(), "*hi*\n")
        sys.stdout = sys.__stdout__                    # Reset redirect.

    def test_print_handler_4(self):
        capturedOutput = io.StringIO()                     # Create StringIO object
        sys.stdout = capturedOutput                        #  and redirect stdout.
        tock_blocks.print_handler("hi", "markdown", "false")  # Call function.
        self.assertEqual(capturedOutput.getvalue(), "## hi\n")
        sys.stdout = sys.__stdout__                    # Reset redirect.

    def test_print_handler_4(self):
        capturedOutput = io.StringIO()                     # Create StringIO object
        sys.stdout = capturedOutput                        #  and redirect stdout.
        tock_blocks.print_handler("hi", "coll", "false")  # Call function.
        self.assertEqual(capturedOutput.getvalue(), "hi\n")
        sys.stdout = sys.__stdout__                    # Reset redirect.
if __name__ == '__main__':
    unittest.main()
