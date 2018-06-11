- [分布式系统](#分布式系统)
    - [分布式面对的难题](#分布式面对的难题)
- [ZooKeeper](#ZooKeeper)
    - [安装](#安装)
    - [配置文件](#配置文件)
    - [启动](#启动)
    - [启动客户端](#启动客户端)
    - [设置zk集群](#设置zk集群)
- [ZooKeeper的内部机制](#ZooKeeper的内部机制)
    - [zookeeper数据模型](#zookeeper数据模型)
    - [znode类型](#znode类型)
        - [持久节点](#持久节点)
        - [临时节点](#临时节点)
        - [序列化节点](#序列化节点)
    - [zookeeper watches](#zookeeper watches)
    - [zookeeper操作](#zookeeper操作)
    - [zookeeper访问控制列表](#zookeeper访问控制列表)
    - [zookeeper状态信息](#zookeeper状态信息)
    - [会话](#会话)
- [zookeeper编程](#zookeeper编程)
    - [连接zk服务](#连接zk服务)
    - [实现watch](#实现watch)
    - [成员管理](#成员管理)
- [常见分布式问题的zookeeper方案](#常见分布式问题的zookeeper方案)
    - [屏障](#屏障)
    - [队列](#队列)
    - [锁](#锁)
    - [选举](#选举)
    - [组成员服务](#组成员服务)

<a name="分布式系统"></a>
# 分布式系统
所谓分布式系统，即由相互独立的计算机通过网络组合在一起，通过通信和协作完成一个共同目标的软件系统。例如电子邮件系统、多人在线游戏系统等。

<a name="分布式面对的难题"></a>
## 分布式面对的难题
- 网络是不稳定的。联通组件的网络可能因为外部原因失效，比如断电。
- 网络延迟。分布式系统中的组件可以位于全球任何地点，而组件间的数据传输是需要时间的。所以网络的服务质量会影响应用的延时。
- 有限带宽。虽然网络带宽不断提速，但仍然是有限的，且不同地区带宽也存在差别。
- 网络安全。网络从来都是不安全的，比如可能遭遇拒绝服务攻击。
- 系统拓扑变化。实际应用中，分布式系统的拓扑从来不是固定的。随着时间推移，系统中的组件会被移除或添加。
- 不存在管理员。分布式系统组件无法孤立的完成任务。他们通过与其他组件的交互来完成功能，而其他组件可能不在管理员的控制之下。
- 传输代价。网络传输不仅仅会消耗计算机资源，如CPU时间等。还需要给网络服务商付费。
- 网络不均匀。网络是由大量不同设备组合而成。因此要让分布式系统正确的运转，需要处理不同网络，操作系统，甚至不同的程序语言。

分布式系统设计者不仅要面对以上问题，更是需要解决如何协调系统中不同组件的运作，这是一个复杂的工程。zookeeper被设计的初衷就是为了解决这个问题，从而使分布式系统开发可以更加快捷、高效。

<a name="ZooKeeper"></a>
# ZooKeeper
ZooKeeper是一个开源的，提供高性能和高可靠性的分布式应用协调服务。其可用于常见的分布式协调问题，如：
- 配置信息管理
- 命名服务
- 分布式的同步，例如锁。
- 集群成员操作，例如判别成员的离开和加入。

<a name="安装"></a>
## 安装
从官方网站下载好压缩包，解压到本地文件夹即可。例如将其安装到/usr/local:
```
$tar -C /usr/local -zxf zookeeper-3.4.12.tar.gz
$cd /usr/local/zookeeper-3.4.12/
```

<a name="配置文件"></a>
## 配置文件
zookeeper运行需要conf目录下的zoo.cfg文件，可以在其conf/zoo_sample.cfg的基础上修改配置文件，首先执行
```
$cp conf/zoo_sample.cfg conf/zoo.cfg
```

其中的参数如下：
- tickTime：单位毫秒；用于配置会话注册和控制客户端与zk之间的心跳。客户端的连接超时时间至少是该值的两倍。
- dataDir:这是存储ZooKeeper的内存状态的位置；包括数据库快照和更新数据库的事务日志。zk的安装并不会自动创建该目录，需要用户手动创建并赋予写权限。
- clientPort：zk监听客户端请求端口。可以设置为任何值，默认为2181.

<a name="启动"></a>
## 启动
运行zookeeper前请准备好Java运行环境。

在*bin*目录下运行*zkServer.sh start*即可启动zk服务。如果想要在系统任意目录启动zk，则需将zk的*bin*目录添加到系统环境变量之中。

<a name="启动客户端"></a>
## 启动客户端
zookeeper发行包中自带了一个客户端程序，只需在zk的*bin*目录运行
```
$./zkCli.sh -server localhost:2181
```

<a name="设置zk集群"></a>
## 设置zk集群
单点模式只使用于学习和探索，在实际应用中，ZooKeeper常常部署为重复模式。推荐的最小节点数为3，生产环境中最常见为部署5个节点。

同一个应用程序域中的复制服务器组称为集群。在该模式下，zk服务运行在多个独立主机中，所有集群中的服务都含有完全相同的配置文件。一个集群中，zk实体以领导者和跟随者组织。如果领导者失效，那么会自动从跟随者中选举出新的领导者。

集群配置如下：
```
tickTime=2000
dataDir=/var/lib/zookeeper
clientPort=2181
initLimit=5
syncLimit=2
server.1=zoo1:2888:3888
server.2=zoo2:2888:3888
server.3=zoo3:2888:3888
```
- initLimit:指定了跟随者向领导者建立连接的超时时间，单位为tickTime。
- syncLimit：指定了跟随者与领导者同步的超时时间，单位为tickTime。

server.id=host:port:port是集群中的服务器列表。id用于标识对应的主机。如上例中主机zoo1就使用1来标识。

这个标识数字被记录在数据目录的myid文件中，该文件只包含一行，记录对应的id值。集群中的ZooKeeper服务器都应分配唯一的id，取值范围为[1, 255].

对于host后的两个端口号：
- 第一个端口，2888，主要用于集群中节点与节点间的通信，例如跟随者连接领导者时，跟随者使用TCP连接领导者的该端口。
- 第二个端口，3888，用于选举。所有通信均使用TCP，第二个端口被设计为响应集群中的选举请求。

集群中所有节点共用相同的配置文件，然后分别启动各个节点即可启动整个集群。通过```bin/zkServer.sh status```可以查看节点状态。

<a name="ZooKeeper的内部机制"></a>
# ZooKeeper的内部机制
下图展示了zookeeper服务：
![](/image/zookeeper/zkservice.jpg)

从上图中可以看到zk服务以一个重复的集合运行着。客户端可以连接该集合中任意一个成员来使用zk服务。

<a name="zookeeper数据模型"></a>
## zookeeper数据模型
zookeeper通过在一个分级的命名空间中注册数据来实现协调合作。这个命名空间十分类似Unix文件系统。数据注册在zookeeper中称为znode。下图即为多个znode的实例图：
![](/image/zookeeper/znodes.png)

从上图可以看出，znode被组织为层次结构，呈树形，非常类似标准文件系统。上图中：
- 根节点有一个子节点/zoo，而其有具有三个子节点。
- zk树中每一个节点由其路径标识，路径由/分割。
- 节点被称为数据注册器是因为它们可以保存数据。由此，一个znode可以包含子节点和关联的数据。非常类似于文件系统中文件夹既可以拥有子文件夹，也可以在其中保存文件。

保存在znode中的数据通常是字节形式，其最大容量不超过1MB。znode的路径只能使用绝对路径，相对路径和引用无法被zookeepr识别。znode的路劲可以包含Unicode字符，可以任意命名，其中例外是，ZooKeeper被作为保留字无法使用，“.”在路径中也是非法字符。

<a name="znode类型"></a>
## znode类型
zookeeper具有两种类型的znode：持久节点和临时节点。znode的类型信息需要在创建节点时设定。

<a name="持久节点"></a>
### 持久节点
如名字所述，持久节点只在显式的删除操作后才会被移除。但并不是创建该节点的用户才有删除节点的权利。任何对节点有适当权限的用户都可以删除节点。

使用zk自带的zkCli.sh创建持久节点如下例所示：
```
[zk: localhost:2181(CONNECTED) 1] create /pNode "ApacheZooKeeper"
Created /pNode
```
持久节点对于保存数据非常有用，可以保证数据的高可靠性和稳定性。例如用于保存配置信息。即使创建节点的客户端挂掉，节点和节点中的数据也不会丢失。

<a name="临时节点"></a>
### 临时节点
与持久节点不同，临时节点在其创建者会话结束时，被zk服务自动删除。会话结束的原因可能是意外的断连，或者显式的结束连接。虽然临时节点绑定到一个客户端会话，但是其仍然对所有客户端可见，其规则仍然遵循访问控制策略（ACL）。

临时节点也可以被有权限的用户显式的删除。临时节点在其创建者会话结束时消失，因此zk不允许临时节点有子节点。

可用如下命名创建临时节点：
```
[zk: localhost:2181(CONNECTED) 6] create -e /eNode "helo"    
Created /eNode
```
使用命令选项-e，指定创建临时节点。

临时节点可用于分布式系统中组件之间确认彼此的状态。例如，分布式群组服务就可以使用临时节点实现。临时节点在其创建者会话断开时被删除的特性，可以用于判断节点加入或离开集群。

<a name="序列化节点"></a>
### 序列化节点
序列化节点是在以上两种节点的基础上生成的，持久节点和临时节点都可以被序列化，被序列化的节点在创建时自动在节点名称后添加一个10位数的序号，其创建过程如下：
```
[zk: localhost:2181(CONNECTED) 1] create -s /sNode "hi"
Created /sNode0000000004
```

<a name="zookeeper watches"></a>
## zookeeper watches
客户端可以通过向zk注册来获取特定事件发生的通知。需要注意的是，一个Watch是一次性操作，只会被激发一次。所以如果要持续的监控某个事件，就需要客户单端在每次收到事件通知时注册新的watch。

watch可以被以下三种情况触发：
1. znode上的数据发生变化，如使用SetData操作向节点中写入新的数据。
2. 节点的子节点发生变化，如使用delete操作删除子节点。
3. 节点本身被创建或者被删除。

对于zk的watch，具有以下约束：
- zk保证watch以先入先出的顺序被触发，并且通知也总是按顺序被分发。
- watch的通知会在节点发生任何其他修改前被送至客户端。
- watch事件的顺序是以zk发现的更新操作顺序。

由于zk的watch只被触发一次，并且在获取watch事件与重置watch之间存在间隔，所以在重置watch的间隔里，客户存在丢失事件的可能性。

<a name="zokeeper操作"></a>
## zookeeper操作
zk支持以下九种基本操作：
- create：以给定路径创建一个新的节点。
- delete：删除指定路径的节点。
- exists：检查节点是否存在。
- getChildren：获取节点的子节点列表。
- getData：获取节点绑定的数据。
- setData：向节点写入数据。
- getACL：获取节点的访问控制信息。
- setACL：设置节点的访问控制信息。
- sync：同步客户端对节点的视图。

zk不允许对节点数据进行局部读写。因此对节点数据的读写操作都是针对整个数据内容进行。

zk进行读写操作如下图：
![](/image/zookeeper/rw.png)
其中两个重要的部分：
- 读操作：读操作由客户端连接的服务器直接应答。
- 写操作：写操作被服务器传递到领导者节点，完成同步过程后响应给客户端。

对节点的读操作，如exists，getChildren和getData，允许执行时同时设置watch。另一方面，watch可由写操作触发，如create，delete和setData。

以下是一些可能触发watch事件的节点变化：
- NodeChildrenChanged：一个节点的子节点被创建或删除。
- NodeCreated：一个节点被创建到ZooKeeper中。
- NodeDataChanged：节点相关的数据被更新。
- NodeDeleted：一个节点从ZooKeeper中删除。

<a name="zookeeper访问控制列表"></a>
## zookeeper访问控制列表
zk提供一下内置的权限访问：
- World：表示任何连接到zk服务的客户端。
- Auth：表示任何授权用户，但是没有使用任何ID。
- Digest：表示通过用户名和密码的方式授权。
- IP address：表示通过IP地址进行授权。

节点关联的ACL信息并不会传播给其子节点。

zookeeper ACL支持以下权限控制：
- CREATE：为节点创建子节点。
- READ：读取节点数据和其子节点列表。
- WRITE：向节点写入数据。
- DELETE：删除子节点。
- ADMIN：设置ACL。

任何连接到zk服务的客户端都可以检测节点是否存在，该操作不受权限管理约束。

<a name="zookeeper状态信息"></a>
## zookeeper状态信息
zk中每个节点都有自己的状态信息，包含以下内容：
- cZxid：创建节点的事务ID。
- mZxid：最后一次修改节点的事务ID。
- pZxid：节点添加或移除子节点的事务ID。
- ctime：创建节点的时间。
- mtime：最后一次修改节点的时间。
- dataVersion：节点数据被修改的次数
- cversion：子节点被修改（创建或删除）的次数。
- aclVersion：节点ACL被修改的次数。
- ephemeralOwner：如果节点是临时节点，该项为临时节点所有者的会话ID。如果节点非临时节点，该值为零。
- dataLength：节点数据长度。
- numChildren：子节点个数。

<a name="会话"></a>
## 会话
客户端通过一个服务器列表连接zk服务。客户端会依次尝试与列表中的服务器连接，直到连接成功或所有连接失败。

一旦连接成功，一个会话就在客户端和zk服务间建立起来，其以一个64位的数标识，被发送给客户端。会话在对zk进行操作中非常重要，其与客户端对zk的每一次操作紧密相关。

会话在zk中扮演十分重要的角色，如临时节点的概念就基于客户端和zk服务之间的会话。临时节点具有与客户端和zk服务会话同样的生命周期。当会话结束，临时节点即被zk服务自动删除。

会话可以设置超时时间，其由客户端设置，连接zk服务时上传至zk服务。会话的超时由zk集群处理。目前超时时间要求最小两个tickTime，最大20个tickTime。

会话的保持由客户端发送ping请求，即心跳到zk服务。客户端与zk服务之间的会话使用TCP连接。心跳间隔应该设置较短，这样当连接异常时，客户端可以尝试恢复连接，或尝试连接zk集群中其他节点，只要恢复连接的时间没有超过会话超时时间，会话仍然有效，其关联的临时节点也任然有效。

连接状态变化如下：
![](/image/zookeeper/connect_status.png)

<a name="zookeeper编程"></a>
# zookeeper编程
以下给出几个使用Java库连接zk服务的用例，以下是例子中使用的依赖：
```
<dependency>
	<groupId>org.apache.zookeeper</groupId>
	<artifactId>zookeeper</artifactId>
	<version>3.4.10</version>
</dependency>
```

<a name="连接zk服务"></a>
## 连接zk服务
```
import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.ZooKeeper;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class HelloZooKeeper {
    public static void main(String[] args) throws IOException {
        String hostPort = "localhost:2181";
        String zpath = "/";
        List<String> zooChildren = new ArrayList<String>();
        ZooKeeper zk = new ZooKeeper(hostPort, 2000, null);
        if (zk != null) {
            try {
                zooChildren = zk.getChildren(zpath, false);
                System.out.println("Znodes of '/': ");
                for(String child: zooChildren){
                    System.out.println(child);
                }
            } catch (KeeperException e) {
                e.printStackTrace();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
```
上例中，我们建立了一个与zk服务的连接，并获取其根节点'/'的子节点列表。

<a name="实现watch"></a>
## 实现watch
实现一个watch，在节点数据发生变化时，让zk服务通知客户端。以下例子中，将实现两个类：DataWatcher和DataUpdater。其中DataWatcher等待zk服务推送NodeDataChange事件。DataUpdater周期性的更新节点数据。

以下为DataWatcher.java内容：
```
package watcher;

import org.apache.zookeeper.*;

import java.io.IOException;

public class DataWatcher implements Watcher, Runnable {
    private static String hostPort = "localhost:2181";
    private static String zooDataPath = "/myData";
    byte[] zooData = null;
    ZooKeeper zk;

    public DataWatcher() {
        try {
            zk = new ZooKeeper(hostPort, 2000, this);
            if (zk != null) {
                try {
                    if (zk.exists(zooDataPath, this) == null) {
                        zk.create(zooDataPath, "".getBytes(),
                                ZooDefs.Ids.OPEN_ACL_UNSAFE,
                                CreateMode.PERSISTENT);
                    }
                } catch (KeeperException | InterruptedException e) {
                    e.printStackTrace();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args)
            throws InterruptedException, KeeperException {
        DataWatcher dataWatcher = new DataWatcher();
        dataWatcher.printData();
        dataWatcher.run();

    }

    public void printData() throws InterruptedException, KeeperException {
        zooData = zk.getData(zooDataPath, this, null);
        String zString = new String(zooData);
        System.out.printf("\nCurrent Data @ ZK Path %s: %s", zooDataPath, zString);
    }

    @Override
    public void run() {
        try {
            synchronized (this) {
                while (true) {
                    wait();
                }
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
            Thread.currentThread().interrupt();
        }
    }

    @Override
    public void process(WatchedEvent watchedEvent) {
        System.out.printf("\nEvent Received: %s", watchedEvent.toString());
        if (watchedEvent.getType() == Event.EventType.NodeDataChanged) {
            try {
                printData();
            } catch (KeeperException | InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}

```
在DataWatcher构造函数中，我们检测节点是否存在，如果不存在则创建节点。

当收到事件通知后，调用printData获取节点数据，注意，在printData中，调用getData时，我们通过设置getData的第二个参数重置了watch。因为每个watch只触发一次，在处理通知时再次注册watch，以保证对事件的持续监听。

以下是DataUpdater.java的内容：
```
package watcher;

import org.apache.zookeeper.KeeperException;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;

import java.io.IOException;
import java.util.UUID;

public class DataUpdater implements Watcher {
    private static String hostPort = "localhost:2181";
    private static String zooDataPath = "/myData";
    ZooKeeper zk;

    public DataUpdater() {
        try {
            zk = new ZooKeeper(hostPort, 2000, this);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args)
            throws InterruptedException, KeeperException {
        DataUpdater dataUpdater = new DataUpdater();
        dataUpdater.run();
    }

    public void run() throws InterruptedException, KeeperException {
        while (true) {
            String uuid = UUID.randomUUID().toString();
            byte[] zooData = uuid.getBytes();
            zk.setData(zooDataPath, zooData, -1);
            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    @Override
    public void process(WatchedEvent watchedEvent) {
        System.out.println("Event Received: " + watchedEvent.toString());
    }
}
```

DataUpdater每5秒钟更新一次节点数据，此处DataUpdater实现Watcher接口，演示了每个watch只会被触发一次。在构造函数中，通过设置ZooKeeper的第三个参数注册了watch，所以在程序启动后，我们会收到一次zk服务的通知，但是由于在process中我们没有再次注册watch，因此，其后不再收到zk服务通知。

<a name="成员管理"></a>
## 成员管理
下面的例子，将创建一个成员管理应用，包含ClusterMonitor和ClusterClient。其中ClusterMonitor用于使用zk监控集群成员的加入和离去。ClusterClient用于模拟集群成员。这里的监控利用了zk服务临时节点的特性，代码如下：
```
package membership;

import org.apache.zookeeper.*;

import java.io.IOException;
import java.util.List;

public class ClusterMonitor implements Runnable {
    private static String membershipRoot = "/members";
    private final Watcher connectionWatcher;
    private final Watcher childrenWatcher;
    boolean alive = true;
    private ZooKeeper zk;

    public ClusterMonitor(String hostPort) throws
            IOException, InterruptedException, KeeperException {
        connectionWatcher = new Watcher() {
            @Override
            public void process(WatchedEvent watchedEvent) {
                if (watchedEvent.getType() == Watcher.Event.EventType.None &&
                        watchedEvent.getState() == Event.KeeperState.SyncConnected) {
                    System.out.println("Event Received: " + watchedEvent.toString());
                }
            }
        };

        childrenWatcher = new Watcher() {
            @Override
            public void process(WatchedEvent watchedEvent) {
                System.out.println("Event Received: " + watchedEvent.toString());
                if (watchedEvent.getType() == Event.EventType.NodeChildrenChanged) {
                    try {
                        List<String> children = zk.getChildren(membershipRoot, this);
                        System.out.println("!!!Cluster Membership Change!!!");
                        System.out.println("Members: " + children);
                    } catch (KeeperException e) {
                        throw new RuntimeException(e);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        alive = false;
                        throw new RuntimeException(e);
                    }
                }
            }
        };

        zk = new ZooKeeper(hostPort, 2000, connectionWatcher);

        if (zk.exists(membershipRoot, false) == null) {
            zk.create(membershipRoot, "ClusterMonitorRoot".getBytes(),
                    ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
        }

        List<String> children = zk.getChildren(membershipRoot, childrenWatcher);
        System.out.println("members: " + children);
    }

    public synchronized void close() {
        try {
            zk.close();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void run() {
        try {
            synchronized (this) {
                while (alive) {
                    wait();
                }
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
            Thread.currentThread().interrupt();
        } finally {
            this.close();
        }
    }

    public static void main(String[] args) throws
            IOException, InterruptedException, KeeperException {
        String hostPort = "localhost:2181";
        new ClusterMonitor(hostPort).run();
    }
}
```

以下是ClusterClient.java的代码：
```
package membership;

import org.apache.zookeeper.*;

import java.io.IOException;
import java.lang.management.ManagementFactory;

public class ClusterClient implements Watcher, Runnable {
    private static String membershipRoot = "/members";
    ZooKeeper zk;

    public ClusterClient(String hostPort, Long pid) {
        String processId = pid.toString();
        try {
            zk = new ZooKeeper(hostPort, 2000, this);
        } catch (IOException e) {
            e.printStackTrace();
        }
        if (zk != null) {
            try {
                zk.create(membershipRoot + "/" + processId,
                        processId.getBytes(), ZooDefs.Ids.OPEN_ACL_UNSAFE,
                        CreateMode.EPHEMERAL);
            } catch (KeeperException | InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public synchronized void close() {
        try {
            zk.close();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void run() {
        try {
            synchronized (this) {
                while (true) {
                    wait();
                }
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
            Thread.currentThread().interrupt();
        } finally {
            this.close();
        }
    }

    @Override
    public void process(WatchedEvent watchedEvent) {
        System.out.println("Event Received: " + watchedEvent.toString());
    }

    public static void main(String[] args) {
        String hostPort = "localhost:2181";
        String name = ManagementFactory.getRuntimeMXBean().getName();
        int index = name.indexOf('@');
        Long processId = Long.parseLong(name.substring(0, index));
        new ClusterClient(hostPort, processId).run();
    }
}
```

<a name="常见分布式问题的zookeeper方案"></a>
# 常见分布式问题的zookeeper方案
<a name="屏障"></a>
## 屏障
屏障是用于分布式应用多节点同步的一种方法。系统中多个节点被阻塞直到相应条件达成。

屏障的zk实现如下：
1. 程序开始时，一个znode指定为负责管理屏障的节点，为方便叙述，将该节点命名为/zk_barrier.
2. 当屏障节点存在时，认为屏障处于激活状态。
3. 系统中每个客户端对节点/zk_barrier调用exists()方法，并注册watch事件。
4. 如果exists()返回false，则表示屏障已经消失，因此客户端可以继续其后的运算。
5. 如果exists()返回true，客户端则等待watch事件被触发。
6. 当屏障条件被达成时，负责管理屏障的客户端负责删除/zk_barrier。
7. 删除动作会触发watch事件，所有调用exists()注册了事件的客户端都会得到通知，客户端再次调用exists().
8. 步骤7返回true，客户端继续其后的运算。

<a name="队列"></a>
## 队列
通过zk提供的序列化节点可以轻松的实现分布式生产者-消费者队列。
1. 创建一个znode用于保存队列，为便于叙述，命名为/queue。
2. 生产者通过调用create时指定模式为EPHEMERAL_SEQUENTIAL在/queue下创建节点命名为“queue-”的节点，zk会自动在为创建的节点名后添加序列号。
3. 消费者通过调用getChildren方法，获取到/queue下的所有子节点，通过排序即可获取序列号最小的节点，取出节点数据，处理，并删除该节点。

<a name="锁"></a>
## 锁
使用zk实现锁的过程如下：
1. 创建保持锁信息的父节点/locknode.
2. 调用create(“/locknode/lock-”, CreateMode.EPHEMERAL_SEQUENTIAL).
3. 调用getChildren("/locknode/lock-", false).
4. 如果客户端在步骤2中创建的节点具有最小的序列号，则该客户端获得锁，退出算法。
5. 调用exists("/locknode/<最小序列号的znode名称>"， True)。
6. 如果exists返回false。则回到步骤3.
7. 如果exists返回true，等待步骤5中注册的watch事件被触发。

其释放锁的过程如下：
1. 拥有锁的客户端删除对应的节点，触发下一个客户端去获取锁。
2. 节点列表中，下一个序列号的客户端会被通知并取得锁。

<a name="选举"></a>
## 选举
1. 创建选举信息父节点"/election".
2. 以SEQUENCE和EPHEMERAL标志在"/election"下创建节点。为便于叙述，假设创建节点时，zk分配的序列号为N。
3. 调用getChildren("/election", false)获取当前所有主节点的候选节点。
4. 在当前节点列表中，序号仅次于N的节点上设置watch，exists("/election/<序列号仅小于N的节点>"， true)。
5. 当收到步骤4中设置的watch事件时，执行getChildren("/election", false)获取所有参与选举的节点。
6. 节点列表中序列号最小的节点当选为新的主节点。
7. 修改节点的watch为，序列号仅仅小于自身节点序列号的节点。

<a name="组成员服务"></a>
## 组成员服务
该服务的zk实现，已在上面的实例中说明，不再赘叙。
