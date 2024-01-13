from turtle import Turtle, window_width, window_height, colormode, register_shape
from time import sleep, localtime, strftime
from math import sin, cos, atan, degrees as radToDeg, radians as degToRad, sqrt

shapePoints = ((-16,4),(-17.5,6),(-18,8),(-17.7,10),(-17,12),(-16,13.5),(-15.5,14),(-14,15.5),(-13,16),(-12,16.5),(-10,17),(-8,17),(-6,16.5),(-10,10),(-3.5,6),(-2,7),(-0.5,7.5),(0.5,7.5),(2,7),(3.5,6),(10,10),(6,16.5),(8,17),(10,17),(12,16.5),(13,16),(14,15.5),(15.5,14),(16,13.5),(17,12),(17.7,10),(18,8),(17.5,6),(16,4),(12,8),(3.5,1.5),(3.5,-1.5),(12,-8),(16,-4),(17.5,-6),(18,-8),(17.7,-10),(17,-12),(16,-13.5),(15.5,-14),(14,-15.5),(13,-16),(12,-16.5),(10,-17),(8,-17),(6,-16.5),(10,-10),(3.5,-6.5),(-3.5,-6.5),(-3.5,-6),(-10,-10),(-6,-16.5),(-8,-17),(-10,-17),(-12,-16.5),(-13,-16),(-14,-15.5),(-15.5,-14),(-16,-13.5),(-17,-12),(-17.7,-10),(-18,-8),(-17.5,-6),(-16,-4),(-12,-8),(-12,-8),(-3.5,-1.5),(-3.5,1.5),(-12,8))
register_shape("drone",shapePoints)

def colorisize(turtle, height, direction):
	red, green, blue = turtle.color()[0]
	redOffset, greenOffset, blueOffset = height*.9, height*.1, height*.1
	if direction=="up": red,green,blue = int(red+redOffset), int(green+greenOffset), int(blue+blueOffset)
	elif direction=="down": red,green,blue = int(red-redOffset), int(green-greenOffset), int(blue-blueOffset)
	if red > 255: red = 255
	elif red < 0: red = 0
	if green > 255: green = 255
	elif green < 0: green = 0
	if blue > 255: blue = 255
	elif blue < 0: blue = 0
	return red, green, blue

def breakadids(string): 
	raise Exception("\u001b[38;5;202m\u001b[48;5;226m\u001b[1m\n"+string+"\u001b[0m")
def hit(item): breakadids("Drone has collided with\nthe "+item)
def checkCollision(daMethod,oldPosition,daHeight):
	if daMethod != "curve":
		newPosition = int(droneTurtle.position()[0]),int(droneTurtle.position()[1]),int(daHeight)
		droneA, droneB = {"x":int(oldPosition[0]),"y":int(oldPosition[1]),"z":int(oldPosition[2])}, {"x":newPosition[0],"y":newPosition[1],"z":newPosition[2]}
		droneXs, droneYs, droneZs = [*range(droneA["x"],droneB["x"])], [*range(droneA["y"],droneB["y"])], [*range(droneA["z"],droneB["z"])]
		for daList,type in ((droneXs,"x"),(droneYs,"y"),(droneZs,"z")):
			if not daList: daList += [*range(droneB[type],droneA[type])]
			if not daList: daList.append(droneA[type])
		for obstacleLine in lineList:
			lineA, lineB = obstacleLine["a"], obstacleLine["b"]	
			lineXs, lineYs, lineZs = [*range(lineA["x"],lineB["x"])], [*range(lineA["y"],lineB["y"])], [*range(lineA["z"],lineB["z"])]
			for daList,type in ((lineXs,"x"),(lineYs,"y"),(lineZs,"z")):
				if not daList: daList += [*range(lineB[type],lineA[type])]
				if not daList: daList.append(lineA[type])
			hitX,hitY,hitZ = False,False,False
			for droneValues,lineValues,type in ((droneXs,lineXs,"x"),(droneYs,lineYs,"y"),(droneZs,lineZs,"z")):
				for dv in droneValues:
					if type=="z": collisionRange = range(-1,2)
					else: collisionRange = range(-6,7)
					for value in collisionRange:
						if dv+value in lineValues:
							if type=="x": hitX = True
							elif type=="y": hitY = True
							elif type=="z": hitZ = True
					if hitX==True and hitY==True and hitZ==True: hit(obstacleLine["name"])
	elif daMethod == "curve":
		print("Oop")

class Tello:
	"""Tello object uses a turtle drawing to represent a drone.\n
	No parameters are required.\n
	Optional "scalefactor" parameter allows for representations to be smaller or larger (input percent value as integer, default=100). \n
  Optional "meter" parameter allows for the user to preserve or remove the meter option for the height (input as bool, default=True). \n
	Optional "map" parameter allows for the turtle to have a map set. The current option is "obstacle" or "course" for the Kunz Lab Obstacle course, and if "left" or "right" is included, the side of the course can be chosen. ex: "courseleft" or "obstacleRight." \n
 	Optional "penEnabled" paremeter determines if the drone path should be drawn or not. Bool True enables, Bool False disables."""
	def __init__(self,scalefactor:int=100,meter:bool=True,map:str="",penEnabled:bool=True):
		self.scalefactor = scalefactor/100
		if scalefactor <= 0: breakadids("Scalefactor cannot be 0 or less")
		
		global droneTurtle
		droneTurtle = Turtle()
		colormode(255)
		
		droneTurtle.shape("drone")
		droneTurtle.setheading(90)
		droneTurtle.speed(1)
		droneTurtle.color(255,255,255)
		droneTurtle.resizemode("user")
		droneTurtle.shapesize(self.scalefactor/2,self.scalefactor/2,self.scalefactor/2)
		
		self.meterSet = meter
		if meter:
			global meterTurtle
			meterTurtle = Turtle()
			meterTurtle.speed(0)
			meterTurtle.hideturtle()
			meterTurtle.penup()
			width, height = window_width(), window_height()
			self.meterHeight = height/3
			self.meterBottom = {"x":width/-2+30,"y":height/-2+30}
			meterTurtle.goto(self.meterBottom["x"],self.meterBottom["y"])
			meterTurtle.pensize(2)
			meterTurtle.pendown()
			meterTurtle.forward(25)
			meterTurtle.backward(50)
			meterTurtle.forward(25)
			meterTurtle.left(90)
			meterTurtle.penup()
			meterTurtle.forward(self.meterHeight)
			meterTurtle.left(90)
			meterTurtle.pendown()
			meterTurtle.forward(25)
			meterTurtle.backward(50)
			meterTurtle.forward(25)
			meterTurtle.penup()
			meterTurtle.right(90)
			meterTurtle.backward(self.meterHeight)
			meterTurtle.pensize(15)
			meterTurtle.color(255,255,255)
		
		self.inAir = False
		self.height = 0
		self.speed = 100
			
		timeNow = localtime()
		self.startTime = {
			"H":int(strftime("%H", timeNow)),
			"M":int(strftime("%M",timeNow)),
			"S":int(strftime("%S",timeNow))
		}
		self.totalDistance = 0
		if map == "": self.mapEnabled = False
		else: self.mapEnabled = True
		if "obstacle" in map.lower() or "course" in map.lower():
			mapTurtle = Turtle()
			mapTurtle.speed(0)
			mapTurtle.hideturtle()
			mapTurtle.penup()
			mapTurtle.goto(300*self.scalefactor,0) # Right Fence
			mapTurtle.pendown()
			mapTurtle.goto(380*self.scalefactor,0)
			mapTurtle.penup()
			mapTurtle.goto(320*self.scalefactor,-200*self.scalefactor) # Right Carpet
			mapTurtle.pendown()
			mapTurtle.goto(360*self.scalefactor,-200*self.scalefactor)
			mapTurtle.goto(360*self.scalefactor,-240*self.scalefactor)
			mapTurtle.goto(320*self.scalefactor,-240*self.scalefactor)
			mapTurtle.goto(320*self.scalefactor,-200*self.scalefactor)
			mapTurtle.penup()
			mapTurtle.goto(-320*self.scalefactor,-200*self.scalefactor) # Left Carpet
			mapTurtle.pendown()
			mapTurtle.goto(-360*self.scalefactor,-200*self.scalefactor)
			mapTurtle.goto(-360*self.scalefactor,-240*self.scalefactor)
			mapTurtle.goto(-320*self.scalefactor,-240*self.scalefactor)
			mapTurtle.goto(-320*self.scalefactor,-200*self.scalefactor)
			mapTurtle.penup()
			mapTurtle.goto(-300*self.scalefactor,0) # Left Fence
			mapTurtle.pendown()
			mapTurtle.goto(-380*self.scalefactor,0)
			mapTurtle.penup()
			mapTurtle.goto(-30*self.scalefactor,450*self.scalefactor) # Top Fence
			mapTurtle.pendown()
			mapTurtle.goto(30*self.scalefactor,450*self.scalefactor)
			droneTurtle.penup()
			if "right" in map.lower(): droneTurtle.goto(340*self.scalefactor,-220*self.scalefactor)
			else: droneTurtle.goto(-340*self.scalefactor,-220*self.scalefactor)
			droneTurtle.pendown()
			global lineList
			lineList = [
				{"name":"Lower Bar (Left Fence)",
				 "a":{"x":int(-380*self.scalefactor),"y":0,"z":int(95*self.scalefactor)},
				 "b":{"x":int(-300*self.scalefactor),"y":0,"z":int(95*self.scalefactor)}},
				{"name":"Upper Bar (Left Fence)",
				 "a":{"x":int(-380*self.scalefactor),"y":0,"z":int(190*self.scalefactor)},
				 "b":{"x":int(-300*self.scalefactor),"y":0,"z":int(190*self.scalefactor)}},
				{"name":"Left Leg (Left Fence)",
				 "a":{"x":int(-380*self.scalefactor),"y":0,"z":0},
				 "b":{"x":int(-380),"y":0,"z":int(190*self.scalefactor)}},
				{"name":"Right Leg (Left Fence)",
				 "a":{"x":int(-300*self.scalefactor),"y":0,"z":0},
				 "b":{"x":int(-300*self.scalefactor),"y":0,"z":int(190*self.scalefactor)}},
				{"name":"Top Bar (Top Fence)",
				 "a":{"x":int(-30*self.scalefactor),"y":int(450*self.scalefactor),"z":int(80*self.scalefactor)},
				 "b":{"x":int(30*self.scalefactor),"y":int(450*self.scalefactor),"z":int(80*self.scalefactor)}},
				{"name":"Left Leg (Top Fence)",
				 "a":{"x":int(-30*self.scalefactor),"y":int(450*self.scalefactor),"z":0},
				 "b":{"x":int(-30*self.scalefactor),"y":int(450*self.scalefactor),"z":int(80*self.scalefactor)}},
				{"name":"Right Leg (Top Fence)",
				 "a":{"x":int(30*self.scalefactor),"y":int(450*self.scalefactor),"z":0},
				 "b":{"x":int(30*self.scalefactor),"y":int(450*self.scalefactor),"z":int(80*self.scalefactor)}},
				{"name":"Lower Bar (Right Fence)",
				 "a":{"x":int(300*self.scalefactor),"y":0,"z":int(90*self.scalefactor)},
				 "b":{"x":int(380*self.scalefactor),"y":0,"z":int(90*self.scalefactor)}},
				{"name":"Upper Bar (Right Fence)",
				 "a":{"x":int(300*self.scalefactor),"y":0,"z":int(154*self.scalefactor)},
				 "b":{"x":int(380*self.scalefactor),"y":0,"z":int(154*self.scalefactor)}},
				{"name":"Left Leg (Right Fence)",
				 "a":{"x":int(300*self.scalefactor),"y":0,"z":0},
				 "b":{"x":int(300*self.scalefactor),"y":0,"z":int(154*self.scalefactor)}},
				{"name":"Right Leg (Right Fence)",
				 "a":{"x":int(380*self.scalefactor),"y":0,"z":0},
				 "b":{"x":int(380*self.scalefactor),"y":0,"z":int(154*self.scalefactor)}}
			]
		
		if penEnabled == False: droneTurtle.penup()

	def send_command(self, command:str, query: bool=False):
		print("Pointless command '"+command+"' has been pretend sent")

	def _receive_thread(self):
		print("You have unfortunately called a pointless method")

	def _video_thread(self):
		print("Please visit 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' for your video feed")
	
	def wait(self, delay: float):
		"""Makes drone wait for specificed time \n
		"delay" parameter must be a float, counted in seconds"""
		print("wait",delay,"seconds")
		sleep(delay)

	def get_log(self):
		return "stuff has happened"

	# Controll Commands
	def command(self):
		print("Unnecessary command function has been called")
	
	def takeoff(self):
		"""Every drone must takeoff before flying"""
		if not self.inAir:
			self.inAir = True
			self.height = 50
			droneTurtle.color(50,29,15)
			print("Takeoff successful")
			if self.meterSet:
				meterTurtle.color(50,29,15)
				meterTurtle.pendown()
				meterTurtle.forward(self.meterHeight/10)
			sleep(1)
		else: breakadids("The Tello object is in the air, cannot takeoff")

	def land(self):
		"""Every drone needs to land after flying"""
		if self.inAir:
			self.inAir = False
			self.height = 0
			droneTurtle.color(0,0,0)
			if self.meterSet:
				meterTurtle.color(255,255,255)
				meterTurtle.goto(self.meterBottom["x"],self.meterBottom["y"])
			print("Landed successfully")
			sleep(1)
		else: breakadids("The Tello object is on the ground, cannot land")

	def streamon(self):
		print("Please visit 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' for your video feed")

	def streamoff(self):
		print("Hopefully you visited that link")
	
	def emergency(self):
		"""Stop motors immediately"""
		self.inAir = False
		self.height = 0
		print("Motors stopped")
		if self.meterSet:
			meterTurtle.color(255,255,255)
			meterTurtle.goto(self.meterBottom["x"],self.meterBottom["y"])
		
 # Movement Commands
	def up(self, distance: int):
		"""Ascend to specified centimeters. \n
		"distance" parameter can be 20-500, must be an integer"""
		if distance < 20 or distance > 500: breakadids("Distance is out of range")
		elif not self.inAir: breakadids("Motor Stop: drone has not taken off")
		elif self.height > 500: breakadids("Cannot exceed height of 500 cm")
		
		print("up",distance,"cm")
		oldPosition = droneTurtle.position()[0],droneTurtle.position()[1],self.height*self.scalefactor
		self.totalDistance += distance
		self.height += distance
		distance = distance*self.scalefactor
		
		red, green, blue = colorisize(droneTurtle,self.height,"up")
		droneTurtle.color(red, green, blue)
		if self.meterSet:
			meterTurtle.color(red, green, blue)
			meterTurtle.forward(distance)
		if self.mapEnabled: checkCollision("up",oldPosition,self.height*self.scalefactor)
		sleep(1)
		
	def down(self, distance: int):
		"""Descend specificed centimeters. \n
		"distance" parameter can be 20-500, must be an integer"""
		if distance < 20 or distance > 500: breakadids("Distance is out of range")
		elif not self.inAir: breakadids("Motor Stop: drone has not taken off")
		elif self.height < 20: breakadids("Cannot go below height of 20 cm")
		
		print("down",distance,"cm")	
		oldPosition = droneTurtle.position()[0],droneTurtle.position()[1],self.height*self.scalefactor
		self.totalDistance += distance
		self.height -= distance
		distance = distance*self.scalefactor
		
		red, green, blue = colorisize(droneTurtle,self.height,"down")
		droneTurtle.color(red, green, blue)
		if self.meterSet:
			meterTurtle.color(255,255,255)
			meterTurtle.backward(distance)
			meterTurtle.color(red, green, blue)
		if self.mapEnabled: checkCollision("down",oldPosition,self.height*self.scalefactor)
		sleep(1) 
		
	def left(self, distance: int):
		"""Fly left specificed distance in centimeters. \n
		"distance" parameter can be 20-500, must be an integer"""
		if distance < 20 or distance > 500: breakadids("Distance is out of range")
		elif not self.inAir: breakadids("Motor Stop: drone has not taken off")
			
		print("left",distance,"cm")
		oldPosition = droneTurtle.position()[0],droneTurtle.position()[1],self.height*self.scalefactor
		distance = distance*self.scalefactor
		self.totalDistance += distance
		
		currentX, currentY = droneTurtle.position()
		currentAngle = droneTurtle.heading()
		theta = degToRad(90+currentAngle)
		adjustX, adjustY = distance*cos(theta), distance*sin(theta)
		newX, newY = currentX+adjustX, currentY+adjustY
		droneTurtle.goto(newX,newY)
		if self.mapEnabled: checkCollision("left",oldPosition,self.height*self.scalefactor)
		sleep(1)

	def right(self, distance:int):
		"""Fly right specificed distance in centimeters. \n
		"distance" parameter can be 20-500, must be an integer"""
		if distance < 20 or distance > 500: breakadids("Distance is out of range")
		elif not self.inAir: breakadids("Motor Stop: drone has not taken off")
			
		print("right",distance,"cm")
		oldPosition = droneTurtle.position()[0],droneTurtle.position()[1],self.height*self.scalefactor
		distance = distance*self.scalefactor
		self.totalDistance += distance
		
		currentX, currentY = droneTurtle.position()
		currentAngle = droneTurtle.heading()
		theta = degToRad(90+currentAngle)
		adjustX, adjustY = distance*cos(theta)*-1, distance*sin(theta)*-1
		newX, newY = currentX+adjustX, currentY+adjustY
		droneTurtle.goto(newX,newY)
		if self.mapEnabled: checkCollision("right",oldPosition,self.height*self.scalefactor)
		sleep(1)
	
	def forward(self,distance:int):
		"""Fly forward specificed distance in centimeters. \n
		"distance" parameter can be 20-500, must be an integer"""
		if distance < 20 or distance > 500: breakadids("Distance is out of range")
		elif not self.inAir: breakadids("Motor Stop: drone has not taken off")
				
		print("forward",distance,"cm")
		oldPosition = droneTurtle.position()[0],droneTurtle.position()[1],self.height*self.scalefactor
		distance = distance*self.scalefactor
		self.totalDistance += distance
		droneTurtle.forward(distance)
		if self.mapEnabled: checkCollision("forward",oldPosition,self.height*self.scalefactor)
		sleep(1)
		
	def back(self,distance:int):
		"""Fly backward specificed distance in centimeters. \n
		"distance" parameter can be 20-500, must be an integer"""
		if distance < 20 or distance > 500: breakadids("Distance is out of range")
		elif not self.inAir: breakadids("Motor Stop: drone has not taken off")

		print("back",distance,"cm")
		oldPosition = droneTurtle.position()[0],droneTurtle.position()[1],self.height*self.scalefactor
		distance = distance*self.scalefactor
		self.totalDistance += distance
		droneTurtle.backward(distance)
		if self.mapEnabled: checkCollision("back",oldPosition,self.height*self.scalefactor)
		sleep(1)

	def cw(self, degrees:int):
		"""Rotate specified degrees clockwise. \n
		"degrees" parameter can be 1-360, must be integer"""
		if degrees < 1 or degrees > 360: breakadids("Degrees is out of range")
		elif not self.inAir: breakadids("Motor Stop: drone has not taken off")

		print("cw",degrees,"degrees")
		droneTurtle.right(degrees)
		sleep(1)

	def ccw(self, degrees:int):
		"""Rotate specified degrees counter-clockwise. \n
		"degrees" parameter can be 1-360, must be integer"""
		if degrees < 1 or degrees > 360: breakadids("Degrees is out of range")
		elif not self.inAir: breakadids("Motor Stop: drone has not taken off")

		print("ccw",degrees,"degrees")
		droneTurtle.left(degrees)
		sleep(1)

	def flip(self,direction:str):
		"""Flip in specified direction: \n
		“l” = left \n
		“r” = right \n 
		“f” = forward \n
		“b” = back"""
		if not self.inAir: breakadids("Motor Stop: drone has not taken off")
		elif direction not in ["l","r","f","b"]: breakadids("Inputed",direction," is an invalid flip option")
		
		print("flip",direction)
		oldPosition = droneTurtle.position()[0],droneTurtle.position()[1],self.height*self.scalefactor
		distance = 20*self.scalefactor
		self.totalDistance += distance
		
		if direction == "l": 
			currentX, currentY = droneTurtle.position()
			currentAngle = droneTurtle.heading()
			theta = degToRad(90+currentAngle)
			adjustX, adjustY = distance*cos(theta), distance*sin(theta)
			newX, newY = currentX+adjustX, currentY+adjustY
			droneTurtle.goto(newX,newY)
		elif direction == "r": 
			currentX, currentY = droneTurtle.position()
			currentAngle = droneTurtle.heading()
			theta = degToRad(90+currentAngle)
			adjustX, adjustY = distance*cos(theta)*-1, distance*sin(theta)*-1
			newX, newY = currentX+adjustX, currentY+adjustY
			droneTurtle.goto(newX,newY)
		elif direction == "f": droneTurtle.forward(distance)
		elif direction == "b": droneTurtle.backward(distance)
		if self.mapEnabled: checkCollision("flip",oldPosition,self.height*self.scalefactor)	
		sleep(1)

	def go(self,x:int,y:int,z:int,speed:int):
		"""Fly to coordinates at specified speed (cm/s): \n
		“x” can be -500-500, must be integer \n
		“y” can be -500-500, must be integer \n
		“z” can be -500-500, must be integer \n
		“speed” can be 10-100, must be integer \n
		Note: “x”, “y”, and “z” values can’t be set between
		-20 – 20 simultaneously."""
		if (x>-20 and x<20) and (y>-20 and y<20) and (z>-20 and z<20):
			breakadids("x, y, and z parameters can’t be set between -20 to 20 simultaneously")
		elif not self.inAir: breakadids("Motor Stop: drone has not taken off")
		elif self.height+z > 500 or self.height+z < 20: 
			breakadids("Cannot go below height of 20 cm or above height of 500cm")

		print("go",x,y,z,speed)
		oldPosition = droneTurtle.position()[0],droneTurtle.position()[1],self.height*self.scalefactor
		x, y, z = x*self.scalefactor, y*self.scalefactor, z*self.scalefactor
		x,y = y*-1, x
		
		currentX, currentY = droneTurtle.position()
		changeX, changeY = abs(currentX-x), abs(currentY-y)
		distance = sqrt(changeX**2 + changeY**2)
		self.totalDistance += distance
		
		droneTurtle.goto(x+currentX,y+currentY)

		if z != 0:
			self.height += z
			if z > 0: direction = "up"
			elif z < 0: direction = "down"
			red, green, blue = colorisize(droneTurtle,self.height,direction)
			droneTurtle.color(red, green, blue)
			if self.meterSet:
				if z > 0: 
					meterTurtle.color(red, green, blue)
					meterTurtle.forward(z)
				elif z < 0:
					meterTurtle.color(255,255,255)
					meterTurtle.backward(abs(z))
		if self.mapEnabled: checkCollision("go",oldPosition,self.height*self.scalefactor)
		sleep(1)

	def curve(self,x1:int,y1:int,z1:int,x2:int,y2:int,z2:int,speed:int):
		"""Fly at a curve according to the two given coordinates at “speed” (cm/s). \n
		If the arc radius is not within a range of 0.5-10 meters, it will respond with an error. \n
		“x1”, “x2” can be -500-500, must be integers \n
		“y1”, “y2” can be -500-500, must be integers \n
		“z1”, “z2” can be -500-500, must be integers \n
		“speed” can be 10-60, must be an integer \n
		Note: “x”, “y”, and “z” values can’t be set between
		-20 to 20 simultaneously"""
		if (x1>-20 and x1<20) and (y1>-20 and y1<20) and (z1>-20 and z1<20):
			breakadids("x, y, and z parameters can’t be set between -20 to 20 simultaneously")
		elif (x2>-20 and x2<20) and (y2>-20 and y2<20) and (z2>-20 and z2<20):
			breakadids("x, y, and z parameters can’t be set between -20 to 20 simultaneously")
		elif not self.inAir: breakadids("Motor Stop: drone has not taken off")
		elif self.height+z1>500 or self.height+z1<20 or self.height+z1+z2>500 or self.height+z1+z2<20:
			breakadids("Cannot go below height of 20 cm or above height of 500cm")
		
		print("curve",x1,y1,z1,x2,y2,z2,speed)
		oldPosition = droneTurtle.position()[0],droneTurtle.position()[1],self.height*self.scalefactor
		x1, y1, z1 = x1*self.scalefactor, y1*self.scalefactor, z1*self.scalefactor
		x2, y2, z2 = x2*self.scalefactor, y2*self.scalefactor, z2*self.scalefactor
		
		droneX, droneY = droneTurtle.position()
		x1,y1, x2,y2 = y1*-1,x1, y2*-1, x2
		pointA = { "x":droneX, "y":droneY }
		pointB = { "x":x1+droneX, "y":y1+droneY }
		pointC = { "x":x2+droneX, "y":y2+droneY }
		
		midAB, midBC = {}, {}
		for var, p1, p2 in [[midAB,pointA,pointB], [midBC,pointB,pointC]]:
			if p1["x"] > p2["x"]: var["x"] = p1["x"]-(p1["x"]-p2["x"])/2
			else: var["x"] = p2["x"]-(p2["x"]-p1["x"])/2
				
			if p1["y"] > p2["y"]: var["y"] = p1["y"]-(p1["y"]-p2["y"])/2
			else: var["y"] = p2["y"]-(p2["y"]-p1["y"])/2

			if p2["y"]-p1["y"] != 0: 
				var["m"] = (p2["x"]-p1["x"]) / (p2["y"]-p1["y"]) *-1
			else: var["m"] = 0
				
			var["b"] = var["y"]-var["m"]*var["x"]
					
		try:
			circleCenter = { "x": (midBC["b"]-midAB["b"])/(midAB["m"]-midBC["m"]) }
			circleCenter["y"] = midAB["m"]*circleCenter["x"]+midAB["b"]

			for point in [pointA,pointB,pointC]:
				changeX = point["x"]-circleCenter["x"]
				changeY = point["y"]-circleCenter["y"]
				try: 
					angle = abs(radToDeg(atan(changeY/changeX)))
					if changeX>0 and changeY>0: point["angle"] = angle
					elif changeX<0 and changeY>0: point["angle"] = 180-angle
					elif changeX<0 and changeY<0: point["angle"] = 180+angle
					elif changeX>0 and changeY<0: point["angle"] = 360-angle
					elif changeY==0: 
						if changeX>0: point["angle"] = 0
						else:					point["angle"] = 180
				except ZeroDivisionError:
					if changeY>0: point["angle"] = 90
					else:					point["angle"] = 270
	
			if pointA["angle"] > pointC["angle"]:
				option1 = [x for x in reversed(range(int(pointC["angle"]),int(pointA["angle"])+1))]
				option2 = [x for x in range(int(pointA["angle"]),360)] + [x for x in range(0,int(pointC["angle"])+1)]
			else:
				option1 = [x for x in range(int(pointA["angle"]),int(pointC["angle"])+1)]
				option2 = [x for x in reversed(range(0,int(pointA["angle"])+1))] + [x for x in reversed(range(int(pointC["angle"]),360))]
				
			if int(pointB["angle"]) in option1: daRange = option1
			else: daRange = option2
	
			radius = sqrt( (circleCenter["x"]-pointA["x"])**2 + (circleCenter["y"]-pointA["y"])**2 )
			if radius/self.scalefactor + z1+z2 <50: breakadids("Radius is too small! Points are too close together.")
			elif radius/self.scalefactor + z1+z2 >1000: breakadids("Radius is too large! Points are too far away.")
					
			positions = []
			for angle in daRange:
				angle = degToRad(angle)
				changeX, changeY = radius*cos(angle), radius*sin(angle)
				newX, newY = changeX+circleCenter["x"], changeY+circleCenter["y"]
				positions.append((newX,newY))
	
			for goX, goY in positions: droneTurtle.goto(goX,goY)

		except ZeroDivisionError:
			droneTurtle.goto(pointB["x"],pointB["y"])
			droneTurtle.goto(pointC["x"],pointC["y"])
				
		if z1 != 0:
			self.height += z1
			if z1 > 0: direction = "up"
			elif z1 < 0: direction = "down"
			red, green, blue = colorisize(droneTurtle,self.height,direction)
			droneTurtle.color(red, green, blue)
			if self.meterSet:
				if z1 > 0: 
					meterTurtle.color(red, green, blue)
					meterTurtle.forward(z1)
				elif z1 < 0:
					meterTurtle.color(255,255,255)
					meterTurtle.backward(abs(z1))
					
		if z2 != 0:
			self.height += z2
			if z2 > 0: direction = "up"
			elif z2 < 0: direction = "down"
			red, green, blue = colorisize(droneTurtle,self.height,direction)
			droneTurtle.color(red, green, blue)
			if self.meterSet:
				if z2 > 0: 
					meterTurtle.color(red, green, blue)
					meterTurtle.forward(z2)
				elif z2 < 0:
					meterTurtle.color(255,255,255)
					meterTurtle.backward(abs(z2))
		if self.mapEnabled: checkCollision("curve",oldPosition,self.height*self.scalefactor)
		sleep(1)

	# Set Commands
	def set_speed(self, speed:int):
		"""Set speed to specified cm/s \n
		"speed" parameter can be 10-100, must be integer"""
		if speed < 10 or speed > 100: breakadids("Speed is out of range")
		self.speed = speed
		print("speed is now at",speed,"cm/s")

	def rc_control(self, a:int, b:int, c:int, d:int):
		"""Set remote controller control via four channels. \n
			“a” = left/right (-100-100) \n
			“b” = forward/backward (-100-100) \n
			“c” = up/down (-100-100) \n
			“d” = yaw (-100-100)"""
		for parameter in [a,b,c,d]:
			if parameter < -100 or parameter > 100: breakadids("parameter is invalid")
		print("rc_control function has been called")

	def set_wifi(self, ssid:str, passwrd:str):
		"""Set Wi-Fi password. \n
		ssid = updated Wi-Fi name \n
		pass = updated Wi-Fi password"""
		print("wifi",ssid,"has been set up with",passwrd,"password")
		
	# Read Commands
	def get_speed(self):
		"""Obtain current speed (cm/s)"""
		return self.speed

	def get_battery(self):
		"""Obtain current battery percentage"""
		return 101

	def get_time(self):
		"""Obtain current flight time"""
		timeNow = localtime()
		currentTime = {
			"H":int(strftime("%H", timeNow)),
			"M":int(strftime("%M",timeNow)),
			"S":int(strftime("%S",timeNow))
		}
		timeChange = {
			"H":str(abs(currentTime["H"]-self.startTime["H"])),
			"M":str(abs(currentTime["M"]-self.startTime["M"])),
			"S":str(abs(currentTime["S"]-self.startTime["S"]))
		}
		return timeChange["H"]+":"+timeChange["M"]+":"+timeChange["S"]

	def get_height(self):
		"""Obtain current height"""
		return self.height/20

	def get_temp(self):
		"""Obtain current temperature"""
		return 75

	def get_attitude(self):
		"""Obtain current pitch, yaw, and roll. \n
		Response will be a dictionary with each element"""
		return {
			"pitch": 0,
			"yaw": droneTurtle.getheader(),
			"roll": 0
		}

	def get_bar(self):
		"""the barometer measurement in cm"""
		return 1

	def get_acceleration(self):
		"""Obtain acceleration value"""
		return 100

	def get_tof(self):
		"""Obtain total flight distance"""
		return self.totalDistance

	def get_wifi(self):
		return "Connected to turtle-drone"