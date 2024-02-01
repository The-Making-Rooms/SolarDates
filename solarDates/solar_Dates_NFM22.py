#Links
# https://www.mathsisfun.com/polar-cartesian-coordinates.html
# https://www.theplanetstoday.com/

import sys
import svgwrite
import datetime
import math
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import subprocess
from jplephem.spk import SPK
from math import atan2, degrees, sqrt, radians,cos, sin
import numpy
import julian

# Test
# printer = 'Canon MG3000 series XPS'
# driver = 'Canon MG3000 series XPS'
# port = 'A3C9E0000000'

# Large laser
printer = 'Epilog Engraver WinX64'
driver = 'Epilog Engraver WinX64'
port = 'USB0001'

'''
# Small laser
printer = 'Epilog Engraver WinX64'
driver = 'Epilog Engraver WinX64'
port = 'USB0003'
'''

inkscapePath = 'inkscape\\inkscape.exe'
#adobePath = 'C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe'
#adobePath = 'C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe'
adobePath = "C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"

pageWidth = 600
pageHeight = 400

badgesPerRow = 20


xOffset = 28.442
yOffset = 31.045

xStep = 50
yStep = 50

colourMode = False
lineMode = False

gotMoon = True
gotMoonOrbit = False

pendant = 0
coaster= 1
wallHanging = 2
mirror = 3

product = pendant

products = ["pendant", "coaster", "wallHanging", "mirror"]


pendantDiameter = 48.142
coasterDiameter = 95.0
wallHangingDiameter = 500.0
mirrorDiameter = 200


scales = [pendantDiameter, coasterDiameter, wallHangingDiameter, mirrorDiameter]

scaleFactor = scales[product]/pendantDiameter

#epoch = datetime.date(2019,1,20)
plutoDay = datetime.datetime(2006,8,24,0,0,0,0)

DIAMETER_INDEX = 0
DISTANCE_INDEX = 1
ORBIT_TIME_INDEX = 2
EPOCH_ANGLE_INDEX = 3
COLOUR_INDEX = 4
EARTH_INDEX = 2
PLUTO_INDEX = 8

'''
planetDetails = [[1.187,	6.356,		0.241,				277.93873571,	'grey'], 	# Mercury
				[1.513,		9.624,		0.615,				169.38347337,	'yellow'],	# Venus
				[2.5,		17.062,		1.0,				118.78267686,	'blue'], 			# Earth
				[1.332,		24.310,		1.8811610076670,	52.5773278,		'red'], 		# Mars
				[4.0,		30.210,		11.85925520262869,	248.00283466,	'orange'], 	# Jupiter
				[2.8,		37.578,		29.42771084337349,	281.80742938,	'gold'], 		# Saturn
				[2.0,		42.946,		83.759583789704,	31.30463752,	'blue'], 		# Uranus
				[1.959,		47.472,		163.74589266155,	345.63498378,	'blue'], 	# Neptune
				[1.0,		51.000,		247.97371303395,	290.73281424,	'brown']] 	# Pluto
Moon = 			[0.8,		4.548,		0.0748493150684932,	107,			'white']

sunDiameter = 4.6
'''


				#diameter,		dist dia, 	orbit time, 			epoch angles,	colour
planetDetails = [	[0.577, 	3.94,		0.241,					277.93873571,	'grey'], 	# Mercury
					[0.85, 		5.479,		0.615,					169.38347337,	'yellow'],	# Venus
					[0.98, 		9.12,		1.0,					118.78267686,	'blue'], 	# Earth
					[0.77, 		13.03,		1.8811610076670,		52.5773278,		'red'], 	# Mars
					[2.08, 		21.23,		11.85925520262869,		248.00283466,	'orange'], 	# Jupiter
					[1.694, 	26.735,		29.42771084337349,		281.80742938,	'gold'], 	# Saturn
					[1.2, 		36.105,		83.759583789704,		31.30463752,	'blue'], 	# Uranus
					[1.12, 		42.12,		163.74589266155,		345.63498378,	'blue'], 	# Neptune
					[0.77, 		44.45,		247.97371303395,		290.73281424,	'brown']] 	# Pluto
Moon = 				[0.6, 		2.0,		0.0748493150684932,		107,			'white']

sunDiameter = 2.425
# From: https://nssdc.gsfc.nasa.gov/planetary/factsheet/planet_table_ratio.html
# Pluto death August 24, 2006


#earthSize = 2.5
#earthDistance = .9
#earthEpochAngle = planetDetails[ORBIT_TIME_INDEX][EPOCH_ANGLE_INDEX]
#earthYearDays = 365.0 # 365.2422 - calendar leap years should handle the discrepancy
fullCircle = 360.0


#moonYearDays = 365 * Moon[ORBIT_TIME_INDEX]
#moonDayShift = fullCircle / (earthYearDays * Moon[ORBIT_TIME_INDEX])


#Input format: YYYY-M-D

#date_given = datetime.date(1990,3,4)

class DateFile():
	badgeNumber = 0
	printPage = 1

	def __int__(self):
		badgeNumber = 0
		printPage = 1


	def createFile(self, DOBString):
		#date_given_string = sys.argv[1]
		#date_given_array = date_given_string.split('-')
		date_given_array = DOBString.split('-')
		print(date_given_array)
		fileName = DOBString #+ "-" + products[product] 
		date_given = datetime.datetime(int(date_given_array[0]), int(date_given_array[1]), int(date_given_array[2]),0,0,0,0)
		# todo SVG\ will not save in a folder on UNIX OS
		dwg = svgwrite.Drawing('SVGS\\' + fileName + '.svg', profile='tiny',size=(str(pageWidth)+"mm",str(pageHeight)+"mm"),viewBox=('0 0 '+ str(pageWidth)+" "+ str(pageHeight)))


		#deltaDays = (date_given - epoch).days
		#deltaDays = 0
		#print("Days since epoch: " + str(deltaDays))

		if (date_given - plutoDay).days > 0:
			# No pluto
			gotPluto = False
		else:
			#Pluto
			gotPluto = True

		#print(deltaDays)

		xShift = xOffset +( (self.badgeNumber % badgesPerRow) * xStep )
		yShift = yOffset + ( int(self.badgeNumber/badgesPerRow) * yStep )

		xOutlineShift = int(self.badgeNumber % badgesPerRow) * xStep
		yOutlineShift = int(self.badgeNumber/badgesPerRow) * yStep

		kernel = SPK.open('de430.bsp') #EDDIE get open data
		Astro_date = julian.to_jd(date_given, fmt='jd') #EDDIE convert given date to Astro Julian Date

		for i, planet in enumerate(planetDetails):
			if i != PLUTO_INDEX  or gotPluto:
				if colourMode:
					planetColour = planet[4]
				else:
					planetColour = 'black'
				# 360 takes earth 365.2 to do and  orbital period is in relation to how long it takes the earth to days
				position = kernel[0,i+1].compute(Astro_date) #compute x,y,z position for plant
				planetAngle = 180 + degrees(atan2(position[1],-position[0])) #calculate polar angle

				#planetDayShift = fullCircle / (earthYearDays * planet[ORBIT_TIME_INDEX])
				#planetAngle = (planet[EPOCH_ANGLE_INDEX] + (planetDayShift * deltaDays))%360
				# planetDistance = ((((planet[1]*earthDistance) - closestPlanet) * (maxDistance - minDistance)) / (farthestPlanet - closestPlanet)) + minDistance
				planetDistance = (planet[DISTANCE_INDEX]/2.0)*scaleFactor
				x = (planetDistance * cos(radians(planetAngle))) + xShift # calculate x co-ord from polar angle
				y = (planetDistance * sin(radians(planetAngle))) + yShift # calculate y co-ord from polar angle
				planetDiameter = (planet[DIAMETER_INDEX]/2.0)*scaleFactor
				if i == EARTH_INDEX: # i == earth
					if gotMoon:
						Moon_to_earth_position = kernel[3,301].compute(Astro_date)
						moonAngle = 180 + degrees(atan2(Moon_to_earth_position[1],-Moon_to_earth_position[0]))

						#moonAngle = (Moon[EPOCH_ANGLE_INDEX] + (moonDayShift *deltaDays))%360
						moonDistance = (Moon[DISTANCE_INDEX]/2.0)*scaleFactor
						moonRadius = (Moon[DIAMETER_INDEX]/2.0)*scaleFactor
						moonX = ( moonDistance* cos(radians(moonAngle))) + x
						moonY = (moonDistance * sin(radians(moonAngle))) + y
						if gotMoonOrbit:
							dwg.add(dwg.circle(center=(x, y), r=moonDistance,stroke='red', fill='none', stroke_width='0.01')) # moon orbit
						dwg.add(dwg.circle(center=(moonX,moonY), r=moonRadius, stroke='none', fill= 'black')) # moon

					dwg.add(dwg.circle(center=(xShift,yShift), r=planetDistance,stroke='red', fill='none', stroke_width='0.01')) #,sodipodi_start='0', sodipodi_end='6.1086524', sodipodi_open='true')) # earth orbit
					dwg.add(dwg.circle(center=(x,y), r=planetDiameter, stroke='none', fill= 'black')) # earth

				else:
					dwg.add(dwg.circle(center=(xShift,yShift), r=planetDistance,stroke='red', fill='none', stroke_width='0.01')) # planet orbit
					dwg.add(dwg.circle(center=(x,y), r=planetDiameter, stroke='none', fill= 'black')) # planet
					#print(i)

		# Draw sun
		if colourMode:
			planetColour = 'yellow'
		else:
			planetColour = 'black'

		if lineMode:
			dwg.add(dwg.circle(center=(xShift,yShift), r=(sunDiameter/2)*scaleFactor, stroke='none', fill='black')) # sun
		else:
			dwg.add(dwg.circle(center=(xShift,yShift), r=(sunDiameter/2)*scaleFactor, stroke='none', fill=planetColour)) # sun

		#dwg.add(dwg.circle(center=(13.379 + xOutlineShift,4.955 + yOutlineShift), r=1.5, stroke='black', fill='none', stroke_width='0.01')) #necklace hole left
		#dwg.add(dwg.circle(center=(43.506 + xOutlineShift,4.955 + yOutlineShift), r=1.5, stroke='black', fill='none', stroke_width='0.01')) #necklace hole right

		dwg.save()
		f = open('SVGS\\' + fileName + '.svg', "r")
		l = f.readlines()
		f.close()

		#print("File generated:")
		#print(DOBString + '.svg')
		l[-1] = l[-1].replace("</svg>", "")

		if product == pendant:
		# (OLD CODE INJECTION) codeInjection = '<path style="fill:none;stroke:#FFFFFF;stroke-width:0.01;stroke-miterlimit:4;stroke-dasharray:none" d="m ' + str(13.286644+ xOutlineShift) + ',' + str(1.4528396 + yOutlineShift) + ' c -0.563945,0.015233 -1.133298,0.1677693 -1.658055,0.470738 -1.6792239,0.9695 -2.2505249,3.1020183 -1.281025,4.7812415 l 1.77767,3.0785375 a 26.819786,26.819786 0 0 0 -10.5028569,21.2620274 26.819786,26.819786 0 0 0 26.8199319,26.819933 26.819786,26.819786 0 0 0 26.819932,-26.819933 26.819786,26.819786 0 0 0 -10.510574,-21.2487982 l 1.785388,-3.0917667 c 0.969499,-1.6792232 0.398199,-3.8117415 -1.281026,-4.7812415 -1.679222,-0.96950004 -3.811742,-0.398199 -4.78124,1.2810242 l -1.772708,3.0708207 a 26.819786,26.819786 0 0 0 -10.259772,-2.0499698 26.819786,26.819786 0 0 0 -10.252604,2.0620963 l -1.779875,-3.0829472 c -0.666531,-1.1544659 -1.882507,-1.7852744 -3.123186,-1.7517622 z" id="circle4178" inkscape:connector-curvature="0" /> </svg>'
			codeInjection1 = '<g id="g3335" transform="matrix(0.28222224,0,0,0.28222224,' + str(xOutlineShift+ 10.78138) +',' + str(yOutlineShift + 53.892362)+')"> <path sodipodi:nodetypes="ccsccscc" inkscape:connector-curvature="0" id="path3915-4" d="m 133.31496,-145.73946 c 0.007,-0.007 0.0147,-0.0147 0.0221,-0.0221 -0.14678,-1.62281 -0.81687,-3.12496 -2.09923,-4.39732 -1.29062,-1.28058 -2.76421,-1.91884 -4.39732,-2.05503 l -19.79899,-1.67938 c 5.66881,3.46218 11.00545,7.64669 15.9099,12.55115 4.71922,4.71922 8.79166,9.83755 12.1755,15.26908 z" style="fill:none;stroke:#FFFFFF;stroke-width:0.10629921;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1" /> <path sodipodi:nodetypes="csssccscc" inkscape:connector-curvature="0" id="path3917-3" d="m 147.5189,-88.646512 c 2.18886,24.198895 -5.92637,49.156955 -24.38552,67.761325 -33.179672,33.44079 -87.186935,33.67345 -120.6276301,0.4937 -33.4406839,-33.17968 -33.6517699,-87.208513 -0.472099,-120.649203 18.4809491,-18.62634 43.4212131,-26.94026 67.6710161,-24.91812 l 57.870663,4.86316 c 3.62616,0.30239 7.16913,1.83684 9.96356,4.60947 2.79808,2.7763 4.36074,6.31347 4.68895,9.94194 z" style="color:#000000;display:inline;overflow:visible;visibility:visible;fill:none;stroke:#000000;stroke-width:0.10629921;stroke-linecap:round;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1;enable-background:accumulate" /></g> </SVG>'
			l.append(codeInjection1)
			#l.append(codeInjection2)


		else:
			dwg.add(dwg.circle(center=(xShift,yShift), r=scales[product], stroke='black', fill='none', stroke_width='0.01'))
		f = open('SVGS\\' + fileName + '.svg', "w")
		content = "".join(l)
		#print(content)
		print('Generated SVG...')
		f.write(content)
		f.close()

		# create PDF
		#command = '"' + inkscapePath + '" -z -f --export-text-to-path --export-type=\"png\" SVGS\\' + fileName + '.svg -A PNGS\\' + DOBString + '.png'
		command = "inkscape --export-type=\"png\" -D -w 1200 SVGS\{}.svg --export-filename PNGS\{}.png".format(fileName, fileName)
		print(command)
		subprocess.call(command)
		if self.printPage:
			# literal
			# printCommand = '"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe" /t /h /o /s PDFS\\'+ DOBString + '.pdf "Canon MG3000 series XPS" "Canon MG3000 series XPS" "A3C9E0000000"'
			# variable
			printCommand = '"' + adobePath + '" /t /h /o /s PDFS\\'+ fileName + '.pdf "' + printer + '" "' + driver + '" "' + port + '"'
			#print(printCommand)
			#subprocess.Popen(printCommand,shell=True)

		#self.badgeNumber+=1
		print(self.badgeNumber)


if __name__ == "__main__":
	dobFile = DateFile()

	if len(sys.argv) > 1:
		bn = int(sys.argv[1])
		printOut = 1#int(sys.argv[2])
		dobFile.badgeNumber = bn
		dobFile.printPage = printOut
	while True:
		DOB = input("Type your DOB: 1990-03-04\n")
		dobFile.createFile(DOB)
