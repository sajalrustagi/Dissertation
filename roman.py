# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 11:34:25 2015

@author: sajal
"""
import re
class RomanError(Exception): pass
class OutOfRangeError(RomanError): pass
class NotIntegerError(RomanError): pass
class InvalidRomanNumeralError(RomanError): pass

#Define digit mapping
romanNumeralMap = (('m',  1000),
				   ('cm', 900),
				   ('d',  500),
				   ('cd', 400),
				   ('c',  100),
				   ('xc', 90),
				   ('l',  50),
				   ('xl', 40),
				   ('x',  10),
				   ('ix', 9),
				   ('v',  5),
				   ('iv', 4),
				   ('i',  1))

def toRoman(n):
	"""convert integer to Roman numeral"""
	if not (0 < n < 5000):
		raise OutOfRangeError, "number out of range (must be 1..4999)"
	if int(n) <> n:
		raise NotIntegerError, "non-integers can not be converted"

	result = ""
	for numeral, integer in romanNumeralMap:
		while n >= integer:
			result += numeral
			n -= integer
	return result
 
romanNumeralPattern = re.compile("""
    ^                   # beginning of string
    m{0,4}              # thousands - 0 to 4 M's
    (cm|cd|d?c{0,3})    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                        #            or 500-800 (D, followed by 0 to 3 C's)
    (xc|xl|l?x{0,3})    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                        #        or 50-80 (L, followed by 0 to 3 X's)
    (ix|iv|v?i{0,3})    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                        #        or 5-8 (V, followed by 0 to 3 I's)
    $                   # end of string
    """ ,re.VERBOSE)

#print not romanNumeralPattern.search("udalgiri")
