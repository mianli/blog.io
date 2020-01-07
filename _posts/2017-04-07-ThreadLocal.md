



# ThreadLocal

ThreadLocal 的作用是提供**线程内**的局部变量，这种变量在线程的生命周期内起作用。一般被称为“**线程本地变量**”，它是一种特殊的线程绑定机制，将变量和线程绑定在一起，为每一个线程维护独立的内存副本。      

```
ThreadLocal<List<String>> threadLocal = new ThreadLocal<List<String>>() {
		@Override
		protected List<String> initialValue() {
		//设置初始值    
			return null;
		}
	};
new Thread() {
	public void run() {
		List<String> list = new ArrayList<>();
		list.add("中国");
		list.add("美国");
		list.add("俄罗斯");
		threadLocal.set(list);
		
		for(String string : threadLocal.get()) {
			System.out.println("Thread1:" + string);
		}
	};
}.start();

new Thread() {
	public void run() {
		List<String> list = new ArrayList<>();
		list.add("北京");
		list.add("上海");
		list.add("深圳");
		threadLocal.set(list);
		
		for(String string : threadLocal.get()) {
			System.out.println("Thread2:" + string);
		}
	};
}.start();
```

运行结果：  
![](http://www.z4a.net/images/2018/03/10/WX20180310-0015392x.png)

可见第一个线程set的结果和第二个线程set的结果各自独立，并不会相互作用
