import time

def foo():
	time.sleep(0.20)

def main():
	while(True):
		t0 = time.time()
		foo()
		t1 = time.time()
		dt = t1 - t0
		print dt
		while(0 < (1 - dt)):
			dt = time.time() - t0

main()