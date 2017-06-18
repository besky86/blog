前天看到了partial的一个新用法，记录一下。
# 概念
函数声明如下：
```
functools.partial(func[,*args][, **keywords])
```
返回一个可以像函数一样被调用的partial实例，在调用时使用args和keywords参数。使用python实现时，类似于：
```
def partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(args + fargs), **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc

```
# 通常的使用方法
通常的用法是在原函数声明的参数中，从前往后连续将参数值固定：
```
>>> from functools import partial
>>> def test_partial(a, b, c, d):
...     print a,b,c,d
...
>>> test1 = partial(test_partial,1,2)
>>> test1(3,4)
1 2 3 4
>>> test2 = partial(test_partial,1,2,3,4)
>>> test2(3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: test_partial() takes exactly 4 arguments (5 given)
```
这通常只能把前面的参数固定，假如有个需求和现有的不一样，需要使后面的参数固定，该怎么做？可以使用下面的方法
# 新的使用方法
1.使用关键字参数
```
>>> test3 = partial(test_partial, d=4)
>>> test3(1,2,3)
1 2 3 4
```
2. 其限制

```
>>> test4 = partial(test_partial, c=3, d=4)
>>> test4(1,2)
1 2 3 4
>>> test5 = partial(test_partial, b=2, d=4)
>>> test5(1,3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: test_partial() got multiple values for keyword argument 'b'
```
可以看到，当只对b和d赋值，然后调用时会报错，关键值参数有多个值。我们试试在调用时，使用关键字c看看:

```
>>> test5(1,c=3)
1 2 3 4
```
可以看出，这样也可以正常调用。
3. 如果对前面的参数默认赋值，会出现什么情况？是不是和以前一样，只需要使用列表参数就行了？

```
>>> test6 = partial(test_partial, a=1,b=3)
>>> test6(3,4)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: test_partial() got multiple values for keyword argument 'a'
```
显然不行，最后还是得使用关键字参数进行调用。

# 总结
从上面的运行结果来看，使用partial规则如下：

1. 将前面连续的参数固定，就可以直接继续按照原来的参数继续调用。如
```
 >>> test1 = partial(test_partial,1,2)
 >>> test1(3,4)
 1 2 3 4
```

2. 将后面的连续参数固定，就可以直接继续使用原来的参数进行调用。如
```
>>> test4 = partial(test_partial, c=3, d=4)
>>> test4(1,2)
1 2 3 4
```

3. 如果默认参数值不是连续的或者是直接对前面的连续参数赋值，那么就需要使用关键字参数进行调用，如
```
>>> test5(1,c=3)
1 2 3 4
>>> test6(c=3,d=4)
1 3 3 4
```

