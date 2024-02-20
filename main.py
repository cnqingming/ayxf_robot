print("hello world")


#class后面是类名，一般是大写开头的单词。接着是继承类，没有合适的就使用（object)
class Student(object):
    #用__init__创建实例，（）内绑定的是属性，第一个参数永远是实际变量self
    def __init__(self, name: str, score: int):
        self._name = name
        self._score = score

    def print_score(self):
        print(self._name + str(self._score))

#如果student实例本身就有这些数据，我们就可以直接从student类内部去访问函数，这就是数据的封装。如果在属性名称前面加_,就变成了
#private的变量，如果需要修改，可以增加set_score
bart = Student(name="bart", score=59)
bart.print_score()
