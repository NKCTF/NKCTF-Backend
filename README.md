# NKCTFWeb
为南开 CTF 开发的 Web 项目。

## Django

简单介绍关于 Django。

- 使用命令 `django-admin startproject mysite` 可以初始化一个 Django 项目。

- Django 提供了一个集成了许多管理功能的 Python 脚本 &rarr; **manage.py**

- 一个 Django 项目由许多应用组成，这些应用为 Python 的模块的文件夹，与 manage.py 一起置于根文件夹下，使用 `python manage.py startapp polls` 命令可以初始化创建一个 Django 应用。
- 在应用的文件夹内，一般有以下文件：
  - `models.py`：这个文件表明的数据库的设计方式，内部的一个 Python 类对应着一个数据库中的表单。
  - `admin.py`：这个文件中表明了以管理员方式登录网站时，可以操作的内容。

## ctfsite

Django 项目全部在该文件夹内，以下是关于该项目内容的一些解释：

### `User\`

有关用户信息的数据。登录界面、用户信息界面的视图。

下表为 User 这个应用的数据库设计：

| 表名 | 属性                                                         |
| ---- | ------------------------------------------------------------ |
| User | id &rarr; int, not null, primary key, autoincrement<br />name &rarr; char(32), not null, unique<br />QQ &rarr; char(16), null<br />Description &rarr; char(128), not null<br />Email &rarr; char(32), null<br />BelongTo_id &rarr; int, null, references "user_team" ("id") deferrable initially deferred; |
| Team | id &rarr; int, not null, primary key, autoincrement<br />name &rarr; char(32), not null, unique<br />Description &rarr; char(128), not null |

### `Question`

与题目相关的数据。题目相关界面的视图。

### `Post`

与公告相关的数据。公告展示、编辑公告的视图。