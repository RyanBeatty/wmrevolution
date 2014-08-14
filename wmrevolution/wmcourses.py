# -*- coding: <urf-8> -*-

"""
wmcourses.py
by: Ryan Beatty

module for scrapping William and Mary's open course
list page and getting data for all courses. 
"""

import requests
import datetime
from argparse import ArgumentParser
from lxml import html
from bs4 import BeautifulSoup

from .errors import BadRequestError

COURSELIST_URL = u'https://courselist.wm.edu/courseinfo/searchresults'


def grab_courses(term_code, prettify=None):
    """
    Scrapes w&m open course list and returns
    list of courses contained in dictionaries.

    PRETTIFY: function that takes and returns
    a course and performs some data transformation
    on the course dictionary
    """
    soup = BeautifulSoup(_grab_html(term_code))
    courses = _grab_raw_courses(soup)
    if prettify:
        courses = map(prettify, courses)
    return courses


def prettify(course):
    """
    Default course prettify function.
    Converts a course's meet time from
    military to standard time
    """
    course_time_key = u'MEET TIMES'
    if course_time_key in course:
        course_time = course[course_time_key]
        course[course_time_key] = format_time(course_time)
    return course


def format_time(course_time):
    """
    Takes a military time (start_time-end_time) 
    and converts to standard time (hh:mmAM/PM-hh:mmAM/PM)
    """

    def _to_datetime(raw_time):
        return datetime.time(
            hour=int(raw_time[0:2]), minute=int(raw_time[2:4]))

    try:
        times = course_time.split(u'-')
        times = map(_to_datetime, times)
        times = map(lambda t: t.strftime(u"%I:%M%p"), times)
        return u'-'.join(times)
    except ValueError:
        # badly formated time. return original course_time
        return course_time


def _grab_html(term_code):
    """
    Returns wm open course list source html.
    TERM_CODE: code for term you wish to get
    course listing for (found by inspecting website)
    """
    payload = {
        u"term_code": unicode(term_code),
        u"term_subj": u"0",
        u"attr": u"0",
        u"levl": u"0",
        u"status": u"0"
    }

    try:
        page = requests.post(COURSELIST_URL, data=payload)
        page.raise_for_status()
    except requests.exceptions.HTTPError:
        # http request to course list page failed
        raise BadRequestError(
            u"status code: %s can't access course list. check term code" % page.status_code)
    return page.text


def _grab_fields(soup):
    """
    Return course fields in correct order
    """
    return [field.text.strip() for field in soup.find_all(u'th')]


def _grab_raw_courses(soup):
    """
    builds a list of dictionaries containing
    the inner text of all of the courses
    """
    course_fields = _grab_fields(soup)
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
