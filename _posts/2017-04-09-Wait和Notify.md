

# Wait/Notify

wait()和notify()都必须在对象的同步代码中才能被调用，即只能在同步方法或者代码块中被调用。  
- wait()    
1. wait()方法的作用是使当前执行代码的进程进行等待，在wait()被调用的地方停止执行，==该方法会将该线程放入“预执行队列”中==，直到接收到通知或者中断为止
2. 在调用wait()之前，线程必须获得该对象级别的锁，如上所述，只能在同步方法或者同步代码块中被调用    
3. **wait()是释放锁的**，即在执行到wait()方法的时候，因为当前线程被放到“预执行队列”中，所以**当前线程会释放锁**，wait()方法返回前，线程与其他线程竞争重新获取锁  
- notify/notifyAll  
1. 和wait()一样，notify也必须在同步方法或者同步代码块中才能被调用，即线程也必须获得对象级别的锁
2. 执行notify之后，当前线程不会立即释放锁，而是执行完之后才会释放该对象锁，被通知的线程也不会立即获得锁，而是等待notify执行完之后，释放了对象锁，才可以获得对象锁
3. notifyAll通知所有等待同一共享资源的全部线程从等待状态中退出，进入可运行状态，重新竞争对象锁
> wait()/notify()要集合**synchronized**关键字一起使用，因为他们都需要获取对象的锁。**wait()是释放锁，notify不释放锁**。  

```JAVA
byte[] lock = new byte[0];
List<Integer> list = new ArrayList<>();
new Thread() {
	public void run() {
		System.out.println("线程B开始执行");
		synchronized (lock) {
			if(list.size() != 5) {
				try {
					System.out.println("等待通知");
					lock.wait();
					System.out.println("阻塞停止");	
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
		}
		System.out.println("线程B执行结束");
	};
}.start();
new Thread() {
	public void run() {
		synchronized (lock) {
			for(int i = 0; i < 10; i++) {
					list.add(i);
					System.out.println(list.size());
					if(i== 4) {
						System.out.println("A发出通知");
						lock.notify();
					}
				}
		}
		
	};
}.start();
```
运行结果：  
```
线程B开始执行
等待通知
1
2
3
4
5
A发出通知
6
7
8
9
10
阻塞停止
线程B执行结束
```
实例2：
```
static Object lock = new Object();
static class Thread1 extends Thread{
	
	@Override
	public void run() {
		super.run();
		synchronized (lock) {
			System.out.println("开始执行");
			try {
				lock.wait();
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	
}
public static void main(String[] args) {
		Thread1 thread = new Thread1();
		Thread1 thread2 = new Thread1();
		thread.start();
		thread2.start();
	}
```
运行结果可以发现wait是释放锁的：
```
开始执行
开始执行
```
实例3：
为什么用while？
```
class Buf {
    private final int MAX = 5;
    private final ArrayList<Integer> list = new ArrayList<>();
    
    synchronized void put(int v) throws InterruptedException {
    
	//为什么用while？
        while (list.size() == MAX) {
            wait();
        }
        list.add(v);
        notifyAll();
    }
 
    synchronized int get() throws InterruptedException {
        // line 0 
        if (list.size() == 0) { 
            wait();
        }
        int v = list.remove(0); 
        notifyAll();
        return v;
    }
 
    synchronized int size() {
        return list.size();
    }
}
```
这里模拟了一个队列，可以使用put()向list中存放数据，数据最多只能有5个。get()用来每次获取list中的一个数据，获取后会将它从list中移除。注意put中wait()的地方用的是while而不是if。这里不能用if吗？当然不能！   
假如使用if做判断是否进行等待，设想如果多个线程在调用put，并同时在wait的地方进行等待，当达到上限的时候必然会有多个put等待向list中插入数据。如果这个时候get被调用了，get会发出通知让put继续运行，假如有一个线程中的put获取到了锁，当put运行到notifyAll的时候，它又发出了一个notifyAll的通知！！！那么可能此时get的线程没有获取到锁，而put的另一个线程竞争到了锁，结果当然是执行put中wait之后的代码了，对，就是又进行了插入。结果必然是超过了list最大为5的限制。所以用while就不会有这种bug，因为假如是上一种情况发生的时候，它会再次进行判断。        
> 可以发现，如果是wait和notify在同一个执行流程中的时候（比如实例3，他们在同一个方法当中，有可能通知发出后被另一个正在执行put的线程竞争到了锁），最好用while。否则，一般用if也就够了。