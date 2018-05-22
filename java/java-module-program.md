## 代码迁移
之前代码迁移至Java9时，仍然可以使用-cp风格命令编译、运行。然而由于之前工程依赖许多非模块化的jar包。迁移后，为了保证代码能正常运行，生成的镜像仍然会包含几乎整个jre，所以降低了其优势。要完全体现新编程组织方式的优势，仍然有待整个社区对模块化编程思想的接受与支持。

## 模块化编程
在Java9中引入了一种新的特性——模块化编程。该特性影响了，从Java诞生以来的代码组织结构，解决了以往结构中存在的部分缺陷。

## 模块化带来的优势
1. 更强的封装特性
1. 可靠的配置
1. 更高效的部署和效率

### 更强的封装特性
Java9之前，当希望某模块只供内部使用时，开发者往往会遇到障碍。一旦包的使用者利用某种方法使用了设计为内部使用的模块时，
就限制了包创建者的灵活性。当想使用更好的内部模块时，因为旧模块已经被客户使用，为了兼容性，创建者可能不得不在新设计不再使用旧模块时保留它。

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

--module-source-path：告知编译器模块的源代码位置。

--module-path：告知编译器/运行时编译好的模块所在位置，以便用于编译或者运行模块。

## 模块之间的依赖
在Java9中引入了module，requires，exports关键字，其只在module-info.java中起作用，所以模块其他代码中使用时，并不会被当做关键字处理。
1. module用于在module-info.java中申明模块名。

2. requires用于声明本模块所依赖的外部模块，其格式如下：
```
module my.module.name {
    requires outer.module1.name;
    requires outer.module2.name;
}
```
requires后跟依赖的外部模块名，依赖多个外部模块时，可使用多个requires关键字。在添加了requires引入外部模块后，即可使用该模块中exports的包中的public类。

3. exports用于声明本模块允许外部模块使用的包，其格式如下：
```
module my.module.name {
    exports my.export.package1;
    exports my.export.package2;
}
```
exports向外界暴露模块中的包，这样未暴露的包中，即使public类也无法被外部使用，增强了模块的封装性。

## 创建Java运行镜像的步骤
### 工具：jlink
其使用如下：
```
jlink --module-path <module-path-locations> --add-modules <starting-module-name> --output <output_location>
```
其中：

--module-path：指定模块路径。jlink将在该路径下寻找所需要的，已经编译好的模块。

--add-modules：指定启动模块依赖扫描开始模块。可以为多个，为多个时用,分割。通过起点模块迭代扫描模块requires的模块，从而获得整个依赖拓扑。从而获知镜像应包含哪些模块。

--output：指定输出路径。指定镜像的输出目录。

如果出现Error: Module java.base not found错误，表示jlink无法找到java.base模块，则手动将模块所在路径添加到--module-path中即可，不同路径间使用:分割（windows中使用;分割）。

创建的镜像目录结构如下：
```
image
├── bin
├── conf
├── include
├── legal
└── lib
```

jlink还支持插件，其中
--compress可以压缩生成的镜像，=0表示不压缩，=1表示字符串共享，即程序中出现的字符串常量都会被去重。=2使用zip压缩。

--include-locales。jlink默认会携带所有已安装的本地信息，如果能确定进程的运行环境，可以通过该命令指定包含的本地信息，如--include-locales=en.也可以有效的降低镜像的大小。该项似乎只能搭配--bind-services一起使用，原因未明。

### 运行镜像
在输出目录下运行
```
bin/java --module <root-module>/<main-class>
```

## 模块打包
```
jar --create --file <out-location>/<out-jar-name> --module-version=<1.0> -C <module-path-locations> .
```
--create选项告诉jar工具需要创建一个jar文件。
-C指定编译好的class文件位置，其值得格式为<folder> <file>。上式命令中<module-path-locations>即代表floder，.表示在floder文件夹下的所有文件都被包含。
--module-version指定jar文件的版本。
--file指定输出jar文件名。

当打包包含main方法的模块时，可添加--main-class=<main class>.
