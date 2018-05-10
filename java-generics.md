# Java泛化


## 为什么需要泛化
普通的类和方法都作用于特定类型：基本类型或者类。如果想要编写可以同时作用于多种类型的类和方法，就需要引入泛化。


## 多态
面向对象语言引入泛化的一种机制是多态。可以实现一个方法，其使用基类作为参数，然后实际运行时可以将该基类的任何派生类作为参数传入该方法，以此获取更大的灵活性。


## 泛型
使用java支持的泛型语法，以实现更加灵活的泛化。

### 泛型类
可以使用类型参数来实现类的泛型。如下：
```
public class GenericClass<T> {
    private T field;
    public GenericClass(T field) { this.field = field;}
    public T get() {return field; }
    public static void main(String[] args){
        GenericClass<String> generic = new GenericClass<String>("generic class");
        String context = generic.get();
        System.out.println(context);
    }
}
```
其中T只是类型参数的占位符，并无特别含义，可以用其他任何满足Java变量名称命名规则的名称代替。使用泛型类时，其类型参数需要在构造类对象时指定，如以上示例所示，在实例化GenericClass对象时，指定其类型参数为String。以此GenericClass成为一个泛型类，其可以作用于任何类型。

### 泛型接口
定义泛型接口的语法与泛型类基本相同。
```
interface GenericInterface<T> {
    T get();
}

class SomeImplements implements GenericInterface<Double> {
    public Double get() {
        return 0D;
    }
}
```
如上例，在实现接口时只需指定具体的参数类型，即可泛化出支持不同数据类型的接口类型。
