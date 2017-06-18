最近使用了celery，但用着感觉不是很爽，因为它需要把worker和任务调用的逻辑放在同一个工程里面。所以，当分布式使用时，需要将这个工程复制到不同的机器上，而不是将worker与任务调用的逻辑分开。

这段时间都在思考如何摆脱这个限制，想到了一个方案：

1. 一般，celery任务调用如下：

````
@app.task
def add(x, y):
    return x + y
    
from tasks import add
add.delay(4, 4)
````

以上调用都是基于可以引用到方法add的基础上可行的

2. 那么我们如果把没有什么特殊限制的任务在这个基础上做的更通用一点是不是可以更好一点，如果在再在这个通用的基础上做成一个基础库，到需要配置的机器上安装，就可以在不同的工程上直接使用了，不必worker和任务调用逻辑混在一起了

3. 如何通用？

  联想到http请求，我们只要绑定自己的请求参数，请求方法，访问对应的url就行了，这都是统一的。
  参考其数据结构,我们可以定义一个通用的方法,例子为：
  
  客户端：
  ````
  @app.task
  def revoke_task(method, data):
      taskhandler = get_handler(method)
      result = taskhandler.deal(data)
      return result
  ````
简单的想法如上文所说，由于没有考虑celery中频率限制等特性，因此，上述的方案看来只适用于那些没有什么条件限制的任务。

望大家指正！




