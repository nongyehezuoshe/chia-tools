#! /usr/bin/env python3
import os,json

metadata ={
	"format": "CHIP-0007",
	"name": "nft_name", # nft name
	"description": "nft description.", # nft description
	"sensitive_content": False,
	"collection": {
		"name": "collection_name", # nft collection name
		"id": "c2bad6fb-5b2f-47f6-b158-524c559b6725", # nft collection id
		"attributes": [
			{
				"type": "description",
				"value": "NFT collection description" # NFT collection description
			},
			{
				"type": "icon",
				"value": "https://www.test.com/icon.png" # NFT collection icon url
			},
			{
				"type": "banner",
				"value": "https://www.test.com/banner.png" # NFT collection banner url
			},
			{
				"type": "website",
				"value": "https://www.test.com" # website url
			},
			{
				"type": "twitter",
				"value": "@xxxx" # twitter url
			},
			{
				"type":"discord",
				"value":"https://discord.com/invite/xxxx" # discord url
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

if __name__ == "__main__":
	set_hash()