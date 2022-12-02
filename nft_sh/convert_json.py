#! /usr/bin/env python3
import os,json,csv

metadata={
	"encoded_id": "nft1vg6ergrsdk2ghnvff2ncgj6xzdg3hyyennmyzvecjs97qlzthqcq7vnamp",
	"name": "open box#0015"
}

def set_json():
	file_name="lastid.csv"
	new_json=[]
	file_input=open(file_name,"r").readlines()
	for _input in file_input:
		_OBJ=metadata.copy()
		_OBJ["encoded_id"]=_input.split("\n")[0].split(",")[1].strip()

		_num=int(_input.split("\n")[0].split(",")[0].strip())
		_num_str=""
		if _num<10:
			_num_str="000"+str(_num)
		elif _num<100:
			_num_str="00"+str(_num)
		elif _num<1000:
			_num_str="0"+str(_num)
		_OBJ["name"]="open box#"+_num_str
		new_json.append(_OBJ)

	with open(file_name+".json", "w") as file_output: 
		json.dump(new_json, file_output, indent=4, separators=(',', ': '))

if __name__ == "__main__":
	set_json()