#!/usr/bin/python

import sys, os, xmpp

def messageCB(conn, msg):
	pass

#defining the presence notification handler
def presenceCB(conn, msg):
	#get the sender of presence notification
	cur = str(msg.getFrom())
	
	#extract the username
	cur = cur.partition('@')[0]
	
	#flag -> boolean variable which keeps track of whether the friend has been wished
	flag = 0
	
	#wishedlist -> file containing usernames of friends already wished
	fR = open('./wishedlist', 'r')
	#loop through the contents of the file to check if the friend has already been wished
	for line in fR:
		if line.strip() == cur:
			flag = 1
	fR.close()

	if flag == 0:
		fW = open('./wishedlist', 'a')
		
		#the message you want to send to your friends
		msg = "Happy new year to you and your family! :)"
		recipient = cur + '@gmail.com'

		message = xmpp.protocol.Message(recipient, msg)
		#type of message = chat
		message.setAttr('type', 'chat')
	
		#send the message
		conn.send(message)
		#add the friend to the list of wished ppl
		fW.write(cur + '\n')
	return

def StepOn(conn):
	try:
		conn.Process(1)
	except KeyboardInterrupt:
		return 0
	return 1

def GoOn(conn):
	while StepOn(conn):
		pass
	conn.disconnect()
	return

def main():
	#obtaining login credentials of the gmail account
	uname = raw_input()
	pwd = raw_input()
		
	jid = uname + '@gmail.com'
	jid = xmpp.protocol.JID(jid)
	
	cl = xmpp.Client(jid.getDomain())
	
	if cl.connect() == "":
		print "Not connected!"
		sys.exit(0)
	
	if cl.auth(uname, pwd, 'bot') == None:
		print "Authentication failed"
		sys.exit(0)
	
	#message call back handler
	cl.RegisterHandler('message', messageCB)
	#presence notification call back handler
	cl.RegisterHandler('presence', presenceCB)
	#notifying your subscribers about your presence
	cl.sendInitPresence()

	#keep running
	GoOn(cl)
	return

main()
