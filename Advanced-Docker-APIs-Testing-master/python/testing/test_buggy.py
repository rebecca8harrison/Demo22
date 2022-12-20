'''
Example unit tests for the buggy code
'''
import io
import unittest

import testing.buggy_doctests as buggy


class BuggyTests(unittest.TestCase):
  '''
  Example behavioural tests of the buggy code
  '''

  def test_format_charge_formats_integer_values(self):
    # we don't have to assign to expected and actual variables
    # but it can be helpful for readability, especially for more complex values
    expected = '£1.00'
    actual = buggy.format_charge(1)
    self.assertEqual(expected, actual)

  def test_format_charge_formats_float_values(self):
    self.assertEqual('£1.00', buggy.format_charge(0.01))

  def test_main_on_sample_input(self):
    sales = io.StringIO('''
x,y,rate,campaign_name,Y
2,3,r,d1,1
3,9,r,d1,1
4,8,r,d1,0
5,9.8,s,d2,1
''')

    rates = io.StringIO('''
rate,val
r,0.5
s,1.0
''')

    expected = '''x,campaign,charge
2,d1,£1.50
3,d1,£4.50
4,d1,£4.00
5,d2,£9.80
'''

    actual = io.StringIO()

    buggy.main(sales, rates, actual)

    self.assertEqual(actual.getvalue(), expected)

  def test_apply_rates_on_sample_input(self):
    # you could write another test here to debug a smaller part of the code
    pass
