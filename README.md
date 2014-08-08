# WMRevolution
Python module of useful and easy to use scripts for getting William & Mary data. Using wmrevolution you can get the list of all courses and course data 

## Installation
To install wmrevolution as a package in your python environment run 
```
python setup.py install
```

## Usage

### Course List
Getting a list of all courses and course data is easy:

```python
from wmrevolution import wmcourses

# term_code is code for semester you wish to get course list for.
# '20151' corresponds to the Fall 2014 Semester
# can be found be inspecting <https://courselist.wm.edu/>
term_code = '20151'
course_list = wmcourses.grab_courses(term_code)
```

This will give you a list of the courses, where each course is a dictionary containing that courses data.

### Data Transformations
There is also support for adding your own transformations to the course data while processing the courses. There is a built in method ```prettify``` that will convert all militarty course meetings times to standard time.

```python
from wmrevolution import wmcourses

# this will convert all meeting times for each course
# from military time (start_time-end_time) to 
# standard time (hh:mmAM/PM-hh:mmAM/PM)
#
# ex. '1000-1452' -> '10:00AM-2:52PM'
course_list = wmcourses.grab_courses('201510', wmcourses.prettify)
```

Adding your own custom transformation is simple. Just define your own function that takes and returns a course dictionary and pass it to ```grab_courses```:

```python
from wmrevolution import wmcourses

def my_transformation(course):
	# complex transformation here
	return course

course_list = wmcourses.grab_courses('201510', my_transformation)
```
