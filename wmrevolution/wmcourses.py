# -*- coding: <urf-8> -*-

import requests
import datetime
from argparse import ArgumentParser
from lxml import html
from bs4 import BeautifulSoup

from .errors import BadRequestError

COURSELIST_URL = u'https://courselist.wm.edu/courseinfo/searchresults'


def grab_courses(term_code, prettify=None):
    soup = BeautifulSoup(_grab_courselist_html(term_code))
    courses = _grab_raw_courses(soup)
    if prettify:
        courses = map(prettify, courses)
    return courses


def prettify(course):
    course_time_key = u'MEET TIMES'
    if course_time_key in course:
        course_time = course[course_time_key]
        course[course_time_key] = format_time(course_time)
    return course


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
