#! /usr/bin/env python3

import requests,json,time,subprocess,sys,os

options={
	"collectionid":"col1lqdkghxfwj7v0ajka0ww4q5ljkzjh8xgm28h7e3s4sh03smrmxxsn8qcpw", # mintgarden定义的collection ID / collection ID by mintgarden
	"ele_type":"Background", # 属性名称 / attribute type
	"ele_value":"East",  # 属性值 / attribute value
	"page":""
}

def tool_print(line,text):
	print("\033[7;31;47m Line:"+str(line)+" \033[0m ",text)

def get_addr():
	open("nftholder", 'w').close()
	while options["page"]!="null":
		try:
			tool_print(str(sys._getframe().f_lineno)+" "+"request:","https://api.mintgarden.io/collections/"+options["collectionid"]+"/nfts?"+options["page"]+"size=100")
			r = requests.get("https://api.mintgarden.io/collections/"+options["collectionid"]+"/nfts?"+options["page"]+"size=100")
			# tool_print(sys._getframe().f_lineno,r.json())
			if r.status_code==200:
				for i in r.json()["items"]:
					tool_print(str(sys._getframe().f_lineno)+" "+"check nft:",i["encoded_id"])
					if options["ele_type"].strip()!="":
						try:
							req_by_ele=requests.get("https://api.mintgarden.io/nfts/"+i["encoded_id"])
							if req_by_ele.status_code==200:
								for ii in req_by_ele.json()["data"]["metadata_json"]["attributes"]:
									if ii["trait_type"]==options["ele_type"].strip() and ii["value"]==options["ele_value"].strip():
										_xch=req_by_ele.json()["owner_address"]["encoded_id"]
										_id=req_by_ele.json()["encoded_id"]
										tool_print(str(sys._getframe().f_lineno)+" "+"holder:",_id+" - "+_xch)
										with open("nftholder","a") as f:
											f.writelines(_id+","+_xch+"\n")
											time.sleep(1)
											continue
						except Exception as e:
							tool_print(sys._getframe().f_lineno,e)
					else:
						tool_print(str(sys._getframe().f_lineno)+" "+"holder:",i)
						with open("nftholder","a") as f:
							f.writelines(i["encoded_id"]+","+i["owner_address_encoded_id"]+"\n")

			options["page"]="page="+r.json()["next"]+"&"
			time.sleep(3)
			continue
		except Exception as e:
			tool_print(sys._getframe().f_lineno,e)

if __name__ == "__main__":
	get_addr()
