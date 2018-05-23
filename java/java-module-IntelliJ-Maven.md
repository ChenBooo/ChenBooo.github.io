# Java模块化编程在Intellij和Maven中的使用

## 概念
首先要明确Maven Modules, Java Modules和IntelliJ Modules三个不同的概念
- Maven Modules:是将工程组织为子工程的概念。在Maven中，用户可以控制每个模块的版本和模块之间的依赖关系。
- Java Modules:是Java9引入的新语言特性。用于增强类的封装性。并不提供版本控制等功能。
- IntelliJ Modules:是IntelliJ中组织文件的一种方式，在后面的例子中，我们将用其来组织我们的Maven modules。

## 单模块
请下载最新版的IntelliJ。
1.首先创建一个Maven工程。其目录结构如下：
```
├── modules.iml
├── pom.xml
└── src
    ├── main
    │   ├── java
    │   └── resources
    └── test
        └── java
```

2.按照Maven代码组织约定，以src/main/java作为源代码根目录。在src/main/java上右键选择*New - module-info.java*。如果module-info.java选项没有出现在弹窗中，则在src/main/java上右键选择*Open Module Settings*，在*Language level*中，将默认的的Java5修改为Java9，即可激活选项。

3.创建*module-info.java*并且将模块命名为*my.modules.one*。

4.在*src/main/java*右键选择*New - Package*创建包*my.modules.one*.

5.在上面创建的包中，右键选择*New - Java Class*创建*OneModule.java*。内容如下：

```
package my.modules.one;

public class OneModule {
    public static void main(String[] args) {
        System.out.println("One Modules!");
    }
}
```

6.通过*View - Tool Windows - Maven Projects*打开Maven Projects工具面板。在Lifecycle选项中选择clean，然后右键install，选择*Create 'one[install]'...*，这将会打开*Create Run/Debug Configurations*窗口 —— 直接选择*OK*。然后在Maven Projects面板中会出现新项目*Run Configurations*，其中保存了刚才创建的运行配置信息。

7.修改pom.xml文件。系统生成的pom.xml文件内容如下

```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>my.modules</groupId>
    <artifactId>one</artifactId>
    <version>1.0-SNAPSHOT</version>
</project>
```

修改为：

```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>my.modules</groupId>
    <artifactId>one</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.version>3.3.9</maven.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        <jdk.version>1.9</jdk.version>
    </properties>

    <build>
        <pluginManagement>
            <plugins>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <version>3.7.0</version>
                    <configuration>
                        <source>${jdk.version}</source>
                        <target>${jdk.version}</target>
                    </configuration>
                </plugin>
            </plugins>
        </pluginManagement>

        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

8.在之前的*Run Configurations*下的*one[install]*右键选择*Run*, 成功后，one-1.0-SNAPSHOT.jar文件出现在*target*目录中。现在可以通过在工程根目录运行：
```
java --module-path target/one-1.0-SNAPSHOT.jar --module my.modules.one/my.modules.one.OneModule
```
来运行程序。程序输出如下：
```
One Modules!
```

## 多模块
1. 在工程根目录右键选择*New - Module*，然后选择*Next*，设置*Artifactid*为*two*。一下步给模块命名为*my.modules.two*，将模块根目录命名为模块名是一个很好的规范，明确的提示改目录不仅仅是一个Maven module，并且是一个Java module。最后点击*Finish*。创建完成后，目录结构变为：
```
├── modules.iml
├── my.modules.two
│   ├── pom.xml
│   └── src
│       ├── main
│       │   ├── java
│       │   └── resources
│       └── test
│           └── java
├── pom.xml
├── src
│   ├── main
│   │   ├── java
│   │   │   ├── module-info.java
│   │   │   └── my
│   │   │       └── modules
│   │   │           └── one
│   │   │               └── OneModule.java
│   │   └── resources
│   └── test
│       └── java
└── target
```
并且*my.modules.two*被IntelliJ自动添加到根pom.xml文件。

2. 在*my.modules.two*模块的源代码根目录*src/main/java*下，右键*New | module-info.java*创建*module-info.java*文件.

3. 在*my.modules.two*模块的源代码根目录*src/main/java*下创建包*my.modules.two*.

3. 创建在创建的包中添加*TwoModule.java*文件，内容如下：
```
package my.modules.two;

public class TwoModule {
    public static void main(String[] args) {
        System.out.println("Two Modules!");
    }
}
```
 
4. 如之前例子一样，运行*one[install]*编译整个工程。两个模块均被编译成功，并打包为jar文件置于各自的*target*目录下。

5. 运行新创建的模块，可用一下命令：
```
java --module-path my.modules.two/target/two-1.0-SNAPSHOT.jar --module my.modules.two/my.modules.two.TwoModule
```
其输出为:
```
Two Modules!
```

### 模块间依赖
1. 按以上步骤，创建新模块*my.modules.three*。完成后目录结构如下(为简略，部分文件已省略)：
```
├── modules.iml
├── my.modules.three
│   ├── pom.xml
│   ├── src
│   │   ├── main
│   │   │   ├── java
│   │   │   │   ├── module-info.java
│   │   │   │   └── my
│   │   │   │       └── modules
│   │   │   │           └── three
│   │   │   │               └── ThreeModule.java
│   │   │   └── resources
│   │   └── test
│   │       └── java
│   └── target
│       └── three-1.0-SNAPSHOT.jar
├── my.modules.two
│   ├── pom.xml
│   ├── src
│   │   ├── main
│   │   │   ├── java
│   │   │   │   ├── module-info.java
│   │   │   │   └── my
│   │   │   │       └── modules
│   │   │   │           └── two
│   │   │   │               └── TwoModule.java
│   │   │   └── resources
│   │   └── test
│   │       └── java
│   └── target
│       └── two-1.0-SNAPSHOT.jar
├── pom.xml
├── src
│   ├── main
│   │   ├── java
│   │   │   ├── module-info.java
│   │   │   └── my
│   │   │       └── modules
│   │   │           └── one
│   │   │               └── OneModule.java
│   │   └── resources
│   └── test
│       └── java
└── target
    └── one-1.0-SNAPSHOT.jar
```

2. 修改模块*my.modules.two*的*TwoModule.java*,如下：
```
package my.modules.two;

public class TwoModule {
    public static void main(String[] args) {
        System.out.println("Two Modules!");
    }

    public void sayHi(){
        System.out.println("Hi, I am Two Modules!");
    }
}
```

3. 修改*my.modules.two*的*module-info.java*文件，以向外暴露*my.modules.two*包，如下：
```
module my.modules.two {
    exports my.modules.two;
}
```

4.修改*my.modules.three*的*module-info.java*文件，以引入*my.modules.two*模块，如下：
```
module my.modules.three {
    requires my.modules.two;
}
```

5. 在*my.modules.three*模块的pom.xml文件中添加对*my.modules.two*模块的依赖，修改后如下：
```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <parent>
        <artifactId>one</artifactId>
        <groupId>my.modules</groupId>
        <version>1.0-SNAPSHOT</version>
    </parent>
    <modelVersion>4.0.0</modelVersion>

    <artifactId>three</artifactId>
    <dependencies>
        <dependency>
            <groupId>my.modules</groupId>
            <artifactId>two</artifactId>
            <version>1.0-SNAPSHOT</version>
            <scope>compile</scope>
        </dependency>
    </dependencies>
</project>
```
*注：步骤3、4、5的依赖关系添加，IntelliJ均提供快捷键，一般是直接在代码中红色字体上按*Alt+Enter*，按弹出窗口中提示操作即可。此处的步骤3、4为添加Java Module依赖关系，步骤5为添加Maven依赖关系。

6. 修改*my.modules.three*模块的*ThreeModule.java*,如下：
```
package my.modules.three;

import my.modules.two.TwoModule;

public class ThreeModule {
    public static void main(String[] args) {
        System.out.println("Three Modules!");
        TwoModule tm = new TwoModule();
        tm.sayHi();
    }
}
```

7. 编译整个工程，然后运行*my.modules.three*，如下：
```
java --module-path my.modules.two/target/two-1.0-SNAPSHOT.jar:my.modules.three/target/three-1.0-SNAPSHOT.jar --module my.modules.three/my.modules.three.ThreeModule
```
因为*my.modules.three*依赖*my.modules.two*,所以运行*my.modules.three*时，需要同时在--module-path下指定两个模块的路径，其运行输出如下：
```
Three Modules!
Hi, I am Two Modules!
```

## 总结
在多模块情况下，情况变的比较微妙，如果仔细对比，可以发现从第二个创建的模块开始，其pom.xml文件相较与第一个模块的pom.xml文件，其多了以下内容:
```
<parent>
    <artifactId>one</artifactId>
    <groupId>my.modules</groupId>
    <version>1.0-SNAPSHOT</version>
</parent>
```
即之后创建的模块与第一个模块之间都是父子关系，此处引入一个问题就是子模块可以添加对父模块的依赖，但是如果父模块企图添加对子模块的依赖时，就会编译错误，提示存在环形依赖。这是因为pom存在以上内容时，其实已经引入了子模块对父模块的依赖，所以当添加父模块对子模块的依赖时就形成了环形依赖，如果想要创建是创建的所有模块均处于平等关系，可以去掉<parent>标签。







