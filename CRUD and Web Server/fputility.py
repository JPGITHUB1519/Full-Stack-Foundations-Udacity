import re
user_check = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
password_check = re.compile(r"^.{3,20}$")
email_check = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def validateUsername(username):
	""" Validate Username"""
	return user_check.match(username)

def validatePassword(password):
	""" Validate Username"""
	return password_check.match(password)

def validateEmail(email):
	return email_check.match(email)
