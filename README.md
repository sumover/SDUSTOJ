# Welcome to use SDUSTOJ

这是一份使用说明.

代码结构说明:

目前, 所有的业务逻辑代码均放在SDUSTOJ主目录下.

所有的Django模板HTML代码均放在template/的相关文件夹下.

相关的静态文件放在static/的相关文件夹下.

# APP 应用结构说明

目前项目规划分为三个python包以及主项目包.

### APP应用层

1.  OnlineJudge

    主要的前端业务逻辑的代码, 多数与页面内异步请求无关的代码均置于此.

2.  AJAXapi

    用于处理页面内异步AJAX请求的业务逻辑代码.

3.  DOMServer

    用于与DOMServer进行直接的数据库通信的python接口.

### 前端业务层

主目录:templates/ & static/

相应的页面代码应放置在相应的子文件夹下, 如template/OnlineJudge/, static/OnlineJudge/




