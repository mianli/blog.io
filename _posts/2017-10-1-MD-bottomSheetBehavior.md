---
layout: post
title: MD之BottomSheetBehavior
date: 2017-10-01
categories: blog
tags: MD
description: MD设计
---


### BottomSheetBehavior
对于Behavior来讲，父布局一定要有CoordinatorLayout，BottomSheetBehavior也不例外。首先先创建一个简单的布局：

```
<android.support.design.widget.CoordinatorLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    xmlns:app="http://schemas.android.com/apk/res-auto">

    <android.support.design.widget.AppBarLayout
        android:layout_width="match_parent"
        android:layout_height="?attr/actionBarSize">

        <android.support.v7.widget.Toolbar
            android:id="@+id/bottom_sheet_toolbar"
            android:layout_width="match_parent"
            android:layout_height="match_parent">
        </android.support.v7.widget.Toolbar>

    </android.support.design.widget.AppBarLayout>

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        app:layout_behavior="@string/appbar_scrolling_view_behavior"
        android:gravity="center"
        android:layout_marginBottom="?attr/actionBarSize"
        android:orientation="vertical">

        <Button
            android:id="@+id/bottom_sheet_hiden_show_switch_btn"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="sheet 显示/隐藏"/>

        <Button
            android:id="@+id/bottom_sheet_dialog_ctr_btn"
            android:layout_marginTop="5dp"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="显示/隐藏 dialog"/>

    </LinearLayout>

    <!--app:behavior_hideable="true"一定要设置-->
    <LinearLayout
        android:id="@+id/bottom_sheet_container"
        android:layout_width="match_parent"
        app:behavior_hideable="true"
        android:layout_height="?attr/actionBarSize"
        app:layout_behavior="@string/bottom_sheet_behavior"
        android:background="@color/colorAccent">

        <Button
            android:layout_width="0dp"
            android:layout_weight="1"
            android:layout_height="match_parent" />

        <Button
            android:layout_width="0dp"
            android:layout_weight="1"
            android:layout_height="match_parent" />

        <Button
            android:layout_width="0dp"
            android:layout_weight="1"
            android:layout_height="match_parent" />

        <Button
            android:layout_width="0dp"
            android:layout_weight="1"
            android:layout_height="match_parent" />

    </LinearLayout>

</android.support.design.widget.CoordinatorLayout>
```

BottomSheetBehavior有几个状态：

```
/**
 * The bottom sheet is dragging.
 */
public static final int STATE_DRAGGING = 1;

/**
 * The bottom sheet is settling.
 */
public static final int STATE_SETTLING = 2;

/**
 * The bottom sheet is expanded.
 */
public static final int STATE_EXPANDED = 3;

/**
 * The bottom sheet is collapsed.
 */
public static final int STATE_COLLAPSED = 4;

/**
 * The bottom sheet is hidden.
 */
public static final int STATE_HIDDEN = 5;
```

我们可以通过控制BottomSheetBehavior的状态来控制底部View的显示和隐藏。BottomSheetBehavior有一个可以从View中获取实例的方法：BottomSheetBehavior.from(View)：

```
/**
 * A utility function to get the {@link BottomSheetBehavior} associated with the {@code view}.
 *
 * @param view The {@link View} with {@link BottomSheetBehavior}.
 * @return The {@link BottomSheetBehavior} associated with the {@code view}.
 */
@SuppressWarnings("unchecked")
public static <V extends View> BottomSheetBehavior<V> from(V view) {
    ViewGroup.LayoutParams params = view.getLayoutParams();
    if (!(params instanceof CoordinatorLayout.LayoutParams)) {
        throw new IllegalArgumentException("The view is not a child of CoordinatorLayout");
    }
    CoordinatorLayout.Behavior behavior = ((CoordinatorLayout.LayoutParams) params)
            .getBehavior();
    if (!(behavior instanceof BottomSheetBehavior)) {
        throw new IllegalArgumentException(
                "The view is not associated with BottomSheetBehavior");
    }
    return (BottomSheetBehavior<V>) behavior;
}
```
看，如果这个View的根布局不是一个CoordinatorLayout将抛出异常。

于是我们先获取这个behavior:

```
mBottomSheetBehavior = BottomSheetBehavior.from(findViewById(R.id.bottom_sheet_container));
```

但是布局中底部View明明是默认显示的啊，我们需要给它设置一个初识的状态：

```
//mBottomSheetBehavior.setHideable(true);
mBottomSheetBehavior.setState(BottomSheetBehavior.STATE_HIDDEN);
```
注意，如果在xml中在用BottomSheetBehavior的地方没有使用**app:behavior_hideable="true"**，将无法达到隐藏和显示的效果。或者通过Java代码的方式设置：
```
mBottomSheetBehavior.setHideable(true);
```
官方给出的解释是：
*Sets whether this bottom sheet can hide when it is swiped down.*，已经描述的很明显了。

![](https://raw.githubusercontent.com/mianli/-/master/md/md_bottomsheet_behavior1.gif)

通过BottomSheetBehavior的源码可以看到，其state默认为STATE_COLLAPSED。你可以通过**setPeekHeight**设置STATE_COLLAPSED状态时的高度。

```
mBottomSheetBehavior.setPeekHeight(500);
```

你会看到其实还有一种设置：**setSkipCollapsed**，跳过STATE_COLLAPSED状态：

```
mBottomSheetBehavior.setHideable(true);
mBottomSheetBehavior.setSkipCollapsed(true);
mBottomSheetBehavior.setState(BottomSheetBehavior.STATE_COLLAPSED);
mBottomSheetBehavior.setPeekHeight(500);
```

![](https://raw.githubusercontent.com/mianli/-/master/md/md_bottomsheet_behavior_skipcollapsed.gif)

注意，此时setHideable必须也设置为true，否则setSkipCollapsed将无效。因为BottomSheetBehavior默认是没有Hiden状态的，这个状态必须由我们主动去设置才会有，所以当没有这个状态即它不能隐藏的时候，跳过折叠状态后会是什么状态？当然还是原来的状态，因为不能隐藏啊，所以单独使用setSkipCollapsed是没有什么作用的。这一点跟可以通过原来得出结论：源码中唯有**shouldHide**这个方法用到了mSkipCollapsed，而**shouldHide**在整个源码中都是配合mHideable一块使用的：**mHideable && shouldHide**

然后通过状态判断控制其显示或者隐藏即可：

```
if(mBottomSheetBehavior.getState() == BottomSheetBehavior.STATE_EXPANDED) {
    mBottomSheetBehavior.setState(BottomSheetBehavior.STATE_HIDDEN);
}else if(mBottomSheetBehavior.getState() == BottomSheetBehavior.STATE_HIDDEN) {
    mBottomSheetBehavior.setState(BottomSheetBehavior.STATE_EXPANDED);
}
```
### BottomSheetDialog

我们可以通过BottomSheetDialog的setContentView来自定义其中的内容显示。比如当我们初始化一个BottomSheetDialog的时候，可以像初始化普通的Dialog一样，这里用一个RecyclerView示例：

```
View view = getLayoutInflater().inflate(R.layout.recyclerview, null, false);
RecyclerView rcv = view.findViewById(R.id.recyclerview);
rcv.setLayoutManager(new LinearLayoutManager(this));
rcv.setNestedScrollingEnabled(false);
final List<Integer> list = new ArrayList<>();
for (int i = 0; i < 30; i++) {
    list.add(i);
}
rcv.setAdapter(new RcvAdapter(list));

mBottomSheetDialog = new BottomSheetDialog(this);
mBottomSheetDialog.setContentView(view);
```

然后就可以通过Dialog都有的方法show和dismiss来进行显示和隐藏了：

```
if(mBottomSheetDialog.isShowing()) {
    mBottomSheetDialog.dismiss();
}else {
    mBottomSheetDialog.show();
}
```

![](https://raw.githubusercontent.com/mianli/-/master/md/md_bottomsheet_behavior_dialog.gif)