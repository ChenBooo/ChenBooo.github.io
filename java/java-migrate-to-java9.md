# 代码迁移至Java9
之前代码迁移至Java9时，仍然可以使用-cp风格命令编译、运行。然而完全体现新编程组织方式的优势，仍然需要将旧代码迁移至Java9。

## 模块化编程

## 问题
除了将自己的代码以Java9的模块化形式组织以外，迁移最大的问题，是应用依赖的第三方库。之前位于classpath中的Jar包怎样在Java9使用的问题。

## 自动模块
Java9之前的Jar包可以简单的直接放到--module-path中，如此Java9编译运行之前的代码都没有问题。这里Java9采取的策略是为每个Jar自动生成一个对应模块，其模块名是Jar包名，其中-被替换为.，版本信息被去掉，示例如下：

JAR file name | Automatic module name
commons-lang-1.2.10.jar | commons.lang
spring-core-4.3.10.RELEASE.jar | spring.core
guice-4.1.0.jar | guice

而为了保证自动包的运行，自动包自动requires transitive所有可发现的模块，并且export所有的包。

### 问题
Java9模块中不允许分包，即不允许同一个包存在于多个模块中。然而同一个包是可以存在多个Jar文件中的，当欲将分享包的多个Jar文件自动化模块时，是无法成功的，并且也没有什么有效的手段可以绕过这个限制，只能由包的开发者修复。

## 使用Jdeps创建模块的描述文件
其语法如下：
```
jdeps --generate-module-info <output-location> <path-to-jars>
```
比如，运行一下命令：
```
jdeps --generate-module-info out lib/commons-collections4-4.1.jar
```
其输出为
```
writing to out/commons.collections4/module-info.java
```
如上输出所示，jdeps已经成功为Jar包生成了模块描述文件，模块名与之前自动包模块名生成规则相同。

运行时可以同时指定多个Jar文件，特别是当Jar文件间存在依赖关系时，同时指定，jdeps还可以自动处理它们之间的依赖关系。

改功能只作为一个起点，因为Jdeps无法确定最优的模块描述。同时Jdeps只做静态分析，所以无法捕获任何库的运行时反射使用。
