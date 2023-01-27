#! /usr/bin/env python3
import os,sys,subprocess,time,json,shutil

options={}

def tool_print(line,text):
	print("\033[7m"+time.strftime("%H:%M:%S ", time.localtime())+str(line)+": "+"\033[0m",text)

def plots_check():
	tool_print(str(sys._getframe().f_lineno)+" "+"START","...")
	_path=os.path.abspath(os.path.expanduser(os.path.expandvars(options["plots_path"]["value"])))
	_dir=os.listdir(_path)
	for _plot in _dir: 
		if not os.path.isdir(_plot) and _plot.endswith("plot"):
			tool_print(str(sys._getframe().f_lineno)+" "+"checking",_plot)
			_sub=subprocess.run(['chia', 'plots', 'check', '-g', _path+'/'+_plot],capture_output=True,text=True)
			_out=_sub.stderr.split('Proofs')
			if len(_out)>1:
				_out=_sub.stderr.split("Proofs")[1].split(", ")[1].split("\n")[0].split("\x1b[0m")[0].strip()
				tool_print(str(sys._getframe().f_lineno)+" "+"checked",_out)
				if float(_out)>=float(options["ratio"]["value"]):
					_remove=plots_remove()
					if _remove=="finish":
						tool_print(str(sys._getframe().f_lineno)+" "+"finished","all plots be replaced")
						return True
					elif not _remove:
						tool_print(str(sys._getframe().f_lineno)+" "+"Error","remove target plot failed")
						return False
					try:
						tool_print(str(sys._getframe().f_lineno)+" "+"Moving","...")
						shutil.copy2(_path+"/"+_plot,options["plots_path_target"]["value"]+"/"+_plot)
						os.remove(_path+"/"+_plot)
						tool_print(str(sys._getframe().f_lineno)+" "+"Moved",_plot)
					except Exception as err:
						print(err)
				else:
					os.remove(_path+"/"+_plot)
					tool_print(str(sys._getframe().f_lineno)+" "+"deleted",_plot)
			else:
				os.remove(_path+"/"+_plot)
				tool_print(str(sys._getframe().f_lineno)+" "+"deleted",_plot)
				continue

def plots_remove():
	tool_print(str(sys._getframe().f_lineno)+" "+"removing target plot","...")
	_path=os.path.abspath(os.path.expanduser(os.path.expandvars(options["plots_path_target"]["value"])))
	_file=open(_path+"/"+"plots_check.csv")
	_str=_file.read().split("\n")
	for i in range(0,len(_str)):
		if _str[i].strip()=="":
			_str.remove(_str[i])
			open(_path+"/"+"plots_check.csv","w").write("\n".join(_str))
			continue

		if _str[i].split(",")[1]=="err" or float(_str[i].split(",")[1])<float(options["ratio_target"]["value"]):
			try:
				os.remove(_path+"/"+_str[i].split(",")[0])
				tool_print(str(sys._getframe().f_lineno)+" "+"removed target plot",_str[i].split(",")[0])
			except Exception as err:
				print(err)
			finally:
				_str.remove(_str[i])
				open(_path+"/"+"plots_check.csv","w").write("\n".join(_str))
			return True
	if i==len(_str)-1:
		return "finish"
	else:
		return False

if __name__ == "__main__":
	while True:
		options=json.loads(open("options.json").read())
		if not plots_check():
			time.sleep(10)
		else:
			break