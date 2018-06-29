- [Java中使用MySql](#Java中使用MySql)
    - [模型](#模型)
    - [执行过程](#执行过程)
    - [示例](#示例)
    - [理解ResultSet](#理解ResultSet)
    - [元数据](#元数据)
        - [DatabaseMetaData](#DatabaseMetaData)
        - [ResultSetMetaData](#ResultSetMetaData)
    - [连接池](#连接池)
        - [什么是连接池](#什么是连接池)
        - [示例代码](#示例代码)

<a name="Java中使用MySql"></a>
# Java中使用MySql

<a name="模型"></a>
## 模型
![](/image/db/model.png),Java中对数据库编程使用三层模型，通过在Java应用与数据库驱动程序间添加隔离层jdbc,到达解耦，使得切换数据库时，应用代码受到的影响降到最低。

<a name="执行过程"></a>
## 执行过程
java.sql包中包含了大量与数据库操作有关的类，其中DriverManager用于关于数据库驱动，只需将驱动放置在classpath中，DriverManager即可自动加载，通过这种方式，应用层不需要显示的声明使用的具体驱动类，从而替换数据库时，应用层代码不会受到影响。
通过DriverManager生成Connection对象，改对象用于连接数据库。Connection对象生成Statement对象，用于执行具体的SQL语句，其流程图如下：
![](/image/db/executepath.png)

<a name="示例"></a>
## 示例
```
import java.sql.*;

public class DataBasePlay {
    Connection connection;

    public DataBasePlay(){
        try{
            Class.forName("com.mysql.jdbc.Driver").newInstance();
        }catch (Exception e){
            System.out.println("Unable to find and load driver: " + e);
            System.exit(1);
        }
    }

    public void connectDB(){
        try{
            connection = DriverManager.getConnection(
                    "jdbc:mysql://hostname:port/dbname?user=User&password=Pwd"
            );
        }catch(SQLException e){
            System.out.println(e);
        }
    }

    public void executeSQL(){
        try{
            Statement statement = connection.createStatement();
            ResultSet rs = statement.executeQuery("select * from table");
            while(rs.next()){
                System.out.println(rs.getString(1));
            }

            rs.close();
            statement.close();
            connection.close();
        }catch(SQLException e){
            System.out.println(e);
        }
    }

    public static void main(String[] args){
        DataBasePlay dbc = new DataBasePlay();
        dbc.connectDB();
        dbc.executeSQL();
    }
}
```
上例中，在构造函数中，检查classpath中是否有mysql的驱动类*com.mysql.jdbc.Driver*，*connectDB*创建与数据库之间的连接。*executeSQL*通过Statement类来执行SQL语句。

<a name="理解ResultSet"></a>
## 理解ResultSet
*ResultSet*类用于存储执行SQL的返回结果，可以将其理解为一个二维数据，如下图：
![](/image/db/resultset.png)
值得注意的是，在返回结果中，首行、首列的下标均为1，下标0，位于首行、列之前的位置。可以通过*ResultSet*提供的API方便的移动游标位置，并获取其中相应的数据。

<a name="元数据"></a>
## 元数据
不仅数据库总存储的数据非常重要，有时应用也关心数据库本身的状态信息。

<a name="DatabaseMetaData"></a>
### DatabaseMetaData
使用DatabaseMetaData类可获得数据库元数据，其主要包含以下五个方面：
- 通用信息。数据库通用信息，并不涉及具体的数据库或表，如连接数据的URL，当前连接用户名等。
- 特性支持情况。可查看是否支持感兴趣的特性，如是否支持块更新等。
- 数据源限制信息。如表中可定义最大行数，每行可容纳最大字节数等。
- SQL对象信息。如表的类型信息等。
- 事务支持

以下给出示例代码：
```
import java.sql.*;

public class DataBasePlay {
    Connection connection;

    public DataBasePlay() {
        try {
            Class.forName("com.mysql.jdbc.Driver").newInstance();
        } catch (Exception e) {
            System.out.println("Unable to find and load driver: " + e);
            System.exit(1);
        }
    }

    public static void main(String[] args) {
        DataBasePlay dbc = new DataBasePlay();
        dbc.connectToDB();
        dbc.getMetaData();
    }

    public void connectToDB() {
        try {
            connection = DriverManager.getConnection(
                    "jdbc:mysql://hostname:port/dbname?user=User&password=Pwd"
            );
        } catch (SQLException e) {
            System.out.println(e);
        }
    }

    public void getMetaData() {
        try {
            DatabaseMetaData md = connection.getMetaData();
            System.out.println("getURL: " + md.getURL());
            System.out.println("getDatabaseProductVersion: " + md.getDatabaseProductVersion());
            System.out.println("getDriverMajorVersion: " + md.getDriverMajorVersion());
            System.out.println("getDriverMinorVersion: " + md.getDriverMinorVersion());
            System.out.println("nullsAreSortedHigh: " + md.nullsAreSortedHigh());
            System.out.println("getMaxRowSize: " + md.getMaxRowSize());
            System.out.println("getMaxStatementLength: " + md.getMaxStatementLength());
            System.out.println("getMaxTablesInSelect: " + md.getMaxTablesInSelect());
            System.out.println("getMaxConnections: " + md.getMaxConnections());
            System.out.println("getMaxCharLiteralLength: " + md.getMaxCharLiteralLength());
            System.out.println("getDefaultTransactionIsolation: " + md.getDefaultTransactionIsolation());
            System.out.println("dataDefinitionIgnoredInTransactions: " + md.dataDefinitionIgnoredInTransactions());
        } catch (SQLException e) {
            System.out.println(e);
        }
    }
}
```
上例中只列出了*DatabaseMetaData*部分可用接口，详细说明可查阅其API文档。

<a name="ResultSetMetaData"></a>
### ResultSetMetaData
从*DatabaseMetaData*类中获得了关于数据库比较恒定的元数据，同样也可以使用*ResultSetMetaData*来获取每次查询的元数据。
以下为获取列名的示例代码：
```
import java.sql.*;

public class DataBasePlay {
    Connection connection;

    public DataBasePlay() {
        try {
            Class.forName("com.mysql.jdbc.Driver").newInstance();
        } catch (Exception e) {
            System.out.println("Unable to find and load driver: " + e);
            System.exit(1);
        }
    }

    public static void main(String[] args) {
        DataBasePlay dbc = new DataBasePlay();
        dbc.connectToDB();
        dbc.getResultSetMetaData();
    }

    public void connectToDB() {
        try {
            connection = DriverManager.getConnection(
                    "jdbc:mysql://hostname:port/dbname?user=User&password=Pwd"
            );
        } catch (SQLException e) {
            System.out.println(e);
        }
    }

    public void getResultSetMetaData() {
        try {
            Statement statement = connection.createStatement();
            ResultSet rs = statement.executeQuery("select * from table");
            ResultSetMetaData md = rs.getMetaData();

            while (rs.next()) {
                for(int i=1; i<=md.getColumnCount(); i++){
                    System.out.println(md.getColumnName(i) + ": " + rs.getString(i));
                }
            }

            rs.close();
            statement.close();
            connection.close();
        } catch (SQLException e) {
            System.out.println(e);
        }
    }
}
```

<a name="连接池"></a>
## 连接池
使用数据库时，可以为每次查询新建连接，查询结束后关闭连接，其缺点是比较浪费时间和资源。
而在应用启动时建立连接，结束时才关闭连接的方法无法应对多客户端使用数据库的情景。
为解决以上问题，可以使用连接池，其自动管理对数据库连接的打开、关闭、重用等。

<a name="什么是连接池"></a>
### 什么是连接池
连接池是一组数据库连接的缓存。连接池根据需要自动创建与数据库的连接，并提供给一个或多个应用共同使用，其原理如下图：
![](/image/db/connect_pool.png)

<a name="示例代码"></a>
### 示例代码
```
import com.mchange.v2.c3p0.ComboPooledDataSource;

import java.beans.PropertyVetoException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class MysqlConnectPool {
    private static ComboPooledDataSource comboPool;

    static {
        try {
            try {
                Class.forName("com.mysql.jdbc.Driver");
            } catch (ClassNotFoundException e) {
                System.out.println(e.getMessage());
            }

            comboPool = new ComboPooledDataSource();
            comboPool.setDriverClass("com.mysql.jdbc.Driver");
            comboPool.setJdbcUrl("jdbc:mysql://hostname:port/dbname");
            comboPool.setUser("User");
            comboPool.setPassword("Pwd");
            comboPool.setMaxPoolSize(2);
            comboPool.setMinPoolSize(1);
        } catch (PropertyVetoException e) {
            System.out.println(e.getMessage());
        }
    }

    private MysqlConnectPool() {
    }

    public synchronized static Connection getConnection() throws SQLException {
        return comboPool.getConnection();
    }

    public static void main(String[] args) {
        try {
            Connection connection = MysqlConnectPool.getConnection();
            Statement statement = connection.createStatement();

            ResultSet rs = statement.executeQuery("select * from table");
            while (rs.next()) {
                System.out.println(rs.getString(1));
            }

            rs.close();
            statement.close();
            connection.close();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }
}
```
