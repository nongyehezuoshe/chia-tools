#! /usr/bin/env python3
import os,sys,time,json,shutil

options={}

def tool_print(line,text):
	print("\033[7m"+time.strftime("%H:%M:%S ", time.localtime())+str(line)+": "+"\033[0m",text)

def plots_diskcheck():
	disk_free=shutil.disk_usage(options["disk_path"]["value"])[2]/1024**3
	tool_print(str(sys._getframe().f_lineno)+" "+"Free size",disk_free)
	if disk_free<options["disk_size"]["value"]:
		plots_remove()

def plots_remove():
	file_list=os.listdir(options["file_location"]["value"])
	# print(file_list)
	new_filelist= sorted(file_list,  key=lambda x: os.path.getctime(os.path.join(options["file_location"]["value"], x)),reverse = False)
	# print(new_filelist)
	for _file in new_filelist:
		if _file.endswith(options["file_endswith"]["value"]):
			_file_time=time.strftime("%Y%m%d",time.localtime(os.path.getctime(options["file_location"]["value"]+"/"+_file)))
			if _file_time>= options["file_time"]["value"].split("-")[0] and _file_time<= options["file_time"]["value"].split("-")[1]:
				os.remove(options["file_location"]["value"]+"/"+_file)
				tool_print(str(sys._getframe().f_lineno)+" "+"removed",_file)
				return
	tool_print(str(sys._getframe().f_lineno)+" "+"no file can be removed","...")

if __name__ == "__main__":
	while True:
		options=json.loads(open("options.json","rb").read())
		plots_diskcheck()
		time.sleep(options["time_interval"]["value"])