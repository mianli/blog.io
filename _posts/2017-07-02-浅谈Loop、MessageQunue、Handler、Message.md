

# 浅谈Loop、MessageQunue、Handler、Message

四者的关系：    
![HandlerLooperMessageQueueThread.png](https://www.z4a.net/images/2018/04/11/HandlerLooperMessageQueueThread.md.png)       
Handler是我们经常用到的一个类，通常用来处理UI事件，关于它的用处是比较重要的一部分。
通过对Thread、Handler、Looper、MessageQueue四者关系图可以看出，Thread是最底层的。Looper、MessageQueue构建在其之上，而Handler又构建在Handler之上。  

## MessageQueue 
每一个线程都维护着一个MessageQueue，它用来存放Message对象，本身可以看做是一个Message的池。线程会依次从其中取出Message，然后进行处理。MessageQueue中有两个比较重要的方法，一个是enqueueMessage、一个是next方法。enqueueMessage用于将一个Message放入到消息队列，next方法则从消息队列中阻塞式的取出一个Message。
## Looper
消息队列只是存储Message，Looper则会让消息队列循环起来进行处理其中的Message。在线程中默认的情况下，是没有消息队列的。为了能够让线程绑定一个MessageQueue，我们需要借助Looper，先调用其prepare方法，然后再调用loop()方法。 
大致看下prepare源码：

```
// sThreadLocal.get() will return null unless you've called prepare().
static final ThreadLocal<Looper> sThreadLocal = new ThreadLocal<Looper>();
...
private Looper(boolean quitAllowed) {
    mQueue = new MessageQueue(quitAllowed);
    mThread = Thread.currentThread();
}
...
public static void prepare() {
    prepare(true);
}
    
private static void prepare(boolean quitAllowed) {
    if (sThreadLocal.get() != null) {
        throw new RuntimeException("Only one Looper may be created per thread");
    }
    sThreadLocal.set(new Looper(quitAllowed));
}
```

可以看到Looper类定义了一个ThreadLocal变量，在prepare方法中会在所在线程中创建一个新的Looper，并且只能有一个。这就是为什么使用了ThreadLocal。而且也描述的很清楚了：==Only one Looper may be created per thread== Looper的构造方法是private的，这表示prepare方法是唯一可以创建Looper的，而且是通过sThreadLocal来维护的。 可以发现，每一个线程最多有且仅只有一个Looper，线程之间Looper是绝对不能共享的。
看一下loop方法：

```
public static void loop() {
        //获取线程对应的looper
        final Looper me = myLooper();
        if (me == null) {
            throw new RuntimeException("No Looper; Looper.prepare() wasn't called on this thread.");
        }
        //获取looper中的MessageQueue对象
        final MessageQueue queue = me.mQueue;

        // Make sure the identity of this thread is that of the local process,
        // and keep track of what that identity token actually is.
        Binder.clearCallingIdentity();
        final long ident = Binder.clearCallingIdentity();
        //开始进行循环
        for (;;) {
            //取message，next方法可能会阻塞
            Message msg = queue.next(); // might block
            if (msg == null) {
                // No message indicates that the message queue is quitting.
                return;
            }

            ...
            try {
                //这里将通过Message中的target来处理Message。其实这个Target是一个Handler，这里调用的是Handler中的dispatchMessage方法
                msg.target.dispatchMessage(msg);
                end = (slowDispatchThresholdMs == 0) ? 0 : SystemClock.uptimeMillis();
            } finally {
                if (traceTag != 0) {
                    Trace.traceEnd(traceTag);
                }
            }
            ...
            msg.recycleUnchecked();
        }
    }
```

上面有几行代码是关键代码:
- final MessageQueue queue = me.mQueue;    
变量me是通过静态方法myLooper()获得的当前线程所绑定的Looper，me.mQueue是当前线程所关联的消息队列。
- for (;;)  
我们发现for循环没有设置循环终止的条件，所以这个for循环是个死循环。
- Message msg = queue.next(); // might block   
我们通过消息队列MessageQueue的next方法从消息队列中取出一条消息，如果此时消息队列中有Message，那么next方法会立即返回该Message，如果此时消息队列中没有Message，那么next方法就会阻塞式地等待获取Message。
- msg.target.dispatchMessage(msg);      
msg的target属性是Handler，该代码的意思是让Message所关联的Handler通过dispatchMessage方法让Handler处理该Message，关于Handler的dispatchMessage方法将会在下面详细介绍。
## Handler
我们在使用Handler的时候，有其中一种方式是类似这么用的：

```
Handler handler = new Handler() {
    @Override
    public void handleMessage(Message msg) {
        super.handleMessage(msg);
        //根据接受到的Message来处理对应的事件
        Log.i(TAG, "handleMessage: what: " + msg.what + ", obj:" +msg.obj);
    }
};

Message msg = Message.obtain();
msg.what = 0x10;
msg.obj = "处理一下";
handler.sendMessage(msg);
```

结果：

```
.../MainActivity: handleMessage: what: 16, obj:处理一下
```

尤其是在新创建的一个新线程中取处理UI事件的时候，Handler极为有用，因为新线程无法直接处理UI（Android规定）。Android甚至为了我们使用方便，设计了一个HandlerThread类，便于在非UI线程使用Handler。使用HandlerThread，必须重写onLooperPrepared方法。大体使用方式如下：

```
public class MyHandlerThread extends HandlerThread {

    private WeakReference<Context> mWeakContext;

    public MyHandlerThread(Context context) {
        super("test");
        this.mWeakContext = new WeakReference<>(context);
    }

    @Override
    protected void onLooperPrepared() {
        super.onLooperPrepared();

        Handler handler = new Handler(Looper.getMainLooper());
        handler.post(new Runnable() {
            @Override
            public void run() {
                if(mWeakContext.get() != null) {
                    Toast.makeText(mWeakContext.get(), "消息", Toast.LENGTH_SHORT).show();
                }
            }
        });
    }
}
```

HandlerThread本身是一个Thread子类，看一下其run方法：

```
@Override
public void run() {
    mTid = Process.myTid();
    Looper.prepare();
    synchronized (this) {
        mLooper = Looper.myLooper();
        notifyAll();
    }
    Process.setThreadPriority(mPriority);
    //重写该方法，便于我们处理业务
    onLooperPrepared();
    Looper.loop();
    mTid = -1;
}
```

> HandlerThread本身是一个Thread，因此如果要想在其中更新UI，必须使用主线程中的Looper。==不是任何的Handler都可以更新UI的==，这个Handler必须依赖主线程中的Looper才可以，亦即使用类似Handler handler = new Handler()创建的Handler是无法在Thread中更新UI的，必须通过获取到主线程的Looper，正确使用方式是Handler handler = new Handler(Looper.getMainLooper());

Handler除了我们sendMessage方式，还提供了post和postDelay方法。其实底层都是发送了一个消息（Message）：

```
public final boolean post(Runnable r){
   return  sendMessageDelayed(getPostMessage(r), 0);
}

public final boolean postAtTime(Runnable r, Object token, long uptimeMillis){
    return sendMessageAtTime(getPostMessage(r, token), uptimeMillis);
}

public final boolean postDelayed(Runnable r, long delayMillis){
    return sendMessageDelayed(getPostMessage(r), delayMillis);
}

private static Message getPostMessage(Runnable r) {
    Message m = Message.obtain();
    m.callback = r;
    return m;
}

//等等
```

可以看到它们最终都调用了sendMessageAtTime方法：

```
public boolean sendMessageAtTime(Message msg, long uptimeMillis) {
    MessageQueue queue = mQueue;
    if (queue == null) {
        RuntimeException e = new RuntimeException(
                this + " sendMessageAtTime() called with no mQueue");
        Log.w("Looper", e.getMessage(), e);
        return false;
    }
    //将Message插入消息队列
    return enqueueMessage(queue, msg, uptimeMillis);
}

private boolean enqueueMessage(MessageQueue queue, Message msg, long uptimeMillis) {
    //每个消息的target都将指向自己，即处理Message的Handler
    msg.target = this;
    if (mAsynchronous) {
        msg.setAsynchronous(true);
    }
    return queue.enqueueMessage(msg, uptimeMillis);
}

...
/**
 * Subclasses must implement this to receive messages.
 */
public void handleMessage(Message msg) {
}

/**
 * Handle system messages here.
 */
public void dispatchMessage(Message msg) {
    if (msg.callback != null) {
        handleCallback(msg);
    } else {
        if (mCallback != null) {
            if (mCallback.handleMessage(msg)) {
                return;
            }
        }
        handleMessage(msg);
    }
}
```

1. msg.target = this;        
在看Looper源码的时候，我们看到在Looper的loop方法中，Message会调用自己的target的dispathMessage方法。这就是那个地方为什么不会报空指针的原因。
2.

```
if (msg.callback != null) {
        handleCallback(msg);
}
```

我们在调用Handler的post方法的时候会将一个Message发送出去，这个Message通过getPostMessage获得。其实该方法会将post中的参数run传给message的callback。那么这个地方就会被执行。
3. 

```
if (mCallback != null) {
    if (mCallback.handleMessage(msg)) {
        return;
    }
}
handleMessage(msg);
```

如果mCallback不为空，那么将会执行mCallback中的handleMessage。否则就会执行Handler本身的handleMessage方法，这就是为什么我们重写handleMessage方法的原因。
而Handler中的这个方法本身什么都没有做，我们可与在该方法中处理接受到的Message。
> 源码参考API26，API版本不同源码也不尽相同