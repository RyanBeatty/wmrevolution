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
from argparse import ArgumentParser
from lxml import html
from bs4 import BeautifulSoup

from .errors import BadRequestError

COURSELIST_URL = u'https://courselist.wm.edu/courseinfo/searchresults'

 
def _retrieve_courselist_html(term_code):
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

def _get_course_fields(soup):
    return [field.string.strip() for field in soup.find_all(u'th')]

def grab_courses(soup):
    course_fields = _get_course_fields(soup)
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




# from bson.objectid import ObjectId

# dictionary used to get key field for each course
key_dict = {
    '0': 'CRN',
    '1': 'ATTRIBUTE',
    '2': 'COURSE_ID',
    '3': 'TITLE',
    '4': 'INSTRUCTOR',
    '5': 'CREDIT_HOURS',
    '6': 'DAYS',
    '7': 'TIMES',
    '8': 'PROJ_ENR',
    '9': 'CUR_ENR',
    '10': 'AVAILABLE',
    '11': 'STATUS'
}

# returns the string key associated with each field in a course entry
# index: int between [0,11] used to get correct string key


def switch(index):
    return key_dict[str(index)]

# converts militray time to standard time
# time: time string formated in military time


def _format_time(time):

    if time >= 1300:
        return _format(str(time - 1200)) + u"PM"
    elif time >= 1200:
        return _format(str(time)) + u"PM"
    else:
        return _format(str(time)) + u"AM"

# formats the time field in each course entry


def _format(time):

    str_len = len(time)

    if str_len == 4:
        return time[:2] + u':' + time[2:]
    else:
        return time[:1] + u':' + time[1:]


def get_course_list(term_code):

    soup = BeautifulSoup(_retrieve_courselist_html(term_code))

    field_count = 0         # used to keep track of current field
    course_count = 0        # used to keep track of total number of courses
    course = {}              # used to store each courses' fields

    # course_fields = [
    #     u'CRN',
    #     u'ATTRIBUTE',
    #     u'COURSE_ID',
    #     u'TITLE',
    #     u'INSTRUCTOR',
    #     u'CREDIT_HOURS',
    #     u'DAYS',
    #     u'TIMES',
    #     u'PROJ_ENR',
    #     u'CUR_ENR',
    #     u'AVAILABLE',
    #     u'STATUS'
    # ]
    # course_fields = _get_course_fields(soup)
    # courses = []
    # course = {}
    # count = 0
    # for field in soup.find_all(u'td'):
    #     if count == 12:
    #         courses.append(course)
    #         course = {}
    #         count = 0
    #     field_key = course_fields[count]
    #     course[field_key] = field.text.strip()
    #     count += 1

    courses = grab_courses(soup)
    return courses

    



    # # iterate over all entries in the open course list table
    # for link in soup.find_all(u'td'):

    #     # strip the text of extraneous characters
    #     text = link.getText().strip()

    #     # if the text is not whitespace/newline/tab, process text
    #     if not text.isspace():
    #         # get entry key string
    #         key = switch(field_count)

    #         # if we are processing a courses' time info, convert time to
    #         # standard time
    #         if key is 'TIMES':
    #             time = text.split('-', 2)

    #             try:
    #                 time_a = convert2Standard(int(time[0]))
    #                 time_b = convert2Standard(int(time[1]))

    #                 entry[key] = time_a + '-' + time_b
    #             except ValueError:
    #                 entry[key] = text

    #         # else just add the text to the course dict
    #         else:
    #             entry[key] = text

    #         field_count += 1

    #     # if we have built a full course entry
    #     if field_count == 12:
    #         # print the entry (change to insert to a database)
    #         print entry

    #         # reset the current field count and entry and increment the course
    #         # count
    #         field_count = 0
    #         course_count += 1
    #         entry = {}

    # print 'number of courses: ' + str(course_count)
    # print 'done'


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-t', '--term-code',
                        required=True,
                        help='term code for semester you wish to get class info from '
                             'can be found by inspecting <https://courselist.wm.edu/> source')

    args = parser.parse_args()

    print get_course_list(args.term_code)
    # _get_text(args.term_code)
    # main()
