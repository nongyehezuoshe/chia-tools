#! /usr/bin/env python3
import requests,json,time,subprocess,sys,os

options={
	"collection_name":"balldog", # farmersmarket.cc 中定义的collection name
	"collection_id":"col17jxrr7pwxuhxra86z4gr08tajk3mpr7gjst643a7gv0dc8p8p9aqdcvj30", # mintgarden.io 中定义的 collection id
	"ele_index": 2, # farmersmarket.cc 中定义的nft属性序号
	"ele_value":"Special" # nft属性值，如果需要获取所有nft的holder，则留空。
}

maindata={
	"holders":[],
	"page":"",
	"id_by_ele":[]
}

def tool_print(line,text):
	print("\033[7;31;47m"+str(line)+" \033[0m",text)

def get_holdersdata():
	tool_print(str(sys._getframe().f_lineno)+" "+"get holders data","...")
	while True:
		try:
			tool_print(str(sys._getframe().f_lineno)+" "+"request:","https://api.mintgarden.io/collections/"+options["collection_id"]+"/nfts?"+maindata["page"]+"size=100")
			r = requests.get("https://api.mintgarden.io/collections/"+options["collection_id"]+"/nfts?"+maindata["page"]+"size=100")
			if r.status_code==200:
				for i in r.json()["items"]:
					_nft={
						"id":i["encoded_id"],
						"holder":i["owner_address_encoded_id"]
					}
					tool_print(str(sys._getframe().f_lineno)+" "+"nft:",_nft)
					maindata["holders"].append(_nft)

			maindata["page"]="page="+r.json()["next"]+"&"
			if r.json()["next"]==r.json()["page"]:
				break
			time.sleep(3)
			continue
		except Exception as e:
			tool_print(sys._getframe().f_lineno,e)
	print(maindata["holders"])

def get_idbyeledata():
	tool_print(str(sys._getframe().f_lineno)+" "+"get id by ele data","...")
	url ="https://farmersmarket.cc/assets/data/"+options["collection_name"]+".txt"+"?_="+str(int(time.time()*1000))
	req=requests.get(url).text
	response = json.loads(req)
	# print(json.dumps(response, indent=4, sort_keys=True))
	for nft in response["data"]:
		if nft[4+options["ele_index"]]==options["ele_value"]:
			maindata["id_by_ele"].append(nft[2])
			# _nft={
			# 	"id":nft[2]
			# }
			# with open("output_holder","a") as f:
			# 	f.writelines(_nft["id"]+"\n")
	print(maindata["id_by_ele"])

if __name__ == "__main__":
	open("output_holder.csv", 'w').close()
	get_idbyeledata()
	get_holdersdata()
	for nftid in maindata["id_by_ele"]:
		for nft in maindata["holders"]:
			# tool_print(str(sys._getframe().f_lineno)+" "+"nftid",nftid)
			# tool_print(str(sys._getframe().f_lineno)+" "+"nft",nft)
			if options["ele_value"].strip()=="":
				with open("output_holder.csv","a") as f:
					f.writelines(nft["id"]+","+nft["holder"]+"\n")
			else:
				if nftid==nft["id"]:
					with open("output_holder.csv","a") as f:
						tool_print(str(sys._getframe().f_lineno)+" "+"catched",nft["id"]+","+nft["holder"])
						f.writelines(nft["id"]+","+nft["holder"]+"\n")
					continue