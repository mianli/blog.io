

参考：
https://blog.csdn.net/mffandxx/article/details/69223021
https://www.jianshu.com/p/7caa5f4f49bd

CoordinatorLayout可以结合AppbarLayout、CollapsingToobarLayout等控件可以产生各种酷炫的效果。

#### 结合FloatActionButton

```
<?xml version="1.0" encoding="utf-8"?>
<android.support.design.widget.CoordinatorLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <android.support.design.widget.FloatingActionButton
        android:id="@+id/floatactionbtn"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="bottom|right"
        android:src="@android:drawable/ic_input_add"
        android:layout_margin="8dp"/>

</android.support.design.widget.CoordinatorLayout>
```
这种用法很简单，只要讲coordinatorLayout当做一个普通的FrameLayout就行了。如果这个时候再结合SnackBar会是什么效果呢？
直接给FloatActionButton添加点击事件：

```
FloatingActionButton fab = findViewById(R.id.floatactionbtn);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Snackbar.make(v, "显示一个snackbar", Snackbar.LENGTH_LONG).show();
            }
        });
```
![](https://raw.githubusercontent.com/mianli/-/master/coodinatorLayout%2BFloatActionButton.gif)
#### 结合AppBarLayout
AppBarLayout继承自LinearLayout，默认方向为Vertical      

- AppBarLayout继承自LinearLayout，它是为MD风格而设计的AppBar，它的作用是将AppBarLayout包裹的内容作为AppBar。它就是为了和CoordinatorLayout搭配使用的，实现一些MD风格的UI，没有CoordinatorLayout，它和LinearLayout没有区别。

- AppBarLayout有一个属性：app:layout_scrollFlags，这个属性有五种Flags:scroll、enterAlways、enterAlwaysCollapsed、snap、exitUtilCollapsed

1. scroll   
伴随着滚动事件而滚出或滚进屏幕

> **如果使用了其他值，必须要使用这个常量值才会起作用；    
如果在这个ChildView前面的任何其他的ChildView没有设置该值，那么这个ChildView的设置将会失去作用。**

```
<?xml version="1.0" encoding="utf-8"?>
<android.support.design.widget.CoordinatorLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <android.support.design.widget.AppBarLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content">

        <android.support.v7.widget.Toolbar
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            app:title="title"
            app:layout_scrollFlags="scroll">
        </android.support.v7.widget.Toolbar>
    </android.support.design.widget.AppBarLayout>

    <android.support.v4.widget.NestedScrollView
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        app:layout_behavior="@string/appbar_scrolling_view_behavior">

        <android.support.v7.widget.RecyclerView
            android:id="@+id/rcv"
            android:layout_width="match_parent"
            android:layout_height="match_parent">
        </android.support.v7.widget.RecyclerView>


    </android.support.v4.widget.NestedScrollView>

</android.support.design.widget.CoordinatorLayout>
```
![](https://raw.githubusercontent.com/mianli/-/master/coodinatorLayout%2BappbarLayout_scroll.gif)

2.enterAlways  

快速返回模式。只要向上滚动该布局就会向上收缩，只要向下滚动该布局就会显示。  

```
...
app:layout_scrollFlags="scroll|enterAlways"
...
```
![](https://raw.githubusercontent.com/mianli/-/master/coodinatorLayout%2BappbarLayout_scrollenterAlways.gif)

3.enterAlwaysCollapsed     

- 它和scroll单独结合使用的时候，只有在向下滑动到顶部的时候该布局才会显示   

```
...
app:layout_scrollFlags="scroll|enterAlwaysCollapsed"
...
```
![](https://raw.githubusercontent.com/mianli/-/master/coodinatorLayout%2BappbarLayout_scroll_enterAlwayCollapsed.gif)

- 其实它可以作为enterAlwalys的附加值，这涉及到ChildView的高度和最小高度。向下滚动时，ChildView会先向下滚动一个最小高度，当到达边界即滚动到NestedScrollView的顶端时，继续才会继续完全显示      

```
...
android:layout_height="50dp"
android:minHeight="25dp"
app:layout_scrollFlags="scroll|enterAlways|enterAlwaysCollapsed"
...
```
![](https://raw.githubusercontent.com/mianli/-/master/coodinatorLayout%2BappbarLayout_scroll_enterAlwayCollapsed_with_minHeight.gif)

4.exitUtilCollapsed        
这个也涉及最小高度。发生滚动时，ChildView向上滚动退出直至最小高度，然后ScorllView开始滚动。即不会完全退出屏幕。

```
...
android:layout_height="?attr/actionBarSize"
android:minHeight="20dp"
app:layout_scrollFlags="scroll|exitUntilCollapsed"
...
```
![](https://raw.githubusercontent.com/mianli/-/master/coodinatorLayout%2BappbarLayout_scroll_exitUntilCollapsed_with_minHeight.gif)

5.snap      
childView滚动比例的一个吸附效果。也就是说，ChildView不会存在局部显示的情况，滚动Child View的部分高度，当我们松开手指时，ChildView要么向上全部滚出屏幕，要么向下全部滚进屏幕

```
...
android:layout_height="200dp"
app:layout_scrollFlags="scroll|snap"
...
```
![](https://raw.githubusercontent.com/mianli/-/master/coodinatorLayout%2BappbarLayout_scroll_snap.gif)

> 在AppBarLayout容器内不仅仅只能添加AppBar才会得到上面的效果，可以尝试添加其他的View，同时给这个View也增加app:layout_scrollFlags，那么它一样会产生相同的效果

注意有这样一个属性不可或缺：app:layout_behavior="@string/appbar_scrolling_view_behavior"，它表明是要把自己放到AppBarLayout下面，可以试试去掉这一行——将不再会得到以上的效果，取而代之的是一种ScrollView没有依附appBarLayout的效果。

#### 和CollapsingToolbarLayout
CollapseingToolbarLayout是提供一个可折叠的ToolBar，它继承自FrameLayout。

```
<?xml version="1.0" encoding="utf-8"?>
<android.support.design.widget.CoordinatorLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:fitsSystemWindows="true">

    <android.support.design.widget.AppBarLayout
        android:id="@+id/appbar_layout"
        android:layout_width="match_parent"
        android:layout_height="wrap_content">

        <android.support.design.widget.CollapsingToolbarLayout
            android:layout_width="match_parent"
            android:layout_height="200dp"
            app:contentScrim="?attr/colorPrimary"
            app:layout_scrollFlags="scroll|exitUntilCollapsed"
            app:title="标题">

            <ImageView
                android:layout_width="match_parent"
                android:layout_height="match_parent"
                android:background="@drawable/chenglong" />

            <android.support.v7.widget.Toolbar
                android:layout_width="match_parent"
                android:layout_height="50dp"
                android:background="#74389174"
                app:title="title">

            </android.support.v7.widget.Toolbar>

        </android.support.design.widget.CollapsingToolbarLayout>

    </android.support.design.widget.AppBarLayout>

    <android.support.v4.widget.NestedScrollView
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        app:layout_behavior="@string/appbar_scrolling_view_behavior">
        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="match_parent"
            android:orientation="vertical">

            <View
                android:layout_width="match_parent"
                android:layout_height="300dp"
                android:background="@color/colorAccent"/>

            <View
                android:layout_width="match_parent"
                android:layout_height="300dp"
                android:background="@color/colorPrimary"/>

            <View
                android:layout_width="match_parent"
                android:layout_height="300dp"
                android:background="@color/colorPrimaryDark"/>

        </LinearLayout>
    </android.support.v4.widget.NestedScrollView>

    <android.support.design.widget.FloatingActionButton
        android:id="@+id/fab"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_margin="30dp"
        app:layout_anchor="@id/appbar_layout"
        app:layout_anchorGravity="bottom|right"
        app:srcCompat="@android:drawable/ic_dialog_email" />

</android.support.design.widget.CoordinatorLayout>
```
> 包含关系：AppbarLayout->CollapsingToolbarLayout->ToolBar

只要CollapsingAppbarlayout里面包含ToolBar，那么CollapsingAppbarLayout折叠后的高度就是Toolbar的高度，相当于CollapsingAppbarLayout设置了minHeight属性。

app:layout_collapseMode表示折叠模式，它是CollapsingToolbarLayout子控件需要直接设置的。它有3种设置情况：
1.不设置：会跟随NestedScrollView的滑动一起滑动，NestedScrollView滑动多少距离，它就跟随着滑动多少距离。

![](https://raw.githubusercontent.com/mianli/-/master/coodinatorLayout%2BcollapsingToolbarLayout_none.gif)

2.pin：在滑动过程中会固定在它所在的位置不动，直到CollapsingAppbarLayout全部折叠或展开。

```
<android.support.v7.widget.Toolbar
    android:layout_width="match_parent"
    android:layout_height="50dp"
    android:background="#74389174"
    app:layout_collapseMode="pin"
    app:title="title">
</android.support.v7.widget.Toolbar>
```
![](https://raw.githubusercontent.com/mianli/-/master/coodinatorLayout%2BcollapsingToolbarLayout_pin.gif)

3.parallax：视差效果。可以和layout_collapseParallaxMultipier(*取值为0~1*)配合使用。

```
<android.support.v7.widget.Toolbar
    android:layout_width="match_parent"
    android:layout_height="50dp"
    android:background="#74389174"
    app:layout_collapseMode="parallax"
    app:layout_collapseParallaxMultiplier="0.5"
    app:title="title">
</android.support.v7.widget.Toolbar>
```
![](https://raw.githubusercontent.com/mianli/-/master/coodinatorLayout%2BcollapsingToolbarLayout_collapseMode.gif)

> 注意其中配合FloatActionButton一起使用的效果