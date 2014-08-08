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

'''
term_code is code for semester you wish to get course list for
can be found be inspecting <https://courselist.wm.edu/>
'''
term_code = '20151'
course_list = wmcourses.grab_courses(term_code)
```

