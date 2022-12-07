#!/usr/bin/env python3
import getopt
import getpass
import signal
import time
from sys import argv
from random import randint,choice
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
# from quickstart import sendGmail,sendGmailWithAttachments

def sig_int(signal, frame, sender, reciever):
	print('quiting...')
	sendGmail(sender,reciever,"quiting","")
	driver.quit()
	exit()

def setup():
	helpmsg = '''
Options:
  -n  SECONDS		 refresh the website every SECONDS seconds (default: 3)
  --no-sign-in		 the script will not try to sign in the course'''
	sec = 100
	need_sign_in = True
	try:
		opts, args = getopt.getopt(argv[1:], 'n:', ['help','no-sign-in'])
		for opt, arg in opts:
			if opt == '--help':
				print(helpmsg)
				exit()
			elif opt == '-n':
				sec = arg
			elif opt == '--no-sign-in':
				need_sign_in = False
	except getopt.GetoptError:
		print(helpmsg)
		exit(1)
	
	if len(args) > 1:
		print('Error: too many urls')
		print(helpmsg)
		exit(2)
	elif len(args) < 1:

# ---------------------------------------------------------------------------- #
#                             Enter Your Course ID                             #
# ---------------------------------------------------------------------------- #

		# print('Error: missing the url, set course "自動化測試實習" as default')
		# url = "https://irs.zuvio.com.tw/student5/irs/clickers/504929"
		print('Error: missing the url, set course "國防政策" as default')
		# url = "https://irs.zuvio.com.tw/student5/irs/clickers/725547"
		url = "https://irs.zuvio.com.tw/student5/irs/rollcall/981470"
		# url = "https://irs.zuvio.com.tw/student5/irs/clickers/981470"
		print(helpmsg)
	else:
		url = args[0]

	return sec, need_sign_in, url


sec, need_sign_in, url = setup()

# ---------------------------------------------------------------------------- #
#                            Enter Your Account Here                           #
# ---------------------------------------------------------------------------- #

# email = input('Enter your email: ')
# email = "YOUR ACCOUNT"
email = "b07207073@ntu.edu.tw"
# password = getpass.getpass()
# password = "YOUR PASSWORD"
password = "123"

# options = webdriver.firefox.options.Options()
# options.add_argument('--headless') #hide the browser window

# ---------------------------------------------------------------------------- #
#                              Enter Your Location                             #
# ---------------------------------------------------------------------------- #

params = {
    "latitude": 25.018469,
    "longitude": 121.536851,
    "accuracy": 100
}
chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome()#chrome_options=chrome_options
driver.execute_cdp_cmd("Page.setGeolocationOverride", params)
driver.get('https://irs.zuvio.com.tw')

# signal.signal(signal.SIGINT, sig_int)

login = False
while not login:
	# driver.find_element_by_id('email').send_keys(email)
	driver.find_element("id", "email").send_keys(email)
	# driver.find_element_by_id('password').send_keys(password)
	driver.find_element("id", "password").send_keys(password)
	driver.find_element("id", 'login-btn').click()
	driver.implicitly_wait(1)
	try:
		driver.find_element("id", 'login_btn')
	except NoSuchElementException: #if it does not exist the login button, which means you have logged in
		login=True
	else:
		print('Wrong email or password. Please try again.')
		email = input('Enter your email: ')
		password = getpass.getpass()

del password
print('Logged in successfully')

# ---------------------------------------------------------------------------- #
#                           Enter Your Email Address                           #
# ---------------------------------------------------------------------------- #

# sender = "Your Email Address"
sender = "jay25262753@gmail.com"
# reciever = "Your Email Address"
reciever = "jay25262753@gmail.com"
# sendGmail(sender,reciever,'Logged in successfully',"")
# ---------------------------------------send email------------------------
driver.get(url)

signed_in = not need_sign_in
sign_in_url=url.replace('clickers','rollcall')


recurssive = True
while recurssive or not signed_in:			
	if recurssive or not signed_in:
		driver.get(sign_in_url)
		time.sleep(sec)
		try:			
			driver.save_screenshot("The_shot.png")
			driver.find_element("id", 'submit-make-rollcall').click()
			print(str(datetime.now().time())[:8]+' signed in')
			# time.sleep(5)
			# driver.save_screenshot("The shot_2.png")
			# sendGmailWithAttachments(sender,reciever,'Signed in',str(datetime.now().time())[:8]+' signed in',"The_shot.png")
			# signed_in = True

		except NoSuchElementException:
			print(str(datetime.now().time())[:8]+"not started yet")
			# sendGmail(sender,reciever,'NO such element',"")
			pass
	try:
		driver.refresh()
	except:
		print('{{{'+str(datetime.now().time())[:8]+'}}} connection timeout')
		# sendGmail(sender,reciever,"CONNECTION ERROR","")
		time.sleep(30)
		continue
