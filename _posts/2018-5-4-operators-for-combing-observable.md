

# Combine

- 当两个Observable中有任何一个发射数据时，另一个Observable会通过一个指定的方法与它最近发射的数据项结合，并发射通过这个指定方法发射一个其结合的结果。

![](http://reactivex.io/documentation/operators/images/combineLatest.png)

CombineLatest操作符行为类似于zip，但是只有当原始的Observable中的每一个都发射了一条数据时zip才发射数据。CombineLatest则在原始的Observable中任意一个发射了数据时发射一条数据。当原始Observables的任何一个发射了一条数据时，CombineLatest使用一个函数结合它们最近发射的数据，然后发射这个函数的返回值。

```
Observable<String> o1 = Observable.create(new Observable.OnSubscribe<String>() {
            @Override
            public void call(Subscriber<? super String> subscriber) {
                try {
                    if(!subscriber.isUnsubscribed()) {
                        subscriber.onNext("1");
                        Thread.sleep(2000);
                        subscriber.onNext("2");
                        Thread.sleep(7000);
                        subscriber.onNext("3");
                        Thread.sleep(1000);
                        subscriber.onNext("4");
                    }
                }catch (Exception e) {
                }
            }
        }).subscribeOn(Schedulers.newThread());

        Observable<String> o2 = Observable.create(new Observable.OnSubscribe<String>() {
            @Override
            public void call(Subscriber<? super String> subscriber) {
                try {
                    if(!subscriber.isUnsubscribed()) {
                        Thread.sleep(1000);
                        subscriber.onNext("a");
                        Thread.sleep(2000);
                        subscriber.onNext("b");
                        Thread.sleep(5000);
                        subscriber.onNext("c");
                        Thread.sleep(6000);
                        subscriber.onNext("b");
                    }
                }catch (Exception e) {
                }
            }
        }).subscribeOn(Schedulers.newThread());

        //注意，两个Observable一定要在不同的线程当中，因为同一个线程会造成发射数据阻塞，
        //导致只会有一个Observable的最后一个数据和另一个发射的数据结合
        Observable.combineLatest(o1, o2, new Func2<String, String, String>() {
            @Override
            public String call(String s1, String s2) {
                return s1 + s2;
            }
        }).subscribe(new Action1<String>() {
            @Override
            public void call(String s) {
                Log.i(TAG, "call: " + s);
            }
        });
```