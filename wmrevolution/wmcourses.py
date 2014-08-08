# -*- coding: <urf-8> -*-



##########################################################################
# wmcourselistscraper.py
# written by: Ryan Beatty
#
# This is a python script that will scrape the William and Mary's open course list
# for info and construct a dictionary for each course and print each dictionary
# to standard output. Simple modifications can be made to upload each entry
# to a database or write them to a file
##########################################################################

import requests
import datetime
from argparse import ArgumentParser
from lxml import html
from bs4 import BeautifulSoup

from .errors import BadRequestError

COURSELIST_URL = u'https://courselist.wm.edu/courseinfo/searchresults'

def grab_courses(term_code, target=None):

    soup = BeautifulSoup(_grab_courselist_html(term_code))
    courses = _grab_raw_courses(soup)
    if target:
        courses = map(target, courses)
    return courses

def format_time(course_time):

    def _to_datetime(raw_time):
        return datetime.time(
            hour=int(raw_time[0:2]), minute=int(raw_time[2:4]))

    try:
        times = course_time.split(u'-')
        times = map(_to_datetime, times)
        times = map(lambda t: t.strftime(u"%I:%M%p"), times)
        return u'-'.join(times)
    except ValueError:
        return course_time
 
def _grab_courselist_html(term_code):
    payload = {
        u"term_code": unicode(term_code),
        u"term_subj": u"0",
        u"attr": u"0",
        u"levl": u"0",
        u"status": u"0"
    }

    page = requests.post(COURSELIST_URL, data=payload)
    try:
        page.raise_for_status()
    except requests.exceptions.HTTPError:
        raise BadRequestError(u"can't access course list. check term code")
    return page.text

def _grab_course_fields(soup):
    return [field.string.strip() for field in soup.find_all(u'th')]

def _grab_raw_courses(soup):
    course_fields = _grab_course_fields(soup)
    courses = []
    course = {}
    count = 0

    for field in soup.find_all(u'td'):
        if count == 12:
            courses.append(course)
            course = {}
            count = 0
        field_key = course_fields[count]
        course[field_key] = field.text.strip()
        count += 1

    return courses

# def grab_courses(term_code, target=None):

#     soup = BeautifulSoup(_grab_courselist_html(term_code))
#     courses = _grab_raw_courses(soup)
#     if target:
#         courses = map(target, courses)
#     return courses

# def _format_time(time):

#     if time >= 1300:
#         return _format(str(time - 1200)) + u"PM"
#     elif time >= 1200:
#         return _format(str(time)) + u"PM"
#     else:
#         return _format(str(time)) + u"AM"

# def _format(time):

#     str_len = len(time)

#     if str_len == 4:
#         return time[:2] + u':' + time[2:]
#     else:
#         return time[:1] + u':' + time[1:]


# def grad_courses(term_code):

#     soup = BeautifulSoup(_grab_courselist_html(term_code))
#     courses = _grab_raw_courses(soup)
#     return courses


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-t', '--term-code',
                        required=True,
                        help='term code for semester you wish to get class info from '
                             'can be found by inspecting <https://courselist.wm.edu/> source')

    args = parser.parse_args()

    print grab_courses(args.term_code)
    # _get_text(args.term_code)
    # main()
