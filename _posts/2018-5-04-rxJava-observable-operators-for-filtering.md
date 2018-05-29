---
layout: post
title: RxJava1.x Observable过滤操作
date: 2018-5-04
categories: blog
tags: RxJava
description: RxJava1.x 手册
---


## Debounce

- 在指定时间内如果Observable没有发射数据才进行发射数据

![](http://reactivex.io/documentation/operators/images/debounce.png)

> 它会过滤掉发射速率过快的数据项。但是它会接着最后一项数据发射原始Observable的onComplete通知，即使这个通知也在你指定的时间内，换而言之，onComplete不会触发限流。

```
Observable<Integer> observable = Observable.create(new Observable.OnSubscribe<Integer>() {
            @Override
            public void call(Subscriber<? super Integer> subscriber) {

                if(subscriber.isUnsubscribed()) {
                    return;
                }

                subscriber.onNext(1);
                subscriber.onNext(2);

                try {
                    Thread.currentThread().sleep(2100);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                subscriber.onNext(3);
                subscriber.onNext(4);
                subscriber.onNext(5);
                subscriber.onNext(6);

                try {
                    Thread.currentThread().sleep(2100);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

                subscriber.onNext(7);
                subscriber.onNext(8);
                
                
            }
        }).debounce(2000, TimeUnit.MILLISECONDS);
        observable.subscribeOn(Schedulers.newThread());
        observable.subscribe(new Action1<Integer>() {
            @Override
            public void call(Integer integer) {
                Log.i(TAG, "call: " + integer);
            }
        });
```
```
call: 2
call: 6
call: 8
```

## distinct

- 过滤掉重复的数据项

![](http://reactivex.io/documentation/operators/images/distinct.png)

```
Observable.just(1, 2, 1, 1, 2, 3)
          .distinct()
          .subscribe(new Subscriber<Integer>() {
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
Sequence complete.
```

- distinct(Fun1)

这个操作符有一个变体接受一个函数。这个函数根据原始Observable发射的数据项产生一个Key，然后，比较这些Key而不是数据本身，来判定两个数据是否是不同的。

```
Observable.just("aaaa", "aa", "ac", "b", "cc", "bc")
        .distinct(new Func1<String, String>() {
            @Override
            public String call(String s) {
                if(s.contains("a")) {
                    return "a";
                }else if(s.contains("c")) {
                    return "c";
                }
                return "b";
            }
        }).subscribe(new Action1<String>() {
    @Override
    public void call(String s) {
        Log.i(TAG, "call: " + s);
    }
});
```
```
call: aaaa
call: b
call: cc
```

## elementAt

- 只发射第N项数据

![](http://reactivex.io/documentation/operators/images/elementAt.png)

如果你传递的是一个负数，或者原始Observable的数据项数小于index+1，将会抛出一个IndexOutOfBoundsException异常。

```
Observable.just(1, 2, 3, 4, 5)
	.elementAt(2)//指定第2项
	.subscribe(new Action1<Integer>() {
	    @Override
	    public void call(Integer integer) {
	        Log.i(TAG, "call: " + integer);
	    }
	});
```
```
call: 2
```

- 它有一个变体函数：elementAtOrDefault，它和elementAt的不同之处在于，如果你指定的索引大于数据序列的最大索引值，它不会抛出异常，而是会发射一个指定的default数据。如果你传入的是一个小于0的索引值，它仍然会抛出IndexOutOfBoundsException异常。

## filter

- 仅仅发射原始Observable中通过指定条件的的数据

![](http://reactivex.io/documentation/operators/images/filter.png)

```
Observable.just(1, 2, 3, 4, 5)
      .filter(new Func1<Integer, Boolean>() {
          @Override
          public Boolean call(Integer item) {
            return( item < 4 );
          }
      }).subscribe(new Subscriber<Integer>() {
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
Sequence complete.
```

- ofType(Class T)

它只会发射指定类型的数据

```
Observable.just("1", 10, new Student("s1"))
    .ofType(String.class)
    .subscribe(new Action1<String>() {
        @Override
        public void call(String s) {
            Log.i(TAG, "call: " + s);
        }
    });
```
```
call: 1
```

## ignoreElements

- Observable不发射任何数据，只发射一个终止通知

![](http://reactivex.io/documentation/operators/images/ignoreElements.c.png)

ignoreElements操作符抑制原始Observable中的数据发射，但是允许终止的通知（不管是onComplete还是onError）发出。如果你不关心Observable发射数据项，而只是在乎在它完成时或者发生错误终止时收到通知，ignoreElements会确保永远不会调用onNext方法。

```
Observable.create(new Observable.OnSubscribe<Integer>() {
        @Override
        public void call(Subscriber<? super Integer> subscriber) {
            subscriber.onNext(0);
            subscriber.onNext(1);
            subscriber.onNext(1);
            subscriber.onNext(1);
            subscriber.onCompleted();

        }
    }).ignoreElements().subscribe(new Observer<Integer>() {
        @Override
        public void onCompleted() {
            Log.i(TAG, "onCompleted");                
        }

        @Override
        public void onError(Throwable e) {
            Log.i(TAG, "onError");
        }

        @Override
        public void onNext(Integer integer) {
            Log.i(TAG, "onNext: " + integer);
        }
    });
```
```
onCompleted
```

## Last

- 只发射最后一条或者最后一条满足某种条件的数据

![](http://reactivex.io/documentation/operators/images/last.png)

Last操作符用于你只关心最后一条数据的发射或者在某种条件下最后发射的一条数据。

在某些实现中，Last没有实现为一个返回Observable的过滤操作符，而是实现为一个在当时就发射原始Observable指定数据项的阻塞函数。在这些实现中，如果你想要的是一个过滤操作符，最好使用TakeLast(1)。

在RxJava中的实现是last和lastOrDefault。

```
Observable.just(1, 2, 3)
          .last()
          .subscribe(new Subscriber<Integer>() {
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
Next: 3
Sequence complete.
```

或者满足某种条件：

```
Observable.just(1, 2, 3, 4, 5)
    .last(new Func1<Integer, Boolean>() {
        @Override
        public Boolean call(Integer integer) {
            return integer % 2 == 0;
        }
    })
    .subscribe(new Action1<Integer>() {
        @Override
        public void call(Integer integer) {
            Log.i(TAG, "last: " + integer);
        }
    });
```
```
last: 4
```

## Sample

- 在采样时间间隔内发射Observable中最近的一条数据

![](http://reactivex.io/documentation/operators/images/sample.png)

> 如果自上次采样以来，原始Observable没有发射任何数据，这个操作返回的Observable在那段时间内也不会发射任何数据

Sample（别名throttleLast）操作符定期的监听Observable，然后发射自上次发射数据之后的时间段内最近发射的数据。在一些实现中，它和ThrottleFirst操作符很类似，但是ThrottleFirst不是发射定期内最近（后）的一条数据，而是发射最开始的数据。

```
Observable.unsafeCreate(new Observable.OnSubscribe<String>() {
	    @Override
	    public void call(Subscriber<? super String> subscriber) {
	        try {
	            subscriber.onNext("1");
	            Thread.sleep(1000);
	            subscriber.onNext("2");
	            subscriber.onNext("3");
	            Thread.sleep(1000);
	            subscriber.onNext("4");
	            Thread.sleep(1000);
	            subscriber.onNext("5");
	            Thread.sleep(1000);
	            subscriber.onNext("6");
	        }catch (Exception e) {
	
	        }
	    }
	}).sample(2, TimeUnit.SECONDS)
    .subscribe(new Action1<String>() {
        @Override
        public void call(String s) {
            Log.i(TAG, "call: " + s);
        }
    });
```
```
call: 3
call: 5
call: 6
```

## Skip

-  忽略指定条件下的数据

![](http://reactivex.io/documentation/operators/images/skip.png)

```
Observable.just(1, 2, 3, 4, 5, 6)
        .skip(3)
        .subscribe(new Action1<Integer>() {
            @Override
            public void call(Integer integer) {
                Log.i(TAG, "call: " + integer);
            }
        });
```

skip有一些变体函数，它们的表达的含义大致相同。与之对应的为**skipLast**，表示忽略指定条件下后面的数据，意义和skip正好相反。

## Take

- 和Skip意义相反，表示保留指定条件下的数据项，即只发射前n项数据，忽略剩余的数据

![](http://reactivex.io/documentation/operators/images/take.png)

```
Observable.just(1, 2, 3, 4, 5, 6, 7, 8)
          .take(4)
          .subscribe(new Subscriber<Integer>() {
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

如果你要保留的数据少于你指定的数据时，take操作符并不会触发onError方法，而是直接触发onComplete。
与之对应的操作符为**TakeLast**，可保留指定的后面的n项数据。