# 后端文档

## RESTful API 接口规范
**API 参考写法**

1、[github 开发者api接口](https://developer.github.com/v3/) 

2、[豆瓣 开发者api接口](https://developers.douban.com/wiki/?title=api_v2)

**HTTP动词**
> 1、POST:创建<br>
2、PUT:更新<br>
3、GET:查询<br>
4、DELETE:删除<br>


**状态码 statusCode**

<table>
<tr><td><em>状态码</em></td><td><em>含义</em></td><td><em>说明</em></td></tr>
<tr><td>200</td><td>OK</td><td>请求(删除)成功</td></tr>
<tr><td>201</td><td>CREATED</td><td>创建成功</td></tr>
<tr><td>202</td><td>ACCEPTED</td><td>更新成功</td></tr>
<tr><td>400</td><td>BAD REQUEST</td><td>请求的地址不存在或者包含不支持的参数</td></tr>
<tr><td>401</td><td>UNAUTHORIZED</td><td>未授权</td></tr>
<tr><td>403</td><td>FORBIDDEN</td><td>被禁止访问</td></tr>
<tr><td>404</td><td>NOT FOUND</td><td>请求的资源不存在</td></tr>
<tr><td>500</td><td>INTERNAL SERVER ERROR</td><td>内部错误</td></tr>
</tbody>
</table>

**错误码 errorCode**

<table>
<tbody>
<tr><td>错误码</td><td>错误信息</td><td>含义</td><td>status code</td></tr>
<tr><td>999</td><td>unknow_error</td><td>未知错误</td><td>500</td></tr>
<tr><td>1000</td><td>need_permission</td><td>需要权限</td><td>401</td></tr>
<tr><td>1001</td><td>uri_not_found</td><td>资源不存在</td><td>404</td></tr>
<tr><td>1002</td><td>missing_args</td><td>参数不全</td><td>400</td></tr>
<tr><td>1003</td><td>error_args</td><td>参数错误</td><td>400</td></tr>
</tbody>
</table>

**错误写法**
> /getuser/:id

**推荐写法**
> GET: /user/:id


## 服务器 API 写法
**Flask 的 API 写法**

```
待定
```


**Node.js 的 Express 框架 API 写法**

```
// apiAuthentication，为「验证权限」的中间件
app.use(apiAuthentication)
// idMustBePostiveInt为「验证id参数」的中间件
// users为封装后的「mongoose查询方法」
app.get('/users', users.findAll)
app.get('/users/:id', idMustBePostiveInt, users.findById)
app.post('/users', users.add)
app.put('/users/:id', idMustBePostiveInt, users.update)
app.delete('/users/:id', users.delete)
```

### 一、用户 API
1、获取所有用户 GET /api/users
前端已经获取了所有uses的信息，可以基于id进行修改
users返回格式如下：
1.1正确结果，格式

```
[{
'id': 111111,
'username': 'admin',
'level': 'A',
'regtime': '2016/05/02 15:25:25'
},
{

},
]
```
1.2错误结果，格式

```
{
'code': 1000,
'msg': 'need_permission',
'request': 'GET /api/users'
}
```
同时修改状态码，HTTP Status Code为401（如400，403，404）

2、获取某个用户 GET /api/user/:id
2.1正确结果，格式(对象)

```
{
'id': 111111,
'username': 'admin',
'level': 'A',
'regtime': '2016/05/02 15:25:25'
}
```
2.2错误结果，格式

```
{
'code': 1001,
'msg': 'uri_not_found',
'request': 'GET /api/users/717171'
}
```

3、修改某个用户信息 PUT /api/user/:id

3.1正确结果

返回status = 202

4、新增用户 POST /api/user

4.1正确结果

返回status=201

5、删除某个用户 DELETE /api/user/:id

5.1正确结果

返回status=200


### 二、警报日志 API


### 三、操作日志 API









<POST>登录用户，post传入用户信息 post("http://127.0.0.1:5000/login", data=user_info)　　　需要：post（username,password）
<GET>登出用户， get("http://127.0.0.1:5000/logout")   　不需要参数
#################
<GET>查看所有用户　get("http://127.0.0.1:5000/api/users")　 无级别限制，不需要参数

<POST>新建用户，<PUT>重置用户，<DELETE>删除用户，url中通过tag来传入操作者id，post/put/delete中传入被操作者信息，以及操作者的密码，即admin_password
      post("http://127.0.0.1:5000/api/users?tag=111111", data=user_info)　    需要：url(tag), post (user_id,username,password,level,admin_password)
      put("http://127.0.0.1:5000/api/users?tag=111111", data=user_info)      需要：url(tag), put (user_id,new_password,admin_password)或put (user_id,new_level,admin_password)
      delete("http://127.0.0.1:5000/api/users?tag=111111", data=user_info)　　　需要：url(tag), delete (user_id,admin_password)
################
<GET>查看操作日志by用户id　　　get("http://127.0.0.1:5000/api/action_id", data=user_info)　　需要：get(user_id)
<GET>查看操作日志by时间　　　get("http://127.0.0.1:5000/api/action_time", data=user_info)　　需要：get(s_time,e_time)   开始，结束时间
<GET>查看所有alert        　get("http://127.0.0.1:5000/api/alert")　 无级别限制，不需要参数

自己用client.py跑跑看

