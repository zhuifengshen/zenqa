# QA之禅

```
安装覆盖率检测工具
$ pipenv install coverage --dev
清除上一次的统计信息
$ pipenv run coverage erase
运行 django 单元测试
$ pipenv run coverage run manage.py test
生成覆盖率统计报告
$ pipenv run coverage report
生成HTML报告
$ pipenv run coverage html


新建配置文件：.coveragerc

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

配置文件浅析：
branch = True  是否统计条件语句的分支覆盖情况。if 条件语句中的判断通常有 True 和 False 两种情况，设置 branch = True 后，Coverage 会测量这两种情况是否都被测试到。
source = .  指定需统计的源代码目录，这里设置为当前目录（即项目根目录）。
omit 配置项可以指定排除统计的文件。
show_missing = True  在生成的统计报告中显示未被测试覆盖到的代码行号。
skip_covered  配置项可以指定统计报告中不显示 100% 覆盖的文件。


.gitignore配置
htmlcov/
.coverage
.coverage.*
coverage.xml
*.cover
```

