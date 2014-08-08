import unittest
from wmrevolution import wmcourses, errors

class WMCoursesTestCase(unittest.TestCase):

	def test_bad_status_code(self):
		with self.assertRaises(errors.WMRevolutionError):
			wmcourses._retrieve_courselist_html(10000000)