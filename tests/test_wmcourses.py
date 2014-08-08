import unittest
from wmrevolution import wmcourses, errors
from bs4 import BeautifulSoup
from os import path

HERE = path.abspath(path.dirname(__file__))


class WMCoursesTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_file = path.join(
            HERE, './fixtures/wmcourselist2014-08-08.html')

    def test_bad_status_code(self):
        with self.assertRaises(errors.WMRevolutionError):
            wmcourses._grab_courselist_html(10000000)

    def test_get_correct_course_fields(self):
        course_fields = [
            u'CRN',
            u'COURSE ID',
            u'COURSE ATTR',
            u'TITLE',
            u'INSTRUCTOR',
            u'CRDT HRS',
            u'MEET DAYS',
            u'MEET TIMES',
            u'PROJ ENR',
            u'CURR ENR',
            u'SEATS AVAIL',
            u'STATUS',
        ]
        with open(self.test_file) as f:
            soup = BeautifulSoup(str(f.readlines()))
            self.assertEqual(
                course_fields, wmcourses._grab_course_fields(soup))

    def test_military_to_standard_bad_times(self):
        self.assertEqual(wmcourses.format_time(u'2400-2430'), u'2400-2430')
        self.assertEqual(wmcourses.format_time(u'240-243'), u'240-243')
        self.assertEqual(wmcourses.format_time(u'1000-1060'), u'1000-1060')
        self.assertEqual(wmcourses.format_time(u'1000-'), u'1000-')
        self.assertEqual(wmcourses.format_time(u'-1000'), u'-1000')
        self.assertEqual(wmcourses.format_time(u'-1000'), u'-1000')

    def test_military_to_standard_time(self):
        self.assertEqual(
            wmcourses.format_time(u'0000-0030'), u'12:00AM-12:30AM')
        self.assertEqual(
            wmcourses.format_time(u'2300-0030'), u'11:00PM-12:30AM')
        self.assertEqual(
            wmcourses.format_time(u'1159-1200'), u'11:59AM-12:00PM')
        self.assertEqual(
            wmcourses.format_time(u'0100-0130'), u'01:00AM-01:30AM')
