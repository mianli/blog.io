---
layout: post
title: ConstaintLayout
date: 2018-05-26
categories: blog
tags: Java
description: Java基础
---


# ConstaintLayout

> 在约束布局中不能有相互依赖关系

### 相对定位

相对定位在约束布局中是基础的一个模块，这类约束可以使指定的一个控件依赖于另一个控件，你可以约束一个控件在横向或者纵向上。

横向可以约束left,right,start以及end。纵向可以约束top,bottom,text baseline。
一般情况是约束一个控件的一个边到另一个控件的一个边，比如：
![](https://developer.android.google.cn/reference/android/support/constraint/resources/images/relative-positioning.png)

```
<Button
    android:id="@+id/button_a"
    android:text="a"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content" />

<Button
    android:id="@+id/button_b"
    android:text="b"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    app:layout_constraintLeft_toRightOf="@+id/button_a"/>
```

诸如此类的还有如下种类的约束方式：
- layout_constraintLeft_toLeftOf
- layout_constraintLeft_toRightOf
- ...
- layout_constraintEnd_toStartOf
- layout_constraintEnd_toEndOf
上述的约束方式均需要一个指定控件的id或者parent(即该指定控件的父布局，这个父布局一定是constraintlayout)

如果控件之间需要间距，通常使用的margin属性就可以达到效果：
- android:layout_marginStart
- android:layout_marginEnd
- ...

> 注意margin值必须为非负数

#### 给GONE属性的控件设置间距

如果你想给一个依赖于另一个设置为GONE属性的控件B的控件A之间设置一个间距，但是在B显示之后这个间距将取消，那么可以使用layout_goneMargin：

- layout_goneMarginStart
- layout_goneMarginEnd
- ...

这种layout_goneMargin\*和layout_margin\*之间的区别是，layout_goneMargin\*在另一个被设置为View.GONE的控件显示之后，被设置的margin将取消，而layout_margin\*会一直有与另一个控件保持指定的margin大小。

#### 居中定位

```
<android.support.constraint.ConstraintLayout ...>
         <Button android:id="@+id/button" ...
             app:layout_constraintLeft_toLeftOf="parent"
             app:layout_constraintRight_toRightOf="parent/>
     </>
```

上述代码约束button左侧约束于父布局左侧，右侧约束于父布局右侧，除非Button的宽度足以满足这个父布局，否则这个条件是无法满足的。那么此时，按钮将显示在父布局左右居中的位置。其他居中约束也是类似。

如果一个控件已经居中，但是你想对它进行进行某些偏移，可以使用一下属性：

- layout_constraintHorizontal_bias
- layout_constraintVertical_bias

![](https://developer.android.google.cn/reference/android/support/constraint/resources/images/centering-positioning-bias.png)

比如你想对左右居中的控件A进行左偏移30%而不是居中的50%。

```
<android.support.constraint.ConstraintLayout ...>
         <Button android:id="@+id/button" ...
             app:layout_constraintHorizontal_bias="0.3"
             app:layout_constraintLeft_toLeftOf="parent"
             app:layout_constraintRight_toRightOf="parent/>
     </>
     
```

#### 圆形定位

你可以根据一个控件的中心,设置角度和距离来约束另一个控件的位置，相关的属性为：
- layout_constraintCircle:   关联另一个控件id
- layout_constraintCircleRadius： 与另一个控件的距离
- layout_constraintCircleAngle：控件所在角度（0~360）

![](https://developer.android.google.cn/reference/android/support/constraint/resources/images/circle1.png)
![](https://developer.android.google.cn/reference/android/support/constraint/resources/images/circle2.png)

```
<Button android:id="@+id/buttonA" ... />
<Button android:id="@+id/buttonB" ...
  app:layout_constraintCircle="@+id/buttonA"
  app:layout_constraintCircleRadius="100dp"
  app:layout_constraintCircleAngle="45" />
     
```

#### 尺寸约束

android:layout_width 和 android:layout_height 有三种属性：
- 指定大小
- WRAP_CONTENT 自适应大小
- 0dp相当于MATCH_CONSTRAINT
> match_parent并不推荐使用，在约束布局中可以设置left/right,top/bottom并设置为parent，因此就是填充父容器。

#### WRAP_CONTENT的强制约束

wrap_content如果内容过大，导致超出约束的边界，此时约束将失效。通过设置一下属性可以进行控制：
- app:layout_constrainedWidth=”true|false”
- app:layout_constrainedHeight=”true|false”

默认为false，ture表示强制约束。

#### MATCH_CONSTRAINT的尺寸 

当设置为MATCH_CONSTRAIT时，控件的最终大小就是可用空间大小，有一下属性可以设置：

- layout_constraintWidth_min and layout_constraintHeight_min : will set the minimum size for this dimension
- layout_constraintWidth_max and layout_constraintHeight_max : will set the maximum size for this dimension
- layout_constraintWidth_percent and layout_constraintHeight_percent : will set the size of this dimension as a percentage of the parent

#### 百分比尺寸

- 使用百分比大小，宽度值必须设置为0dp
- 使用app:layout_constraintWidth_default="percent"或者app:layout_constraintHeight_default="percent"
- 使用layout_constraintWidth_percent 或者 layout_constraintHeight_percent ，值为0~1

> app:layout_constraintWidth_default=""或者app:layout_constraintHeight_default=""的值可以为wrap_content、spread、percent。spread相当于match_constraint


你可以定义宽高比，在此之前必须设置宽或高至少一个为0dp，然后指定layout_constraintDimensionRatio值。

```
<Button android:layout_width="wrap_content"
       android:layout_height="0dp"
       app:layout_constraintDimensionRatio="1:1" />

```

如果宽和高都是0dp，可以指定以某一边为标准：

```
<Button android:layout_width="0dp"
   android:layout_height="0dp"
   app:layout_constraintDimensionRatio="H,16:9"
   app:layout_constraintBottom_toBottomOf="parent"
   app:layout_constraintTop_toTopOf="parent"/>
```