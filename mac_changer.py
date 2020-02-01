import re
import subprocess
import string
import random
import sys

mac_alphabets = []
#hex_letters = string.ascii_lowercase[:6]
hex_letters = ['a', 'c', 'e', 'f']
def macGenerator():
	no_of_alphanumeric = random.randrange(1,5)
	no_of_numericals = 6 - no_of_alphanumeric 
	for i in range(0, no_of_alphanumeric):
		random_alpha = str(random.randrange(0,9)) + str(random.choice(hex_letters))
		mac_alphabets.append(random_alpha)
	for i in range(0, no_of_numericals):
		random_num = random.randrange(10, 99, 2)
		mac_alphabets.append(str(random_num))
	random.shuffle(mac_alphabets)
	
			
def originalMac(interface):
	try:
		ifconfig_output = subprocess.check_output("ifconfig " + str(interface), shell=True)
		original_mac = re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_output))
		return original_mac.group(0)
	except subprocess.CalledProcessError:
		print("There was an error running the command")
		sys.exit()

def macChanger(interface, mac_digits, random):
	if random is True:
		mac_address = ":".join(mac_digits)	
	else:
		mac_address = mac_digits
	print("Original Mac Address : " + str(originalMac(interface)))
	print("Changing the Mac Address .....")
	subprocess.run(["ifconfig " + str(interface) + " down"], shell=True)
	subprocess.run(["ifconfig " + str(interface) + " hw ether " + str(mac_address)], shell=True)
	subprocess.run(["ifconfig " + str(interface) + " up"], shell=True)
	print("New Mac Address : " + str(mac_address)) 


interface = input("Enter the name of the interface : ")
try:
	result_of_command = subprocess.check_output("ifconfig " + str(interface), stderr=subprocess.STDOUT, shell=True)
except subprocess.CalledProcessError:
	print("The interface could not be detected, Please input a correct interface")
	sys.exit(0)
	
while True:
	print("1.) Generate a random Mac Address")
	print("2.) Enter a Mac Address")
	choice = input("Choose an option : ")
	if choice == '1':
		macGenerator()
		macChanger(interface, mac_alphabets, True)
		break;
	if choice == '2':
		manual_mac = input("Enter the mac address (xx:xx:xx:xx:xx:xx) -> ")
		reg = re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", manual_mac)
		if reg is None:
			print("Enter a correct mac address in format xx:xx:xx:xx:xx:xx")
		else:
			macChanger(interface, manual_mac, False)
			break;
	if choice != '1' or choice != '2':
		print("Please enter correct option")







