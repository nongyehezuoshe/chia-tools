## how to use
### 安装python（略）
### 安装依赖包
```bash
pip install websocket-client requests uuid
```
### 修改配置文件
修改`config/options.json`相应的选项，主要是`chia_server`,`chia_ssl`,`name`和`notif_url`  
其中，`notif_url`推荐去https://xizhi.qqoq.net 申请，简单方便快捷。
### 运行
Linux： `./notif.py`  
Windows： `python3 notif.py`