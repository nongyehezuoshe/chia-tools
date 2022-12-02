#! /usr/bin/env python3
import os,json,csv

metadata ={
	"format": "CHIP-0007",
	"name": "Freckle Girls II", # nft name
	"description": "Furike is a freckled girl, every girl has her own unique charm, freckles are also her lovely existence.Furike is every girl, every independent and confident girl.", # nft description
	"sensitive_content": False,
	"collection": {
		"name": "Freckle Girls II", # nft collection name
		"id": "614fa088-2e8d-4964-835c-8b23ec2a112f", # nft collection id
		"attributes": [
			{
				"type": "description",
				"value": "Furike is a freckled girl, every girl has her own unique charm, freckles are also her lovely existence.Furike is every girl, every independent and confident girl." # NFT collection description
			},
			{
				"type": "icon",
				"value": "https://bafybeia7ntyq4xoiwym32sy5z3e3z7bcvdcmgtauhmuewgf4etxqvdgofe.ipfs.nftstorage.link/fg2_icon.png" # NFT collection icon url
			},
			{
				"type": "banner",
				"value": "https://bafybeia7ntyq4xoiwym32sy5z3e3z7bcvdcmgtauhmuewgf4etxqvdgofe.ipfs.nftstorage.link/fg2_banner.png" # NFT collection banner url
			},
			{
				"type": "website",
				"value": "https://twitter.com/yanzhan22714570" # website url
			},
			{
				"type": "twitter",
				"value": "@yanzhan22714570" # twitter url
			}
		]
	},
	"attributes": []
}

def set_hash():
	_ext=".png"
	_path="nft_temp"
	_files=os.listdir(_path)
	if not os.path.exists(_path+"/nft"):
		os.makedirs(_path+"/nft")
	if not os.path.exists(_path+"/meta"):
		os.makedirs(_path+"/meta")

	for _file in _files:
		_metadata=metadata.copy()
		if not os.path.isdir(_file):
			_attr=[]
			for i in _file.split("____5____")[1].split("__"):
				_flag={}
				# print(i.split("_"))
				_flag["trait_type"]=str(i.split("_")[0]).strip()
				if str(i.split("_")[1]).endswith(".png"):
					_flag["value"]=str(i.split("_")[1])[:-4].strip()
				else:
					_flag["value"]=str(i.split("_")[1]).strip()
				_attr.append(_flag)
			_name=_file.split("____5____")[0].split("#")[1]
			_metadata["attributes"]=_attr
			_metadata["name"]=_metadata["name"]+" #"+_name
			os.rename(_path+"/"+_file,_path+"/nft/"+_name+".png")
			with open(_path+"/meta/"+_name+".json", "w") as outfile: 
				json.dump(_metadata, outfile, indent=4, separators=(',', ': '))

def set_csv():
	open('attr.csv', 'w').close()
	f=open('attr.csv', 'a')
	# f=csv.writer(open('attr.csv', 'a'))
	# f.writerow(("name_nft","hash_nft","name_meta","hash_meta","mint","mint"))


	_path="nft_temp"
	_files=os.listdir(_path)

	for _file in _files:
		if not os.path.isdir(_file):
			_attr=[]
			for i in _file.split("____5____")[1].split("__"):
				# _attr.append(_file.split("____5____")[0])
				if str(i.split("_")[1]).endswith(".png"):
					# _flag["value"]=str(i.split("_")[1])[:-4].strip()
					_attr.append(str(i.split("_")[1])[:-4].strip())
				else:
					# _flag["value"]=str(i.split("_")[1]).strip()
					_attr.append(str(i.split("_")[1]).strip())
				# _attr.append(_flag)

			# _name=_file.split("____5____")[0]
			_attr.insert(0,_file.split("____5____")[0])
			print(_attr)
			# f=open("attr.csv").readlines()
			f.writelines(",".join(_attr)+"\n")

if __name__ == "__main__":
	set_hash()
	# set_csv()