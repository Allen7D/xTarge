安装Server端（产生Iec104和Modbus的Server）：

1.将Modbus和Iec的文件夹放在一定的目录下：如 /usr/local/safe/ （接下来将以此目录为例）

	（1）$ cd /usr/local/ 

	（2）$ sudo mkdir safe

	（3）$ cd safe/

	（4）将两个文件夹移动至此

2.在/etc/下新建一个文件夹safe，并将iec104.json和modbus.json移动到此

	（1）cd /etc/safe/

	（2）将两个文件移动至此

	（3）$sudo chmod 755 modbus.json  iec104.json

3. 运行Modbus 的Server

	（1）$cd /usr/local/safe/Modbus/server_debug

	（2）$sudo ./server

4. 运行Iec104 的Server

	（1）$cd /usr/local/safe/IEC/GuyiIec

	（2）$sudo ./server





安装前后端步骤：

1.在一定目录下（比如/usr/local/safe/）: 

	$ git clone https://github.com/bodanli159951/xTarge

2.前端:

	(1)$ cd /usr/local/safe/xTarge/

	(2)$ npm install

	(3)$ npm run build  #封装成固定网页

	(4)$ npm run dev

	(5)在chrome浏览器上输入“localhost:9527"

3.后端:

	(1)$ cd /usr/local/safe/xTarge/

	(2)$ sudo apt-get install pip

	(3)$ pip install -r requirements.txt 

	(4)$ python manage.py db initUser

	(5)$ python manage.py db showUser

	(6)$ sudo python targe.py

