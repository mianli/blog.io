# Row和Column


## 主轴和纵轴

两种类似的线性布局，Row是横向布局，Column是纵向布局。对于线性布局有主轴和纵轴之分，有两个枚举定义分别表示是主轴还是纵轴：MainAxisAlignment和CrossAxisAlignment。
如果是Row，即为横向布局的时候，主轴是指水平方向，纵轴为垂直方向；当布局为Column时，主轴为垂直方向，纵轴为水平方向。更为方便的，既然有主轴，就可以理解为另一个为辅轴（纵轴），因为纵轴的理解虽然是专业叫法，但是主副之分才更合乎大众理解。


## Row

Row是指水平方向的布局。


```
Row({
    Key key,
    MainAxisAlignment mainAxisAlignment = MainAxisAlignment.start,
    MainAxisSize mainAxisSize = MainAxisSize.max,
    CrossAxisAlignment crossAxisAlignment = CrossAxisAlignment.center,
    TextDirection textDirection,
    VerticalDirection verticalDirection = VerticalDirection.down,
    TextBaseline textBaseline,
    List<Widget> children = const <Widget>[],
  })
```

TextDirection：表示子控件的排列顺序，到底是从左到右还是从右到左...开始进行排列。默认排列顺序为系统的Local环境，一般都是从左到右，阿拉伯语从右到左。

mainAxisSize： 表示在主轴方向上占用的空间。它有两个值：MainAxisSize.max、MainAxisSize.min，默认为MainAxisSize.max，表示子控件尽可能的和父容器大小保持一致，而MainAxisSize.min表示适合自己的大小，尽可能少的占用父容器的控件，如果子控件没有占满Row水平空间的大小，则Row的实际大小为子控件水平方向的宽度总和。

mainAxisAlignment：表示子控件子Row内的对齐方式。可以这么理解，如果TextDirection方向要从左到右即TextDirection.ltr，那么MainAxisAlignment.start就是从左开始布局子控件，MainAxisAlignment.end则相反；如果TextDirection方向要从左到右即TextDirection.rtl，那么MainAxisAlignment.start就是从右开始布局子控件，MainAxisAlignment.end则相反。mainAxisSize为MainAxisSize.min时，因为Row的实际大小跟子控件的宽度总和相同，所有此时设置该参数没有意义。

> 由此可以看出，一般TextDirection、mainAxisSize、mainAxisAlignment三者是配合使用的。


verticalDirection：表示Row垂直方向（纵轴）上的排列方向。默认为VerticalDirection.down，表示从上向下。**这个值一般和下面的crossAxisAlignment配合使用。**

crossAxisAlignment：表示子组件在纵轴方向的对齐方式，Row的高度等于子组件中最高的子元素高度，它的取值和MainAxisAlignment一样(包含start、end、 center三个值)，不同的是crossAxisAlignment的参考系是verticalDirection。即verticalDirection值为VerticalDirection.down时crossAxisAlignment.start指顶部对齐，verticalDirection值为VerticalDirection.up时，crossAxisAlignment.start指底部对齐；而crossAxisAlignment.end和crossAxisAlignment.start正好相反；


```
...
...

@override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text("hello world"),
                Text("I am Jack")
              ],
            ),
            Row(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text("hello world"),
                Text("I am Jack")
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              textDirection: TextDirection.rtl,
              children: <Widget>[
                Text("hello world"),
                Text("I am Jack")
              ],
            ),
            Row(
              verticalDirection: VerticalDirection.up,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: <Widget>[
                Text(" hello world ", style: TextStyle(fontSize: 30.0),),
                Text("I am Jack")
              ],
            )
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment test',
        child: Icon(Icons.add),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
  ...
  ...
```

![](https://raw.githubusercontent.com/mianli/mianli.GitHub.io/master/_posts/images/test1.png)

Row和Column类似，只不过主轴和纵轴概念交换了。

> Row嵌套Row或者Column嵌套Column，那么只有外层的Row或Column尽可能的占用最大空间，内部的则为实际大小。

