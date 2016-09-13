import time

def foo():
	time.sleep(0.20)

def main():
	while(True):
		time.sleep(1)
		while(True):
			t0 = time.time()
			foo()
			t1 = time.time()
			dt = t1 - t0
			break
		print dt

main()
