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
其中T只是类型参数的占位符，并无特别含义，可以使用任何满足Java变量名称命名规则的名称代替。使用泛型类时，其类型参数需要在构造类对象时指定，如上示例所示，在实例化GenericClass对象时，指定其类型参数为String。以此GenericClass成为一个泛型类，其可以作用于任何类型。

### 泛型接口
定义泛型接口的语法与泛型类基本相同。
```
public interface GenericInterface<T> {
    T get();
}

class SomeImplements implements GenericInterface<Double> {
    public Double get() {
        return 0D;
    }
}
```
如上例，在实现接口时只需指定具体的参数类型，即可泛化出支持不同数据类型的接口类型。

### 泛型方法
泛型方法可以存在于非泛型类中。即其可以独立于所在类单独实现泛化。
```
public class OrdinaryClass {
    public <T> void genericMethod(T arg) {
        System.out.println(arg.getClass().getName());
    }

    public static void main(String[] args) {
        OrdinaryClass ordinary = new OrdinaryClass();
        ordinary.genericMethod("");
        ordinary.genericMethod(1);
    }
}/* Output:
java.lang.String
java.lang.Integer
*///:~
```
上例中值得注意的是，当普通类型作为实参传入时，会自动包装为对应的类，如例子中int型参数自动包装为Interger类；泛型方法的类型参数位于其返回值之前。
### 泛型引起的问题
在Java中，是通过消除参数的类型信息来实现泛型的，所以当泛型的操作需要具体的类型信息时需要额外提供类型信息。
```
class Erased<T> {
    private static final int SIZE = 100;
    public static void f(Object arg){
        if(arg instanceof T){}              //Error
        T var = new T();                    //Error
        T[] array = new T[SIZE];            //Error
        T[] array = (T)new Object[SIZE];    //Error
    }
}
```
解决这个问题的一个方案是，可以为泛型提供额外的类型参数--Class<T>,这样可以调用Class提供的接口来实现创建对象等操作。同时，也可以是用工厂函数来创建所需要的实例对象。
