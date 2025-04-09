# 食品溯源系统

服务启动命令：

在 `FoodTrace` 文件夹下执行以下命令

```shell
python manage.py runserver 0.0.0.0:8000
```

创建数据表：

数据库配置信息在 `FoodTrace` 包中 `setting.py` 文件中的 `DATABASES` 下

表结构在 `app01` 包下的 `models.py` 文件里定义

使用以下命令 创建/更新 表

```shell
python manage.py makemigrations
python manage.py migrate
```



在MySQL中查询用户信息：

```shell
## 在本地登陆 mysql
/usr/local/mysql/bin/mysql -u root -p
## 打开数据库
use foodtrace;
## 查看所有表
show tables;
## 查看用户表的所有信息
select * from app01_userinfo;
```

