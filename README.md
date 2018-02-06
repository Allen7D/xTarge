# safe_protocol_moniter

##  前端项目
> A Vue.js project

### Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```



### 后端项目环境
1. 进入sudo，安装环境<br> `sudo apt-get install git pip`
2. 从github上下载项目<br>
`git clone https://github.com/jingwang/safe-protocol.git`
3. 全局安装python的库flask、flask_socketio<br>
`pip install -r requirements.txt`

### 项目运行
#### 版本V1.0
在终端打开`safe-protocol`目录
运行`python initUser.py` 初始化数据库　<br>
初始化后 <br>　

id=111111 name=super_admin level=A <br>
id=222222 name=admin level=B <br>
id=333333 name=gushenxing level=C <br>
id=12345 name=test level=C <br>

运行`python app.py runserver --host 0.0.0.0`<br>

1.浏览器输入　0.0.0.0:5000/login?name=admin&pw=admin <br>
即可看到**用戶登錄界面**<br>

2.浏览器输入　0.0.0.0:5000/login?name=admin&pw=admin <br>
或　浏览器输入　0.0.0.0:5000/login?name=super_admin&pw=super_admin <br>
即可登录到 **management界面**<br>
 浏览器输入　0.0.0.0:5000/login?name=gushenxing&pw=gushenxing <br>
即可看到**IEC104专属安全协议的控制界面**<br>

3.浏览器输入  0.0.0.0:5000/register?id=123456&name=test2&pw=test2&level=C <br>
即可看到**注册用户**<br>
level=A 可以注册　B级别　C级别用户<br>
level=B 可以注册　C级别用户<br>

4.浏览器输入  0.0.0.0:5000/delete?id=123456 <br>
即可删除id=123456的用户　<br>
level=A 可以删除　B级别　C级别用户　<br>
level=B 可以删除　C级别用户　<br>

5.浏览器输入  0.0.0.0:5000/reset_password?id=12345&pw=0 <br>
即可修改id=12345的用户密码　<br>
level=A 可以修改　自己, B级别, C级别用户 的密码　<br>
level=B 可以修改　自己，C级别用户　的密码　<br>
level=C 可以修改　自己　的密码<br>


5.浏览器输入  0.0.0.0:5000/reset_level?id=12345&level=B <br>
即可修改id=12345的用户级别　<br>
只有　level=A 可以修改　B级别, C级别用户 的级别（修改值 B,　C　两种）<br>


6.浏览器输入  0.0.0.0:5000/all_users <br>
查看到所有的用户的，id，用户名，级别　<br>

7.浏览器输入  0.0.0.0:5000/action_name?name=gushenxing<br>
查看用户名为gushenxing的操作日志　<br>

8.浏览器输入  0.0.0.0:5000/action_time?s_time=2017-01-01 14:32:38&e_time=2017-12-30 14:32:38<br>
查看时间为2017-01-01 14:32:38 ----- 2017-12-30 14:32:38的操作日志　<br>


