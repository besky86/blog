# Python中实例的attributes、Properties以及Descriptors

在很多的语言中，实例的属性都有对应的实例变量与之对应，但在Python中，还可以使用其他的方式：

1. Properties:

   即通过使用Python中内置方法property为一个Attrbute名绑定对应的getter、setter、deletter方法，或者通过@property装饰器，这样，就可以直接通过变量名对实例变量进行访问。

2. Descriptors：
	 一个描述器是一个具有绑定行为的对象属性，其访问控制被描述器协议重写。这些方法包括`__get__()`, `__set__()`, 和 `__delete__()`方法,只要重写了这三个方法中的任何一个，就是实现了描述器协议。

#1. 直接通过实例变量访问
通常情况下，都是直接通过instance.variablename来对实例中的对象进行访问。

例子1：
```
>>> class A(object):
...     pass
... 
>>> a = A()
>>> dir(a)
['__class__', '__delattr__', '__dict__', '__doc__',
 '__format__', '__getattribute__', '__hash__', '__init__', 
 '__module__', '__new__', '__reduce__', '__reduce_ex__', 
 '__repr__', '__setattr__', '__sizeof__', '__str__', 
 '__subclasshook__', '__weakref__']
 
>>> a.__dict__
{}
>>> a.attr1 = 1
>>> dir(a)
['__class__', '__delattr__', '__dict__', '__doc__', 
'__format__', '__getattribute__', '__hash__', '__init__', 
'__module__', '__new__', '__reduce__', '__reduce_ex__', 
'__repr__', '__setattr__', '__sizeof__', '__str__', 
'__subclasshook__', '__weakref__', 'attr1']

>>> a.__dict__
{'attr1': 1}
>>> 
```
从上面的例子中，可以看出，直接对实例添加实例变量，是直接在实例中`__dict__`添加的。因此，这种是直接进行访问。


#2. 通过Property

property是一种创建数据描述器的简洁方式，使得在访问属性时，会对触发对应的方法调用。

```

class C(object):
    def getx(self):
        print 'getx'
        return self.__x

    def setx(self, value):
        print 'setx'
        self.__x = value 

    def delx(self):
        print 'delx'
        del self.__x
        x = property(getx, setx, delx, "I'm the 'x' property.") 
  
instances = C()
instances.x = 5
print instances.x
del instances.x

output：-----
setx
getx
5
delx
```
在上面的代码中，如果将`x = property(getx, setx, delx, "I'm the 'x' property.")`换成`x = property(fget=getx, fdel=delx, doc="I'm the 'x' property.")`，那么调用instances.x会报错`AttributeError: can't set attribute`.

# 3. 通过Descriptors
**Descriptor只对新式类有效**

如果一个对象定义了`__set__`和`__get__`两个方法，那可以成为是一个data-descriptor，如只有`__get__`,那么被成为non-data descriptor。在data-descriptor中，访问属性时，优先使用data-descriptor,而在non-data descriptor中优先使用的是字典中的属性。

> 技巧： 如果想做一个只读的descriptor，那么就可以同时定义 `__get__() `and `__set__()` , 其中 调用`__set__()`时抛出AttributeError异常即可。


## 3.1 调用顺序
1.  `__getattribute__() `
2. data-descriptor
3. 实例字典
4. non-data descriptor
5. `__getattr__`，处理查询不到的属性。


这里可以做很多很多文章。后面进行整理。

data-descriptor  查询顺序：类-基类-实例字典
non-data descriptor 查询顺序：实例字典-类-基类


## 3.2 示例
```
class RevealAccess(object):
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print 'Retrieving', self.name
        return self.val

    def __set__(self, obj, val):
        print 'Updating', self.name
        self.val = val

>>> class MyClass(object):
...     x = RevealAccess(10, 'var "x"')
...     y = 5
...
>>> m = MyClass()
>>> m.x
Retrieving var "x"
10
>>> m.x = 20
Updating var "x"
>>> m.x
Retrieving var "x"
20
>>> m.y
5

```


**重点：**

  *   **descriptors方法被 `__getattribute__() `方法调用,每次访问都会进行调用`__getattribute__() `方法。**
  *	重写 `__getattribute__()`可以阻止系统子自带的descriptor调用
  *	`__getattribute__()` 只能被新式的类和实例有效，对于类和实例，调用方法`object.__getattribute__()` and `type.__getattribute__()`时，对调用 `__get__()`方法是不一样的.
  *	data descriptors优先于实例字典。
  *	non-data descriptors 可能被实例字典重写，因为实例字典的优先级总是高于non-data descriptors。
  *  **descriptor的实例自己访问自己是不会触发__get__，而会触发__call__，只有descriptor作为其它类的属性才有意义。**

> 参考文档

>  *   [Attributes, Properties and Descriptors
](http://itmaybeahack.com/book/python-2.6/html/p03/p03c05_properties.html#objects-properties-desc)



