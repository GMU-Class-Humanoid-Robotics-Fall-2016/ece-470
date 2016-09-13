import time

def foo():
	time.sleep(1)

def main():
	while(True):
		t0 = time.clock()
		print t0
		foo()
		t1 = time.clock()
		print t1
		dt = t1 - t0
		time.sleep(.20 - (dt))
		print dt
main()