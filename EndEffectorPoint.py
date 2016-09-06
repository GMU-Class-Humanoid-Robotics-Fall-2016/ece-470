import math

def endPoint(degree1, degree2, degree3):
	degree1 = degree1 * (math.pi / 180)
	degree2 = degree2 * (math.pi / 180)
	degree3 = degree3 * (math.pi / 180)
	x = 2*math.cos(degree1)+1*math.cos(degree1+degree2)+1*math.cos(degree1+degree2+degree3)
	y = 2*math.sin(degree1)+1*math.sin(degree1+degree2)+1*math.sin(degree1+degree2+degree3)
	print "x =", x
	print "y =", y

endPoint(45,315,45)
