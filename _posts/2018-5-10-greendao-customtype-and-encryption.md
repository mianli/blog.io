## 自定义类型

自定义类型允许数据类拥有任何类型的属性。greenDao默认支持一下类型：

```
boolean, Boolean
int, Integer
short, Short
long, Long
float, Float
double, Double
byte, Byte
byte[]
String
Date
```

### Convert注解和属性转换

通过使用@Convert注解将自定义属性映射为greenDao支持的类型。同时需要提供一个*PropertyConverter*的实现类。

比如，可以自定义一个Color类来映射为Integer类型，或者将*org.joda.time.DateTime*映射为Long类型。

```
@Entity
public class User {
    @Id
    private Long id;
 
    @Convert(converter = RoleConverter.class, columnType = Integer.class)
    private Role role;
 
    public enum Role {
        DEFAULT(0), AUTHOR(1), ADMIN(2);
        
        final int id;
        
        Role(int id) {
            this.id = id;
        }
    }
 
    public static class RoleConverter implements PropertyConverter<Role, Integer> {
        @Override
        public Role convertToEntityProperty(Integer databaseValue) {
            if (databaseValue == null) {
                return null;
            }
            for (Role role : Role.values()) {
                if (role.id == databaseValue) {
                    return role;
                }
            }
            return Role.DEFAULT;
        }
 
        @Override
        public Integer convertToDatabaseValue(Role entityProperty) {
            return entityProperty == null ? null : entityProperty.id;
        }
    }
}
```

> 注意：如果定义自定义属性在实体类内部，最好使用static关键字来修饰

不要忘记处理null数据的情况，通常如果输入为null返回也为null。

自定义属性在greenDao中并不被识别，但是可以识别greenDao支持的类型。推荐使用基本类型，这样会更容易转换。

为了获得最佳性能，greenDAO将为所有转换使用单个转换器实例。*确保除了无参数的默认构造函数之外，转换器没有任何其他构造函数*。另外，*要确保它是线程安全的*，因为它可以在多个实体上并发调用。

### 如何正确的转换枚举类型

枚举类型在数据是比较常用的。那么该如何更好的进行存储枚举类型呢？

- 勿将枚举的ordinal或者名字进行存储： 他们都是不稳定的，你可能会轻易改变他们的定义。
- 使用稳定的ids：定义一个稳定的类型，比如string/integer，用它们来存储数据进行映射。
- 定义未知类型：定义一个Unknown。它可以处理空值或未知值。这将允许您在不破坏应用程序的情况下处理旧枚举值被删除的情况。

### 查询时使用自定义类型

QueryBuilder对自定义类型并不识别。你需要使用greenDao支持的基本类型来进行查询。还要注意，在数据库执行的操作总是使用的是基本类型，例如ORDER BY语句。

例如，在构建查询时可以使用属性转换器：

```
RoleConverter converter = new RoleConverter();
List<User> authors = userDao.queryBuilder()
    .where(Properties.Role.eq(converter.convertToDatabaseValue(Role.AUTHOR)))
    .list();
```

## 加密

greenDao支持使用加密来保护敏感数据。Android本身并不提供数据库的加密。因此，如果攻击者获得对数据库文件的访问权(通过获得root权限，例如通过利用安全缺陷或欺骗有root设备的用户)，则攻击者可能获得对该数据库中所有数据的访问权。使用密码保护的加密数据库增加了额外的安全层。它阻止攻击者简单地打开数据库文件。

### 使用自定义SQLite构建

因为Android不支持开箱即用的加密数据库，所以需要在APK中捆绑定制的SQLite构建。这些定制构建由依赖于CPU的本地代码组成。所以APK的大小会增加几个MByte。因此，只有在真正需要加密时才应该使用加密。

greenDAO直接使用绑定支持*SQLCipher*。SQLCipher是一个使用256位AES加密的SQLite的定制版本。

### 数据库初始化

使用DaoMaster提供的OpenHelper的子类来创建数据库实例，比如DevOpenHelper。然后调用.getEncryptedWritableDb(<password>)来代替使用.getWritableDb()。

```
DevOpenHelper helper = new DevOpenHelper(this, "notes-db-encrypted.db");
Database db = helper.getEncryptedWritableDb("<your-secret-password>");
daoSession = new DaoMaster(db).newSession();
```

