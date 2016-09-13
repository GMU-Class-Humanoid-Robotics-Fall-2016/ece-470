import time

def main():
	while(True):
		t0 = time.clock()
		t1 = time.clock()
		dt = t1 - t0
		check = .20 - dt
		while(0 < (.20 - dt)):
			dt = time.clock() - t0
		print dt

main()