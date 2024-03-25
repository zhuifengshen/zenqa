# QA之禅

欢迎来到 QA之禅 空间

QA 的未来是自动化、场景化、服务化，质量保障之路任重而道远，从这里开始，记录修炼内功的点点滴滴！

创新决定我们飞得有多高，质量决定我们走得有多远，正如著名的质量管理学家朱兰博士所说：“20世纪是生产率的世纪，21世纪是质量的世纪，质量是和平占领市场最有效的武器！”


### 本地开发调试
```
1、进入项目根目录，安装开发依赖
$ pipenv install --dev

2、生成数据库文件
$ pipenv run python manage.py migrate

3、生成测试数据
$ pipenv run python -m scripts.fake

4、运行开发服务器
$ pipenv run python manage.py runserver

5、进入博客首页：http://127.0.0.1:8000/

6、进入博客后台：http://127.0.0.1:8000/admin/  （账号admin，密码admin）

7、开发代码上传GitHub后，自动化部署最新代码
$ pipenv run python -m scrpits.fabfile
```


### 服务器部署运行
```
1、软件依赖：Python3、pipenv、Nginx

2、进入项目根目录，安装运行依赖
$ pipenv install

3、生成数据库文件
$ pipenv run python manage.py migrate

4、生成静态文件
$ pipenv run python manage.py collectstatic

5、创建后台管理员账户
$ pipenv run python manage.py createsuperuser

6、运行项目
sudo vim /etc/systemd/system/zenqa.service

[Unit]
Description=zenqa web gunicorn daemon
After=network.target
[Service]
User=zion
Group=zion
WorkingDirectory=/home/zion/zenqa
ExecStart=/home/zion/.local/share/virtualenvs/zenqa-pPXffCct/bin/gunicorn --access-logfile - --workers 2 --timeout 3600 --bind 0.0.0.0:7788 zenofqa.wsgi:application
[Install]
WantedBy=multi-user.target

sudo systemctl enable zenqa.service
sudo systemctl start/stop/status zenqa.service
sudo systemctl reload

7、配置Nginx
server {
    charset utf-8;
    listen 80;
    server_name zenqa.cn;

    location /static {
        alias /home/zion/zenqa/static;
    }

    location / {
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:7788;
    }
}

7、浏览器访问：https://zenqa.cn
```


### 本地运行单元测试
```
1、清除上一次的统计信息
$ pipenv run coverage erase

2、运行单元测试
$ pipenv run coverage run manage.py test

3、生成覆盖率统计报告
$ pipenv run coverage report

4、生成HTML报告
$ pipenv run coverage html

5、查看HTML报告
$ open htmlcov/index.html
```


### 测试覆盖率配置
```
1、安装覆盖率检测工具
$ pipenv install coverage --dev

2、新建配置文件：.coveragerc

[run]
branch = True
source = .
omit = 
  _credentials.py
  manage.py
  zenofqa/settings/*
  zenofqa/wsgi.py
  scripts/*
  */migrations/*

[report]
show_missing = True
skip_covered = True


3、配置文件浅析：
branch = True  是否统计条件语句的分支覆盖情况。if 条件语句中的判断通常有 True 和 False 两种情况，设置 branch = True 后，Coverage 会测量这两种情况是否都被测试到。
source = .  指定需统计的源代码目录，这里设置为当前目录（即项目根目录）。
omit 配置项可以指定排除统计的文件。
show_missing = True  在生成的统计报告中显示未被测试覆盖到的代码行号。
skip_covered  配置项可以指定统计报告中不显示 100% 覆盖的文件。


4、.gitignore新增配置
htmlcov/
.coverage
.coverage.*
coverage.xml
*.cover
```

