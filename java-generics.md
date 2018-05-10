# Java泛化


## 为什么需要泛化
普通的类和方法都作用于特定类型：基本类型或者类。如果想要编写可以同时作用于多种类型的类和方法，就需要引入泛化。


## 多态
面向对象语言引入泛化的一种机制是多态。可以实现一个方法，其使用基类作为参数，然后实际运行时可以将该基类的任何派生类作为参数传入该方法，以此获取更大的灵活性。


## 泛型
使用java支持的泛型语法，以实现更加灵活的泛化。

### 泛型类
可以使用类型参数来实现类的泛型。如下：
'''
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
'''
其中T只是类型参数的占位符，并无特别含义，可以用R之类其他名称代替。
