# 1. 使用app的原因
django有一套工具用来生成每个app的基本目录，这样就可以专心撸代码，而不是创建文件夹。一个工程里面可以包含多个app.

# 2. url映射
在django中，路由表映射有两个主要的函数：include和url，include, url，
## 2.1 在普通app中urls.py
````
from django.conf.urls import url
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
````
url(regex, view, kwargs=None, name=None):
*     regex: 匹配uri
*     view: 匹配之后进行处理
*     kwargs: 参数
*     name: url标识

## 2.2 在工程app中urls.py
```
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
]

```
在这里， url中的，url需要以`/`结尾。
include方法：
```
include(module, namespace=None, app_name=None)
include(pattern_list)
include((pattern_list, app_namespace), namespace=None)
include((pattern_list, app_namespace, instance_namespace))
```
各个参数如下：
	•	module – URLconf module (or module name)
	•	namespace (string) – Instance namespace for the URL entries being included
	•	app_name (string) – Application namespace for the URL entries being included
	•	pattern_list – Iterable of django.conf.urls.url() instances
	•	app_namespace (string) – Application namespace for the URL entries being included
	•	instance_namespace (string) – Instance namespace for the URL entries being included



