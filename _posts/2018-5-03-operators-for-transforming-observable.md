---
layout: post
title: RxJava1.x Observable变换操作
date: 2018-5-07
categories: blog
tags: RxJava
description: RxJava1.x 手册
---

## buffer
- 定期收集Observable的数据并放入数据包裹中并发射，而不是每次发射一个数据

![](http://reactivex.io/documentation/operators/images/Buffer.png)

Buffer操作符将一个Observable变换为另一个，原来的Observable正常发射数据，变换产生的Observable发射这些数据的缓存集合。Buffer操作符在很多语言特定的实现中有很多种变体，它们在如何缓存这个问题上存在区别。

> 注意：如果原来的Observable发射了一个onError通知，Buffer会立即传递这个通知，而不是首先发射缓存的数据，即使在这之前缓存中包含了原始Observable发射的数据。

```
Observable.range(1, 5)
                .buffer(3).subscribe(new Observer<List<Integer>>() {
            @Override
            public void onCompleted() {
                Log.i(TAG, "onCompleted");
            }

            @Override
            public void onError(Throwable e) {

            }

            @Override
            public void onNext(List<Integer> integers) {
                Log.i(TAG, "onNext: " + integers);
            }
        });
```
```
onNext: [1, 2, 3]
onNext: [4, 5]
onCompleted
```
变体：

- buffer(count)
- buffer(count, skip)
- buffer(bufferClosingSelector)
- buffer(boundary)
- buffer(bufferOpenings, bufferClosingSelector)等


## flatMap
flatMap将一个发射数据的Observable变换为多个observable，然后将它们发射的数据合并后放进一个单独的Observable。

![](http://reactivex.io/documentation/operators/images/flatMap.c.png)

flatMap应用了一个对原始Observable中的每一个要发射的数据执行变换操作的方法，而这个方法返回一个同样发射数据的Observable。FlatMap会合并这些Observable发射的数据，最后将合并后的数据当做自己的数据进行发射。

> flatMap对这些Observable进行的是合并操作，因此并不保证发射它们的顺序。

```
public class Student {

    public String name;
    public List<Course> courses;

    public Student(String name) {
        this.name = name;
        courses = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            Course course = new Course();
            course.title = "course" + i;
            course.score = new Random().nextInt(100);
            courses.add(course);
        }
    }

}

public class Course {

    public String title;

    public int score;

    @Override
    public String toString() {
        return "title: " + title + "/tscore: " + score;
    }
}

Observable.just(new Student("s1"), new Student("s2"), new Student("s3")
                , new Student("s4"))
                .flatMap(new Func1<Student, Observable<Course>>() {
                    @Override
                    public Observable<Course> call(Student student) {
                        Log.i(TAG, "call: " + student.name);
                        return Observable.from(student.courses);
                    }
                }).subscribe(new Action1<Course>() {
            @Override
            public void call(Course course) {
                Log.i(TAG, "call: " + course);
            }
        });
```
```
call: s1
call: title: course0/tscore: 66
call: title: course1/tscore: 98
call: title: course2/tscore: 5
call: title: course3/tscore: 47
call: title: course4/tscore: 26
call: s2
call: title: course0/tscore: 10
call: title: course1/tscore: 27
call: title: course2/tscore: 64
call: title: course3/tscore: 69
call: title: course4/tscore: 16
...
```
> 虽然这个例子看起来是有序的，flatMap并不能被保证对结果顺序

- contactMap		
它类似flatMap，但是和flatMap的区别在于contactMap保证发射结果的顺序

- switchMap		
它类似flatMap，当对原始Observable发射一个新的数据时，它将会对上一个数据的解除订阅并停止发射，然后仅仅作用于当前这一个。

将上一个代码例子中**flatMap**换做**switchMap**并且在Observable.from(student.courses)处将其切换线程（让不在同一个线程，使其并行发生），比如改为Observable.from(student.courses).subscribeOn(Schedulers.newThread())，其结果如下：

```
call: s1
call: s2
call: s3
call: s4
call: title: course0/tscore: 44
call: title: course1/tscore: 44
call: title: course2/tscore: 79
call: title: course3/tscore: 59
call: title: course4/tscore: 58
```

## GroupBy
- 它将原始Observable分成若干个（你所指定的）Observable，每一个Observable会发射原始Observable中要发射的数据的子集。

![](http://reactivex.io/documentation/operators/images/groupBy.c.png)

哪个数据由哪个Observable发射会有一个方法指定，这个方法返回一个Key，Key相同的数据会被分到指定的Observable中，最后会由该Observable发射。
订阅者接受到的是一个Observable的一个特殊子类GroupedObservable

```
Observable.just("a1", "a2", "b1", "b2", "c1", "c2")
    .groupBy(new Func1<String, Integer>() {
        @Override
        public Integer call(String s) {
            //返回的是key
            if(s.contains("1")) {
                return 1;
            }
            return 2;
        }
    }).subscribe(new Action1<GroupedObservable<Integer, String>>() {
        @Override
        public void call(final GroupedObservable<Integer, String> integerStringGroupedObservable) {
            integerStringGroupedObservable.subscribe(new Action1<String>() {
                @Override
                public void call(String s) {
                    Log.i(TAG, "key: " + integerStringGroupedObservable.getKey() + " value: " + s);
                }
            });
        }
    });
```
```
key: 1 value: a1
key: 2 value: a2
key: 1 value: b1
key: 2 value: b2
key: 1 value: c1
key: 2 value: c2
```

> groupBy将原始Observable分解为一个发射多个GroupedObservable的Observable，一旦有订阅，每个GroupedObservable就开始缓存数据。因此，如果你忽略这些GroupedObservable中的任何一个，这个缓存可能形成一个潜在的`内存泄露`。因此，如果你不想观察，也不要忽略GroupedObservable。你应该使用像take(0)这样会丢弃自己的缓存的操作符。如果你取消订阅一个GroupedObservable，那个Observable将会终止。如果之后原始的Observable又发射了一个与这个Observable的Key匹配的数据，groupBy将会为这个Key创建一个新的GroupedObservable

## Map

- 给Observable中要发射的每一个数据应用一个函数

![](http://reactivex.io/documentation/operators/images/map.png)

```
Observable.just(new Student("s1"), new Student("s2"), new Student("s3"))
                .map(new Func1<Student, List<Course>>() {
                    @Override
                    public List<Course> call(Student student) {
                        Log.i(TAG, "call: " + student.name);
                        return student.courses;
                    }
                }).subscribe(new Action1<List<Course>>() {
            @Override
            public void call(List<Course> courses) {
                for (Course course : courses) {
                    Log.i(TAG, "call: " + course);
                }
            }
        });
```
结果会输出s1,s2,s3对应的course列表结果。

## Cast

- 它是Map的一个特殊版本，它会将原始Observable要发射的每一个数据进行强制转换成另一种类型，然后在进行发射。

![](http://reactivex.io/documentation/operators/images/cast.png)

```
Observable.just(1, 2)
    .cast(Integer.class)
    .subscribe(new Action1<Integer>() {
        @Override
        public void call(Integer integer) {
            Log.i(TAG, "call: " + integer);
        }
    });
```
```
call: 1
call: 2
```

## Scan
- 给Observable每一个要发射的数据连续的应用一个函数，然后发射每一个连续的结果。即会将前面的数据应用到后面一个数据中

![](http://reactivex.io/documentation/operators/images/scan.png)

scan对原始Observable发射的第一项数据应用一个函数，然后将那个函数的结果作为自己的第一项发射。它将函数的结果作为同第二项数据一起填充给这个函数来产生自己的第二项数据。然后持续进行这个过程来产生剩余的数据序列。这个操作在某些情况下叫做"accumutor"。

```
Observable.just(1, 2, 3, 4, 5)
        .scan(new Func2<Integer, Integer, Integer>() {
            @Override
            public Integer call(Integer sum, Integer integer) {
                Log.i(TAG, "call: " + sum + "," + integer);
                return sum + integer;
            }
        }).subscribe(new Action1<Integer>() {
    @Override
    public void call(Integer integer) {
        Log.i(TAG, "call: " + integer);
    }
});
```

```
call: 1
call: 1,2
call: 3
call: 3,3
call: 6
call: 6,4
call: 10
call: 10,5
call: 15
```

scan有一个变体版本scanSeed即scan(R seed, Func2)，它允许你传递一个种子值给累加器的第一个值使用，注意，它将会发射种子值来作为自己的第一项数据。

```
Observable.just(1, 2, 3, 4, 5)
        .scan("result: ", new Func2<String, Integer, String>() {
            @Override
            public String call(String s, Integer integer) {
                return s + integer;
            }
        }).subscribe(new Action1<String>() {
    @Override
    public void call(String s) {
        Log.i(TAG, s);
    }
});
```
```
result: 
result: 1
result: 12
result: 123
result: 1234
result: 12345
```

## Window

- 定期的从原始Observable中将数据分块给Observable窗口，然后发射这些窗口，而不是发射每次发射一个原始数据。

![](http://reactivex.io/documentation/operators/images/window.C.png)

乍看起来很像buffer，但是它不是发射一个个的数据包，而是发射一个Observable，每一个Observable都会发射从原始数据中被分块出去的数据，并在结束的时候调用onCompleted。

当一个窗口打开(when a window "opens")意味着一个新的Observable已经发射（产生）了，而且这个Observable开始发射来自原始Observable的数据；当一个窗口关闭(when a window "closes")意味着发射(产生)的Observable停止发射原始Observable的数据，并且发射终止通知onCompleted给它的观察者们。

```
Observable.just(1, 2, 3, 4, 5, 6)
    .window(3)
    .subscribe(new Action1<Observable<Integer>>() {
        @Override
        public void call(final Observable<Integer> integerObservable) {
            integerObservable.subscribe(new Subscriber<Integer>() {
                @Override
                public void onCompleted() {
                    Log.i(TAG, integerObservable.hashCode() + "onCompleted");
                }

                @Override
                public void onError(Throwable e) {

                }

                @Override
                public void onNext(Integer integer) {
                    Log.i(TAG, integerObservable.hashCode() 
                    + "onNext: " + integer);
                }
            });
        }
    });
```
```
169705140onNext: 1
169705140onNext: 2
169705140onNext: 3
169705140onCompleted
241302237onNext: 4
241302237onNext: 5
241302237onNext: 6
241302237onCompleted
```
它有类似buffer的一些变体。

[更多参考点击这里](http://reactivex.io/documentation/operators.html)