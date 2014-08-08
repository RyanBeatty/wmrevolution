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

COURSELIST_URL = 'https://courselist.wm.edu/courseinfo/searchresults'

 
def _get_text(term_code):
    payload = {
        "term_code": str(term_code),
        "term_subj": "0",
        "attr": "0",
        "levl": "0",
        "status": "0"
    }

    page = requests.post(COURSELIST_URL, data=payload)
    try:
        page.raise_for_status()
    except requests.exceptions.HTTPError:
        raise BadRequestError("can't access course list. check term code")
    return page.text


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


def convert2Standard(time):

    if time >= 1300:
        return formatTime(str(time - 1200)) + "PM"
    elif time >= 1200:
        return formatTime(str(time)) + "PM"
    else:
        return formatTime(str(time)) + "AM"

# formats the time field in each course entry


def formatTime(time):

    str_len = len(time)

    if str_len == 4:
        return time[:2] + ':' + time[2:]
    else:
        return time[:1] + ':' + time[1:]


def main(term_code):

    # form payload needed to access all courses
    # payload = {
    #   "term_code": "201510",
    #   "term_subj": "0",
    #   "attr": "0",
    #   "levl": "0",
    #   "status": "0"
    # }

    # submit form and construct BS parser from html
    # page = requests.post(url, data=payload)
    # data = page.text
    soup = BeautifulSoup(_get_text(term_code))

    field_count = 0         # used to keep track of current field
    course_count = 0        # used to keep track of total number of courses
    entry = {}              # used to store each courses' fields

    # iterate over all entries in the open course list table
    for link in soup.find_all('td'):

        # strip the text of extraneous characters
        text = link.getText().strip()

        # if the text is not whitespace/newline/tab, process text
        if not text.isspace():
            # get entry key string
            key = switch(field_count)

            # if we are processing a courses' time info, convert time to
            # standard time
            if key is 'TIMES':
                time = text.split('-', 2)

                try:
                    time_a = convert2Standard(int(time[0]))
                    time_b = convert2Standard(int(time[1]))

                    entry[key] = time_a + '-' + time_b
                except ValueError:
                    entry[key] = text

            # else just add the text to the course dict
            else:
                entry[key] = text

            field_count += 1

        # if we have built a full course entry
        if field_count == 12:
            # print the entry (change to insert to a database)
            print entry

            # reset the current field count and entry and increment the course
            # count
            field_count = 0
            course_count += 1
            entry = {}

    print 'number of courses: ' + str(course_count)
    print 'done'


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('-t', '--term-code',
                        required=True,
                        help='term code for semester you wish to get class info from '
                             'can be found by inspecting <https://courselist.wm.edu/> source')

    args = parser.parse_args()

    _get_text(args.term_code)
    # main()
