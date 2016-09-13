import time

def foo():
	time.sleep(0.20)

def main():
	while(True):
		t0 = time.clock()
		t1 = time.clock()
		dt = t1 - t0
		while(0 < (1 - dt)):
			dt = time.clock() - t0
		print dt

main()