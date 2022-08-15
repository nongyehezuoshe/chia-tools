#! /usr/bin/env python3

import csv,time,subprocess

f = open('bshcat1.csv', 'r')
f_new=open('bshholder.csv', 'a')
with f:
	reader = csv.DictReader(f)
	writer=csv.DictWriter(f_new, fieldnames=['addr', 'name','mount','note'])
	_num=0
	for row in reader:
		while True:
			_sub=subprocess.run(["cdv","encode",row["hash"]],capture_output=True,text=True)
			if _sub.returncode==0:
				_out=_sub.stdout.split("\n")[0]
				writer.writerow({'addr' : _out, 'name': 'BSH', 'mount':row["mount"],'note':'',})
				_num=_num+1
				if _num%100==0:
					print(_num,_out)
				break
			time.sleep(1)