---
layout: post
title: EventBus
date: 2018-6-10
categories: blog
tags: tools
description: tools


EventBus 传送门：[点击这里](https://github.com/greenrobot/EventBus)

官方文档：[EventBus Documentation](http://greenrobot.org/eventbus/documentation/)

##### 使用EventBus步骤

1. 定义事件类

EventBus传递的类继承自Object，表示你可以传递任何类型的类

```
public class MessageEvent {

    public final String message;

    public MessageEvent(String message) {
        this.message = message;
    }
}
```

2. 订阅

当事件被发布之后，订阅者可以通过实现为处理事件而定义的方法去处理这些事件。这些方法需要用注解进行标记：@Subscribe。处理事件的方法名称可以自由命名，并没有特殊限制（这区别与EventBus 2.x）。

```
// This method will be called when a MessageEvent is posted (in the UI thread for Toast)
@Subscribe(threadMode = ThreadMode.MAIN)
public void onMessageEvent(MessageEvent event) {
    Toast.makeText(getActivity(), event.message, Toast.LENGTH_SHORT).show();
}

// This method will be called when a SomeOtherEvent is posted
@Subscribe
public void handleSomethingElse(SomeOtherEvent event) {
    doSomethingWith(event);
}
```

订阅者需要注册和反注册。只有订阅者被注册才能够接受发布的事件。在Android的Activity和Fragment中，可以根据具体情况进行注册和反注册，比如：

```
@Override
public void onStart() {
    super.onStart();
    EventBus.getDefault().register(this);
}

@Override
public void onStop() {
    EventBus.getDefault().unregister(this);
    super.onStop();
}
```
或者在onCreate或者onDestroy中进行注册和反注册，具体情况按己所需。

3. 发布事件
 
在其他部分的代码中发布事件，所有当前注册的订阅者只要符合发布事件的事件类型都可以接受到该事件。

```
EventBus.getDefault().post(new MessageEvent("Hello everyone!"));
```

Android的UI变化只能在UI线程即主线程中进行，而网络请求或者其他有耗时操作的任务都不应该在主线程中进行。EventBus可以处理这种类型的事件发布，而并不需要使用类似AsyncTask这种方式。

## 线程模式


可以定义多种线程模式来指定处理不同线程所发布的事件。

1). POSTING

订阅者会处理在同一个线程当中所发布的事件。这是默认模式。这种模式开销最小，因为它避免了线程之间的切换。用这种方法处理事件应很快就返回结果避免当前线程为主线程的时候发生ANR。

```
// Called in the same thread (default)
// ThreadMode is optional here
@Subscribe(threadMode = ThreadMode.POSTING)
public void onMessage(MessageEvent event) {
    log(event.message);
}
```

2). MAIN

事件的处理会在UI线程中进行

```
// Called in Android UI's main thread
@Subscribe(threadMode = ThreadMode.MAIN)
public void onMessage(MessageEvent event) {
    textField.setText(event.message);
}
```

3). MAIN_ORDER

不同于MAIN模式，这种事件会排队进行发送，这避免了事件处理可能会发生ANR的问题

```
// Called in Android UI's main thread
@Subscribe(threadMode = ThreadMode.MAIN_ORDERED)
public void onMessage(MessageEvent event) {
    textField.setText(event.message);
}
```

4). BACKGROUN

事件处理会在非主线程进行。如果发布事件的线程是非主线程，事件会立即被处理，如果是主线程，则会用一个新线程进行处理事件，这也会让事件有序的进行发送。

```
// Called in the background thread
@Subscribe(threadMode = ThreadMode.BACKGROUND)
public void onMessage(MessageEvent event){
    saveToDisk(event.message);
}
```

5). ASYNC

无论事件在哪个线程发布，事件的处理都会在一个新的子线程中进行。这种模式通常用来处理耗时操作，而不用来更新UI。它避免了触发大量数据长期运行异步订阅者方法，同时了限制并发线程的数量，内部会有一个可复用线程的线程池有效的控制异步问题。

```
// Called in a separate thread
@Subscribe(threadMode = ThreadMode.ASYNC)
public void onMessage(MessageEvent event){
    backend.send(event.message);
}
```
## 配置

**EventBusBuilder**类可以配置多种多样的EventBus属性，例如，下面代码片段构建了一个当没有订阅者订阅就开始发布消息时使程序保持正常状态（不会有log和crash产生）

```
EventBus eventBus = EventBus.builder()
    .logNoSubscriberMessages(false)
    .sendNoSubscriberEvent(false)
    .build();
```

另一个例子是当订阅者抛出异常时失败：

```
EventBus eventBus = EventBus.builder().throwSubscriberException(true).build();
```

默认情况下，EventBus会从订阅者方法中捕获异常并发送一个==SubscriberExceptionEvent==，但这是可以被处理的。

使用EventBus.getDefault()是一种在app中任何地方都可以获取一个共享实例的简单方式。EventBusBuilder也允许使用==installDefaultEventBus==来配置这个默认的EventBus实例。

比如，可能会配置这个默认的EventBus在当发生异常时重抛异常。但是因为这可能会导致程序crash，所以仅限在Debug模式下使用：

```
EventBus.builder().throwSubscriberException(BuildConfig.DEBUG).installDefaultEventBus();
```

> 注意：只能在你第一次使用这个EventBus之前才可以这样做，重复的调用==installDefaultEventBus==将会导致异常出现。这保证了APP统一的行为方式。通常会在Application中取配置默认的EventBus。

## 粘性事件

如果先发布了事件，然后有订阅者订阅该事件，除非重新发布该事件，否则订阅者将永远接受不到该事件。此时可以使用粘性事件。或者如果你有一些传感器或位置数据，你想保存最近的值。与其自己实现该此类缓存，不如使用粘性事件。其实EventBus会在内存保留特定类型的==最后一个==粘性事件，直到有订阅订阅此事件，订阅将接受到该事件。

发送粘性广播：

```
EventBus.getDefault().postSticky(new MessageEvent("Hello everyone!"));
```

对于要接受粘性事件的方法必须在注解中添加**sticky = true**的标识。

```
@Override
public void onStart() {
    super.onStart();
    EventBus.getDefault().register(this);
}

// UI updates must run on MainThread
@Subscribe(sticky = true, threadMode = ThreadMode.MAIN)
public void onEvent(MessageEvent event) {   
    textField.setText(event.message);
}

@Override
public void onStop() {
    EventBus.getDefault().unregister(this);    
    super.onStop();
}
```

检查粘性事件的方法也比较方便。同时，如果一个粘性事件你认为将不再需要被发送，你应该手动的移除掉它。

```
MessageEvent stickyEvent = EventBus.getDefault().getStickyEvent(MessageEvent.class);
// Better check that an event was actually posted before
if(stickyEvent != null) {
    // "Consume" the sticky event
    EventBus.getDefault().removeStickyEvent(stickyEvent);
    // Now do something with it
}
```

==removeStickyEvent==如果成功移除了这个粘性事件会返回这个事件。所以你可以改善一下上述代码：

```
MessageEvent stickyEvent = EventBus.getDefault().removeStickyEvent(MessageEvent.class);
// Better check that an event was actually posted before
if(stickyEvent != null) {
    // Now do something with it
}
```

## 优先级和事件取消

### 订阅事件的优先级

你可以通过设置订阅事件的优先级来改变接受发送事件的顺序，只需要在@Subscriber注解中设置priority的优先级值即可。

```
@Subscribe(priority = 1);
public void onEvent(MessageEvent event) {
    ...
}
``` 

在相同的接受事件的线程模式中，高优先级的订阅事件会更早接收到发送的事件。默认的优先级为**0**。

> 在不同的线程模式中，通过设置优先级来控制接受事件的顺序是无效的。

### 取消发送事件

你可以在优先级的订阅者方法中收到发送事件后取消事件的传递。此时，低优先级的事订阅者事件将不会再收到该事件。**注意，订阅者方法只有在线程模式为==ThreadMode.POSTING==时，才可以取消事件的传递。**

```
// Called in the same thread (default)
@Subscribe
public void onEvent(MessageEvent event){
    // Process the event
    ...
    // Prevent delivery to other subscribers
    EventBus.getDefault().cancelEventDelivery(event) ;
}
```

## 订阅者索引

订阅者索引是EventBus 3的新特性。它是加速订阅者注册的可选优化。订阅者索引的原理是：使用EventBus的注解处理器在应用构建期间创建订阅者索引类，该类包含了订阅者和订阅者方法的相关信息。EventBus**官方推荐**在Android中使用订阅者索引以获得最佳的性能。


> 注意，至于订阅者和事件类为public的订阅者方法才可以使用订阅者索引。并且由于Java语言的技术限制，@Subscriber注解在匿名内部类无法被识别。当EvenBus无法使用订阅者索引时，它将自动在运行期间使用反射的方式，因此，它依然可以工作，只是变慢了而已。

要开启订阅者索引的生成，你需要在构建脚本中使用annotationProcessor属性将EventBus的注解处理器添加到应用的构建中，还要设置一个eventBusIndex参数来指定要生成的订阅者索引的完全限定类名。

```
android {
    defaultConfig {
        javaCompileOptions {
            annotationProcessorOptions {
                arguments = [ eventBusIndex : 'com.example.myapp.MyEventBusIndex' ]
            }
        }
    }
}

dependencies {
    implementation 'org.greenrobot:eventbus:3.1.1'
    annotationProcessor 'org.greenrobot:eventbus-annotation-processor:3.1.1'
}
```

配置好之后，EventBus注解处理器会为你生成一个订阅者索引类：

```
/** This class is generated by EventBus, do not edit. */
public class MyEventBusIndex implements SubscriberInfoIndex {
    private static final Map<Class<?>, SubscriberInfo> SUBSCRIBER_INDEX;

    static {
        SUBSCRIBER_INDEX = new HashMap<Class<?>, SubscriberInfo>();

        putIndex(new SimpleSubscriberInfo(MainActivity.class, true, new SubscriberMethodInfo[] {
            new SubscriberMethodInfo("onMessageEvent", MessageEvent.class, ThreadMode.MAIN),
        }));

    }

    private static void putIndex(SubscriberInfo info) {
        SUBSCRIBER_INDEX.put(info.getSubscriberClass(), info);
    }

    @Override
    public SubscriberInfo getSubscriberInfo(Class<?> subscriberClass) {
        SubscriberInfo info = SUBSCRIBER_INDEX.get(subscriberClass);
        if (info != null) {
            return info;
        } else {
            return null;
        }
    }
}
```

之后还需要配置EventBus：

```
EventBus eventBus = EventBus.builder().addIndex(new MyEventBusIndex()).build();
```

或者配置默认的EventBus实例：

```
EventBus.builder().addIndex(new MyEventBusIndex()).installDefaultEventBus();
// Now the default instance uses the given index. Use it like this:
EventBus eventBus = EventBus.getDefault();
```

你可以使用相同的方式给library module配置EventBus订阅者索引，这个时候可能会需要设置订阅者索引：

```
EventBus eventBus = EventBus.builder()
    .addIndex(new MyEventBusAppIndex())
    .addIndex(new MyEventBusLibIndex()).build();
```

## 混淆

混淆会帮助你修改你的方法名使其难以阅读，也会移除那些没有被使用的方法。因为订阅者方法不是直接被调用，混淆时会认为这些方法是无用的。所以你需要在混淆时告知它这些订阅者需要被保持不混淆。可以使用一下规则保持订阅者方法不被混淆：

```
-keepattributes *Annotation*
-keepclassmembers class * {
    @org.greenrobot.eventbus.Subscribe <methods>;
}
-keep enum org.greenrobot.eventbus.ThreadMode { *; }
 
# Only required if you use AsyncExecutor
-keepclassmembers class * extends org.greenrobot.eventbus.util.ThrowableFailureEvent {
    <init>(java.lang.Throwable);
}
```

> 只要你使用混淆，你必须这么做，不管你是否使用了订阅者索引。