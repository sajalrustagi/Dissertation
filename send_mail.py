# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 22:40:55 2015

@author: sajal
"""

import smtplib
from smtplib import SMTPException
#
#sender = 'from@fromdomain.com'
#receivers = ['to@todomain.com']
#
#message = """From: From Person <from@fromdomain.com>
#To: To Person <to@todomain.com>
#Subject: SMTP e-mail test
#
#This is a test e-mail message.
#"""

try:
   smtpObj = smtplib.SMTP('localhost')
   #smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"