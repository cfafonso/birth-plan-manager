#-*- coding: utf-8 -*-


# This file records the constants used in the birth-plan-manager tool

# Constants related to time

# Value for the weekly pause
WKL_LEAVE = "weekly leave"

# Value for the duration of each assistance
ASSISTANCE_DURATION = '00h20'

# Value for the time increment in each update
FILE_TIME_INCREMENT = '00h30'

# Value for the daily break
DAILY_BREAK = '01h00'

# Value for the maximum working time in a week
MAX_WORK_TIME = '40h00'

# Value when a request is redirected to another hospital network
REDIRECTED_REQUEST = 'redirected to other network'

# Value for the closing time of the hospital
CLOSING_TIME = '20h00'

# Value for the opening time of the hospital
OPENING_TIME = '4h00'


# Constants related to file positions in the sys.argv list

# Index of the doctors file position when running the program
DOCTORS_FILE_INDEX = 1

# Index of the schedule file position when running the program
SCHEDULE_FILE_INDEX = 2

# Index of the requests file position when running the program
REQUESTS_FILE_INDEX = 3


# Constants related to the headers of files

# Scope of the doctors file
DOCTORS_FILE_SCOPE = 'Doctors'

# Scope of the schedule file
SCHEDULE_FILE_SCOPE = 'Schedule'

# Scope of the requests file
REQUESTS_FILE_SCOPE = 'Mothers'

# Number of header's lines
NUM_HEADER_LINES = 7


# Constants related to doctors

# Minimum required category for a doctor to be assigned to a high risk assistance
MIN_CATEG = 2