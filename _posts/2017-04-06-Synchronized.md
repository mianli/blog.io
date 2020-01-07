

# Synchronized

- synchronized方法      
每个实例对应一把锁，每个synchronized方法必须获得调用该方法的类实例的锁才能执行，否则所属线程阻塞，方法一旦执行，就独占该锁，直到从该方法返回时才将锁释放。此后被阻塞的线程方能获得锁，重新进入可执行状态。这种机制确保了同一时刻对每一个类实例，其所有声明的synchronized的成员函数至多只有一个处于可执行状态。不光是类实例，每一个类也对应一把锁，这样我们也可以将静态成员函数声明为synchronized，以控制其对类的静态成员变量的访问。      
- sychronized方法的缺陷       
它锁定的是调用这个同步方法的对象。也就是说，当一个对象P1在不同的线程中执行同一个同步方法的时候，他们之间是互斥的。但是这个对象所属的class创建了另一个对象P2,却可以任意调用这个同步方法。同步方法的实质是将synchronized作用于object reference。P1和P2之间的锁毫不相干，程序在这种情况下将摆脱同步机制的控制。另外如果将一个大的方法声明为synchronized将会大大影响效率。

- synchronized(this) {/code/}       
表示获取到了该类对象的锁，它的作用域是当前的对象。
-synchronized(T.class) {/code/}     
得到该类的锁，作用域是类
-当没有明确的对象作为锁时，只是想让一段代码同步，可以创建一个特殊的instance变量来充当锁。            
```
private byte[] lock = new byte[0];
public void method() {
    sychronized(lock) {
        //code 
    }
}
```
> 注：0长度的byte数组对象创建起来比任何对象都经济——查看编译后的字节码：生成量长度的byte[]对象只需要3条操作码，而Object lock = new Object()则需要7条操作码。

- sychronized静态方法
```
Class Foo {
  // 同步的static 函数
  public synchronized static void methodAAA()  {
  //….
  }
  public void methodBBB() {
       synchronized(Foo.class)   // class literal(类名称字面常量)
  }    
}
```
两个同步方法功能相似，都是把类作为锁的情况，而不是具体对象了。