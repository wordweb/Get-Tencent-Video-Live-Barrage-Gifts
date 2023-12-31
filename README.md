# Get-Tencent-Video-Live-Barrage-Gifts

##使用说明

下载主程序和依赖组件，直接执行项目

```shell
# 拉取仓库
$ git clone https://github.com/wordweb/Get-Tencent-Video-Live-Barrage-Gifts.git

# 进入目录
$ cd Get-Tencent-Video-Live-Barrage-Gifts

# 安装依赖
$ pip install -r requirements.txt

# 运行项目
$ python webapi.py
```

接下来在控制台中将看到一个二维码，用开播的微信扫码登录。

登录成功以后将会看到以下提示：

```
请使用微信扫码登录！
已扫码请在手机上点击确认登录！
已成功登录！
直播间【测试】状态正常
加载成功，开启消息获取线程。获取实时弹幕消息。
如需关闭服务，请输入ctrl+C来终止api服务进程，再输入exit退出监听。
INFO:     Will watch for changes in these directories: ['D:\\wx']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [32268] using StatReload
INFO:     Started server process [14332]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

##获取弹幕等消息
程序将自动在运行目录中建立一个名为msglist的目录，所有捕获到的消息都会缓存在该目录中。以捕获到消息的时间戳作为文件名称。
可以直接读取这些文件来获取信息，当然你也可以通过http api接口请求的方式来主动查询。

##api接口说明
一共提供了三个接口

###获取当前在线用户列表
```
http://127.0.0.1:8000/get_online_member
```

请求方式GET

###获取一组弹幕消息
弹幕消息可能是一条也可能是多条，根据当前直播间弹幕发送速度系统自动分割
```
http://127.0.0.1:8000/getmsg
```
请求方式GET

###删除所有缓存弹幕消息
```
http://127.0.0.1:8000/clsmsg
```
请求方式GET


技术讨论群：734340800