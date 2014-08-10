import requests
from lxml import html
from bs4 import BeautifulSoup

from .errors import BadRequestError

RMPROFESSOR_URL = u'http://www.ratemyprofessors.com/SelectTeacher.jsp?sid=269&pageNo='


def grab_professors():

	last_page = 57
	for page_number in xrange(1, last_page):
		soup = BeautifulSoup(_grab_html(page_number))


def _grab_html(page_number):
	try:
        page = requests.get(url + unicode(page_number))
        page.raise_for_status()
    except requests.exceptions.HTTPError:
        # http request to course list page failed
        raise BadRequestError(
            unicode(page.status_code) + u"can't access page number" + unicode(page_number))
    return page.text


# dictionary used to return the right key for each professor entry
professor_dict = {
	'0': 'NAME',
	'1': 'AVG',
	'2': 'EASY'
}


# gets the correct field 
def getKey(index):
	return professor_dict[str(index)]


# parses the current page on ratemyprofessor for the professor name, average, and easiness fields
# and constructs a dictionary for each professor
#
# collection: iterator returned by some soup.find_all() that you would like to get the info for
def scrape(professor_list):
	count = 0

	new_entry = {}

	# iterate over each professor
	for professor in professor_list:
		# iterate over desired children fields of each professor
		for child in professor.findChildren('div', {'class': ['profName', 'profAvg', 'profEasy']}):
			text = child.getText().strip()

			if not text.isspace():
				new_entry[getKey(count)] = text
				count += 1

			if count == 3:
				# print new_entry

				new_fields = {'AVG_RATING': new_entry['AVG'], 'EASYNESS': new_entry['EASY']}
				# result = collection.update({'INSTRUCTOR': new_entry['NAME']}, {'$set': new_fields}, upsert=True)
				result = collection.update({'INSTRUCTOR': new_entry['NAME']}, new_entry, upsert=True)

				if result['updatedExisting'] is False:
					print new_entry['NAME']
				# if new_entry['NAME'] is 'Saha, Margaret':
				# 	print found
				new_entry = {}
				count = 0



def main():



	url = 'http://www.ratemyprofessors.com/SelectTeacher.jsp?sid=269&pageNo='

	# iterate over each page of professors on the william and mary page
	for count in xrange(1, 57):
		page = requests.get(url + str(count))
		data = page.text

		soup = BeautifulSoup(data)

		scrape(soup.find_all('div', {'class': 'entry even vertical-center'}))
		scrape(soup.find_all('div', {'class': 'entry odd vertical-center'}))
