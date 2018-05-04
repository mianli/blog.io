---
layout: post
title: 这是一篇博客文章模板
date: 2015-3-02
categories: blog
tags: [标签一,标签二]
description: 文章金句。
---

这里是博客正文。













# RxJava1.x Observable创建操作
## just
- 创建一个可发射精确条目的可观察者

![](http://reactivex.io/documentation/operators/images/just.c.png)

just操作符可以将一个item转化成一个可发射它的可观察者（Observable）。		

Just很类似From，但是From会将一个数组array或者iterable或者有序的其他数据结构逐个的进行发射，而Just会简单地将它们当做单个数据并原样发射。
> 注意：如果你传递null给just，它将返回一个可以发射null数据的可观察者（Observable），不要错误的认为它将创建一个空的可观察者（即不发射任何数据的可观察者），如果你想这么做，需要使用Empty操作符。

```
Observable.just(1, 2, 3)
    .subscribe(new Subscriber<Integer>() {
        @Override
        public void onCompleted() {
            Log.i(TAG, "onCompleted");
        }

        @Override
        public void onError(Throwable e) {
            Log.i(TAG, "onError: " + e.getMessage());
        }

        @Override
        public void onNext(Integer integer) {
            Log.i(TAG, "onNext: " + integer);
        }
    });
```
           
## from       
      
- 将多个实例和数据类型转化成可观察者（Observable）

![](http://reactivex.io/documentation/operators/images/from.c.png)

当你使用Observable时，如果你需要处理的数据都可以展现为Observable，而不是需要混合使用Observables和其他类型数据的时候，From会非常方便。这让你可以用一组统一的操作符来管理数据的生命期限。	
例如，Iterable可以看成是同步的Observable；Future，可以看成是总是只发射单个数据的Observable。通过显式地将那些数据转换为Observables，你可以像使用Observable一样与它们交互。

```
Integer[] items = { 0, 1, 2, 3, 4, 5 };
Observable myObservable = Observable.from(items);

myObservable.subscribe(
    new Action1<Integer>() {
        @Override
        public void call(Integer item) {
            System.out.println(item);
        }
    },
    new Action1<Throwable>() {
        @Override
        public void call(Throwable error) {
            System.out.println("Error encountered: " + error.getMessage());
        }
    },
    new Action0() {
        @Override
        public void call() {
            System.out.println("Sequence complete");
        }
    }
);
```
```
0
1
2
3
4
5
Sequence complete
```
至于Future，它会发射get方法返回的单个数据。from方法有一个可接受两个可选参数的版本，分别指定超时时长和时间单位，指定这两个参数与否会相应的调用对应的get方法。如果过了指定的时长Future还没有返回一个值，这个Observable会发射错误通知并终止。

```
Observable.from(new Future<Integer>() {
            @Override
            public boolean cancel(boolean mayInterruptIfRunning) {

                return false;
            }

            @Override
            public boolean isCancelled() {
                return false;
            }

            @Override
            public boolean isDone() {
                return false;
            }

            @Override
            public Integer get() throws InterruptedException, ExecutionException {
                return 2;
            }

            @Override
            public Integer get(long timeout, @NonNull TimeUnit unit) throws InterruptedException, ExecutionException, TimeoutException {
                return 1;
            }
        }, 1, TimeUnit.SECONDS)
        .subscribe(new Action1<Integer>() {
            @Override
            public void call(Integer integer) {
                Log.i(TAG, "call: " + integer);
            }
        }, new Action1<Throwable>() {
            @Override
            public void call(Throwable throwable) {
                Log.i(TAG, "call: " + throwable.getMessage());
            }
        }, new Action0() {
            @Override
            public void call() {
                Log.i(TAG, "call: oncomplete");
            }
        });
```
```
call: 1
call: oncomplete
```

from默认不在任何特定的调度器上执行。然而你可以将Scheduler作为可选的第二个参数传递给Observable，它会在那个调度器上管理这个Future。
## create
- 从头开始创建一个可观察者（Observable）
- **advanced use only!**——平时不要使用它！	

![](http://reactivex.io/documentation/operators/images/create.c.png)

你可以传递给这个操作符一个observer作为参数。编写这个函数，通过合适的调用observer的onNext,onError,onComplete方法来让它表现为Observable。一个正确形式是必须让Observable尝试调用onComplete或者onError（只能）一次，并且这两个方法是互斥的。		
建议你在传递给create方法的函数中检查观察者的isUnsubscribed状态，以便在没有观察者的时候，让你的Observable停止发射数据或者做昂贵的运算。

```
Observable.create(new Observable.OnSubscribe<Integer>() {
    @Override
    public void call(Subscriber<? super Integer> observer) {
        try {
            if (!observer.isUnsubscribed()) {
                for (int i = 1; i < 5; i++) {
                    observer.onNext(i);
                }
                observer.onCompleted();
            }
        } catch (Exception e) {
            observer.onError(e);
        }
    }
 } ).subscribe(new Subscriber<Integer>() {
        @Override
        public void onNext(Integer item) {
            System.out.println("Next: " + item);
        }

        @Override
        public void onError(Throwable error) {
            System.err.println("Error: " + error.getMessage());
        }

        @Override
        public void onCompleted() {
            System.out.println("Sequence complete.");
        }
    });
```

```
Next: 1
Next: 2
Next: 3
Next: 4
Sequence complete.
```
create方法默认不在任何特定的调度器上执行。

## defer
- 直到有订阅才创建可观察者（Observable），会为每一个Observer创建一个新的Observable。

![](http://reactivex.io/documentation/operators/images/defer.c.png)

defer操作符会一直等到有Observer订阅它，才会创建一个Observable。它会为每一个Subscriber创建一个新的Observable，这会让每一个Subscriber认为它们在操作同一个Observable，而事实上，每一个Subscriber各自拥有独立的数据队列。		
在某些情况下，为确保Observable包含了最新的数据，直到最后一刻才会创建Observable。

```
int a = 10;
Observable<Integer> observable = Observable.defer(new Func0<Observable<Integer>>() {
            @Override
            public Observable<Integer> call() {
                return Observable.just(a);
            }
        });
a = 20;
observable.subscribe(new Action1<Integer>() {
            @Override
            public void call(Integer integer) {
                Log.i(TAG, "defer call: " + integer);
            }
        });
```  
```
defer call: 20
```
下面的例子可以看出和just相关操作符的区别。

```
int a = 10;
Observable<Integer> observable = 
	Observable.defer(new Func0<Observable<Integer>>() {
        @Override
        public Observable<Integer> call() {
            return Observable.just(a);
        }
    });
Observable<Integer> observable1 = Observable.just(a);
observable1.subscribe(new Action1<Integer>() {
    @Override
    public void call(Integer integer) {
        Log.i(TAG, "just call: " + integer);
    }
});
a = 20;
observable.subscribe(new Action1<Integer>() {
    @Override
    public void call(Integer integer) {
        Log.i(TAG, "defer call: " + integer);
    }
});
```
```
just call: 10
defer call: 20
```
可以看出，defer操作符会取a最新的值。

## range
- 发射一个范围内的有序整数序列，你可以指定范围的起始和长度。

![](http://reactivex.io/documentation/operators/images/range.c.png)

> 如果你将第二个参数设为0，将导致Observable不发射任何数据（如果设置为负数，会抛异常）。
> range默认不在任何特定的调度器上执行。

```
Observable<Integer> observable = Observable.range(1, 9);
    observable.subscribe(new Action1<Integer>() {
        @Override
        public void call(Integer integer) {
            Log.i(TAG, "call: " + integer);
        }
    });
```
```
1
...
9
```
## interval
- 创建一个按固定时间间隔发射整数序列的Observable

![](http://reactivex.io/documentation/operators/images/interval.c.png)

```
Observable.interval(1, TimeUnit.SECONDS)
    .subscribe(new Action1<Long>() {
        @Override
        public void call(Long aLong) {
            Log.i(TAG, "call: " + aLong.intValue());
        }
    });
```
每一秒发射一个递增后的数据：

```
0
1
2
...
```

## timer
- 它和interval的区别是它只发射一个特殊的值——一个简单的数字0。

![](http://reactivex.io/documentation/operators/images/timer.c.png)

```
Observable.timer(1, TimeUnit.SECONDS)
	.subscribe(new Action1<Long>() {
	    @Override
	    public void call(Long aLong) {
	        Log.i(TAG, "call: " + aLong.intValue());
	    }
	});
```
```
0
```
timer操作符默认在computation调度器上执行。

### Empty、Never、Throw
- Empty		
创建一个不发射任何数据但是正常终止的Observable
- Never			
创建一个不发射数据也不终止的Observable
- Throw			
创建一个不发射数据以一个错误终止的Observable

这三个操作符生成的Observable行为非常特殊和受限。测试的时候很有用，有时候也用于结合其它的Observables，或者作为其它需要Observable的操作符的参数。		
RxJava将这些操作符实现为 empty，never和error。error操作符需要一个Throwable参数，你的Observable会以此终止。这些操作符默认不在任何特定的调度器上执行，但是empty和error有一个可选参数是Scheduler，如果你传递了Scheduler参数，它们会在这个调度器上发送通知。