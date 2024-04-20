#! /usr/bin/env python3

import requests,json,time,subprocess,sys,os

options={
	"collectionid":"col1vfvrczhhpamusgqccphl5lwgqd26vyuvm668augqjr72cyht3hdsxyd7w2",
	# "page":"page="+">i:0~s:0d9220afb24e4bb824670dabaaf4de53549f8590384d22d12d30cdfda544c177"+"&"
	"page":""
}
maindata={
	"uris":[],
	"id":[],
	"owner":[]
}

def tool_print(line,text):
	print("\033[7;31;47m Line:"+str(line)+" \033[0m",text)

def get_addrfromspacescan():
	while options["page"]!="null":
		try:
			tool_print(sys._getframe().f_lineno,"https://api.mintgarden.io/collections/"+options["collectionid"]+"/nfts?"+options["page"]+"size=100")
			r = requests.get("https://api.mintgarden.io/collections/"+options["collectionid"]+"/nfts?"+options["page"]+"size=100")
			tool_print(sys._getframe().f_lineno,r.json())
			if r.status_code==200:
				for i in r.json()["items"]:
					tool_print(sys._getframe().f_lineno,i)
					with open("minted_nftid","a") as f:
						f.writelines(i["encoded_id"]+","+i["name"]+"\n")

			options["page"]="page="+r.json()["next"]+"&"

			time.sleep(3)
			continue
		except Exception as e:
			tool_print(sys._getframe().f_lineno,e)

if __name__ == "__main__":
	get_addrfromspacescan()
