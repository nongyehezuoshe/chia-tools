#! /usr/bin/env python3

import csv

f = open('bshholder.csv', 'r')
conf={
	"reader":"",
	"writer":""
}

_num=1000
_flag=0
_cut=0
with f:
	conf["reader"] = csv.reader(f)
	for row in conf["reader"]:
		print(row)
		if _flag%_num==0:
			conf["writer"]=csv.writer(open('bsh_cut/bshholder_cut_'+str(_cut)+'.csv', 'a'))
			conf["writer"].writerow(['addr','name','mount'])
			_cut=_cut+1
		conf["writer"].writerow(row)
		_flag=_flag+1