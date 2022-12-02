#! /usr/bin/env python3

import hashlib,os,csv,sys,subprocess,time

options={
	"f":"87247851", # fingerprint / 指纹
	"m":"0.0000001" # A fee to add to the offer when it gets taken / 手续费
}
maindata={
	"allnfts":[]
}

def tool_print(line,text):
	print("\033[7;31;47m Line:"+str(line)+" \033[0m",text)

def set_offer():
	_last=open("lastid.csv","r").readlines()
	_current=open("hash.csv","r").readlines()
	_f=options["f"]
	_m=options["m"]
	for i in _last:
		for ii in _current:
			# print(i[0].strip())
			if i.split(",")[0].strip()==ii.split(",")[0].strip()[:-4]:
				tool_print(str(sys._getframe().f_lineno)+" "+"catched",i.split(",")[1].strip()+"||"+ii.split(",")[1].strip())
				while True:
					_offer=subprocess.run(['chia', 'wallet', 'make_offer', '-f', _f, '-m', _m, '-p', 'offers/'+i.split(",")[1].strip()+"-"+ii.split(",")[1].strip(), '-o', ii.split(",")[1].strip()+":1", '-r',i.split(",")[1].strip()+":1"],capture_output=True,text=True,input="y\ny")
						print(_offer.stdout)
					if _offer.returncode==0 :
						print(_offer.stdout)
						break
				break

if __name__ == "__main__":
	set_offer()