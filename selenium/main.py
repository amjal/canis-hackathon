from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import *
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import threading
from datetime import datetime
import numpy
import csv

class Agent:
	def __init__(self, username, password):
		self.username = username
		self.password = password
		options = self.driver_options()
		self.driver_lock = threading.Lock()
		self.driver = webdriver.Chrome(options=options)
		self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
		self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {	
			"source":	
				"const newProto = navigator.__proto__;"	
				"delete newProto.webdriver;"	
				"navigator.__proto__ = dogProto;"	
		})

	def driver_options(self):
		options = Options()
		options.add_argument("--start-maximized")
		options.add_argument("--no-sandbox")
		options.add_argument("--disable-blink-features=AutomationControlled")
		options.add_experimental_option("useAutomationExtension", False)
		options.add_experimental_option("excludeSwitches", ["enable-automation"])
#options.add_experimental_option("detach", True)
		return options

	def openTwitter(self):
		self.driver.get("https://www.twitter.com")
		WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/login"]'))).click()
		login = self.driver.find_element(By.CSS_SELECTOR, '')
		login.click()
		uname = browser.find_element_by_css_selector('input[name="text"]')
		uname.send_keys('amjal')
		print("Logged in")
		sleep(100)


	def login(self):
		self.driver.get("https://ts3.x1.america.travian.com/dorf1.php")
		uname = self.driver.find_element("name", "name")
		uname.send_keys(self.username)

		pswd = self.driver.find_element("name", "password")
		pswd.send_keys(self.password)
		WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.cmpboxbtn.cmpboxbtnyes.cmptxt_btn_yes'))).click()
		sleep(2)
		WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
		WebDriverWait(driver=self.driver, timeout=10).until(
			lambda x: x.execute_script("return document.readyState === 'complete'")
		)
		print("Waiting for page to fully load")
		sleep(5)
		print("Logged in")

	def start_module(self, module_name, parameter, village_no):
		try:
			module_cls = globals()[module_name]
			obj = module_cls(self.driver, self.driver_lock, parameter, village_no)
			# In the dictionary, the name of the class concatenated 
			# with the village number is stored as key so we can have
			# one module running for multiple villages
			module_name = module_name + village_no
			self.module_pool[module_name] = obj
			thread = threading.Thread(target=obj.run, daemon=True)
			thread.start()
		except KeyError:
			print("Cannot find class, try again")

	def stop_module(self, module_name, village_no):
		module_name = module_name + village_no
		self.module_pool[module_name].terminate()
		# The module object will stay in the module pool in case some 
		# staus is to be derived. It will be overwritten in the next creation 
		# of the module.

	def get_log(self, module_name):
		log = ""
		try:
			log = log + "###########################################################\n"
			log = log + "##################  "+module_name+"  ################################\n"
			obj = self.module_pool[module_name]
			log = log + obj.return_log()
		except KeyError:
			log = log + "Cannot find module, current modules are:\n"
			for name in self.module_pool.keys():
				log = log + name + "\n"
			log = log + "\n"
		return log
	
	def parse_command(self, command, *file_option):
		if len(command) == 0:
			return
		args = command.split(' ')
		if args[0] == "exit":
			# Terminate (and join with other threads?)
			exit(0)
		if args[0] == "start":
			if len(args) < 4:
				print ("Usage: start <class name> <avg sleep time> <village no>")
			else:
				self.start_module(args[1], int(args[2]), args[3])
		elif args[0] == "status":
			log = ""
			if len(args) == 2 and args[1] == "all":
				for mod_name in self.module_pool.keys():
					 log = log + self.get_log(mod_name)
			elif len(args) == 3:
				log = self.get_log(args[1] + args[2])
			else:
				log = "Usage: status <class name> <village no>\n		status all"
			if len(file_option) == 1:
			 	#File has been specified
				file = open(file_option[0], "a")
				file.write(log)
				file.close()	
			else:
				print(log)
		elif args[0] == "stop":
			if len(args) < 3:
				print ("Udage: stop <module name> <village no>")
			else:
				self.stop_module(args[1], args[2])
		else:
			print("Unknown command")


if __name__ == "__main__":
	agent = Agent('amjal', 'twittertwitting')
	agent.openTwitter()
