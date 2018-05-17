## 模块化编程
在Java9中引入了一种新的特性——模块化编程。该特性影响了，从Java诞生以来的代码组织结构，解决了以往结构中存在的部分缺陷。

## 模块化带来的优势
1. 更强的封装特性
1. 可靠的配置
1. 更高效的部署和效率

### 更强的封装特性
Java9之前，当希望某模块只供内部使用时，开发者往往会遇到障碍。一旦包的使用者使用利用某种方法使用了设计为内部使用的模块时，
就限制了包创建者的灵活性。当想使用更好的内部模块时，因为该模块已经被客户使用，为了兼容性，创建者可能不得不在新设计不再使用旧模块时保留它。

### 可靠的配置
由于Java9之前的classpath工作方式，无法在部署应用时，检查环境中是否包含所有应用需要的类，直到应用运行时调用该类，如果无法加载，才抛出
NoClassDefFoundError.

### 更高效的部署和效率
在Java9之前部署应用时，不得不包含整个jre。即使其中有很多类是应用并不需要的。这不仅导致更大的发布文件，同时jvm会加载大量并未
使用的类，浪费内存，降低效率。

## 编写一个自己的模块
1.安装Java9.可以使用openjdk.下载地址http://jdk.java.net/9
2.工程目录结构
```
└── src
    └── test.module             -----------模块根目录
        ├── module-info.java    -----------模块定义文件
        └── test                -----------|包目录
            └── module          -----------|
                └── Main.java   -----------java 源代码
```
*注意，上示的目录结构中，模块根目录名与包名并不要求相同，模块根目录名即为模块名，其只需要满足java命名规则，可为模块的唯一标识即可，推荐使用包的命名
约定，使用域名反转的格式。

module-info.java内容如下：
``` 
module test.module {
}
```
module-info.java为模块定义文件，其文件名不能更改。

Main.java
```
package test.module;
public class Main {
    public static void main(String[] args) {
	System.out.println("Hello World!");
    }
}
```

3.编译
```
javac --module-source-path src -d out src/test.module/test/module/Main.java src/test.module/module-info.java
```

4.运行
```
java --module-path out --module test.module/test.module.Main
```
上面出现的新命令选项--module-source-path，--module-path非常类似于之前版本中的-sourcepath和-classpath

module-source-path:告知编译器模块对应的源代码位置。

module-path：告知编译器/运行时编译好的模块所在位置，以便用于编译或者运行模块。

## 模块之间的依赖
在Java9中引入了module，requires，exports关键字，其只在module-info.java中其作用，所以模块其他代码中使用时，并不会被当做关键字处理。
1. module用于在module-info.java中申明模块名。
1. requires用于声明本模块所依赖的外部模块，其格式如下：
```
module my.module.name {
    requires outer.module1.name;
    requires outer.module2.name;
}
```
requires后跟依赖的外部模块名，依赖多个外部模块时，可使用多个requires关键字。在添加了requires引入外部模块后，即可使用该模块中exports的包中的类。
1. exports用于声明本模块允许外部模块使用的包，其格式如下：
```
module my.module.name {
    exports my.export.package1;
    exports my.export.package2;
}
```
exports想外界暴露模块中的包，这样未暴露的包中，即使public类也无法被外部使用，增强了模块的封装性。
