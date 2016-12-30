from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy
import datetime

engine = create_engine('sqlite:///puppyshelter.db')
# connection betweens classes and tables
Base.metadata.bind = engine
# creating session to connect databae
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Helper Methods
def passesLeapDay(today):
    """
    Returns true if most recent February 29th occured after or exactly 183 days ago (366 / 2)
    """
    thisYear = today.timetuple()[0]
    if isLeapYear(thisYear):
        sixMonthsAgo = today - datetime.timedelta(days = 183)
        leapDay = datetime.date(thisYear, 2, 29)
        return leapDay >= sixMonthsAgo
    else:
        return False
        
def isLeapYear(thisYear):
    """
    Returns true iff the current year is a leap year.
    Implemented according to logic at https://en.wikipedia.org/wiki/Leap_year#Algorithm
    """
    if thisYear % 4 != 0:
        return False
    elif thisYear % 100 != 0:
        return True
    elif thisYear % 400 != 0:
        return False
    else:
    	return True
def hw1():
	"""
	1. Query all of the puppies and return the results in 
	ascending alphabetical order
	"""
	puppies = session.query(Puppy).order_by(Puppy.name.asc()).all()
	for puppy in puppies :
		print str(puppy.id) + "\t" + puppy.name + "\t" + puppy.gender  + "\t" + str(puppy.dateOfBirth)

def hw2():
	"""
	2. Query all of the puppies that are less than 6 months 
	old organized by the youngest first
	"""
	today = datetime.date.today()
	if passesLeapDay(today):
		sixMonthsAgo = today - datetime.timedelta(days = 183)
	else:
		sixMonthsAgo = today - datetime.timedelta(days = 182)
		result = session.query(Puppy.name, Puppy.dateOfBirth)\
        .filter(Puppy.dateOfBirth >= sixMonthsAgo)\
        .order_by(Puppy.dateOfBirth.desc())
	# print the result with puppy name and dob
	for item in result:
		print "{name}: {dob}".format(name=item[0], dob=item[1])

def hw3():
	"""
	3. Query all puppies by ascending weight
	"""
	puppies = session.query(Puppy).order_by(Puppy.weight.asc()).all()
	for puppy in puppies :
		print str(puppy.id) + "\t" + puppy.name + "\t" + puppy.gender  + "\t" + str(puppy.weight)

def hw4():
	"""Query all puppies grouped by the shelter in which they are staying"""
	result = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
	for item in result:
		print item[0].id, item[0].name, item[1]
hw2()

