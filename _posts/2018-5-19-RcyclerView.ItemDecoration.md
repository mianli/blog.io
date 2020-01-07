
---
layout: post
title: RcyclerView.ItemDecoration
date: 2018-05-19
categories: blog
tags: Java
description: Java基础
---


# RcyclerView.ItemDecoration

RecyclerView.ItemDecoration有三个重要的方法：
1. onDraw(Canvas c, RecyclerView parent, State state)

> onDraw可以给RecyclerView item绘制合适的装饰内容，这些绘制的内容会在item views绘制之前进行，并且是绘制在item views的底层的

2. onDrawOver(Canvas c, RecyclerView parent, State state)

> onDrawOver 它和onDraw的区别是绘制在item views之后，并且绘制在item views之上

3. getItemOffsets(Rect outRect, View view, RecyclerView parent, State state)

> getItemOffsets方法可以控制每一个Item中的offset，outRect参数指定了item和四周的间距(单位为px)，相当于padding或margin。

它们都会在recyclerView滑动过程中不断地被调用
，下面的代码会给纵向的RecyclerView绘制divider
```
public class DividerItemDecoration extends RecyclerView.ItemDecoration {

    private int dividerHeight;
    private Paint dividerPaint;

    public DividerItemDecoration(int dividerHeight, int dividerColor) {
        this.dividerHeight = dividerHeight;

        dividerPaint = new Paint();
        dividerPaint.setColor(dividerColor);
    }

    @Override
    public void getItemOffsets(Rect outRect, View view, RecyclerView parent, RecyclerView.State state) {
        super.getItemOffsets(outRect, view, parent, state);
        outRect.bottom = dividerHeight;
    }

    @Override
    public void onDraw(Canvas c, RecyclerView parent, RecyclerView.State state) {
        super.onDraw(c, parent, state);
        int childCount = parent.getChildCount();
        int left = parent.getPaddingLeft();
        int right  = parent.getWidth() - parent.getPaddingRight();

        for (int i = 0; i < childCount; i++) {
            View view = parent.getChildAt(i);
            int top = view.getBottom();
            int bottom = view.getBottom() + dividerHeight;

            c.drawRect(new Rect(left, top, right, bottom), dividerPaint);
        }
    }
}
```
从应用的角度来说，在某些时候的onDraw或者onDrawOver效果都是差不多的。但是有些时候则有一些差别：

```
public class CoverItemDecoration extends RecyclerView.ItemDecoration {

    private Paint mPaint;
    private int mColor;
    private int mCoverWidth;
    private int mDividerHeight;

    public CoverItemDecoration() {
        mColor = Color.GRAY;
        mCoverWidth = 100;
        mDividerHeight = 2;

        mPaint = new Paint();
        mPaint.setColor(mColor);
        mPaint.setStyle(Paint.Style.FILL);
    }

    @Override
    public void getItemOffsets(Rect outRect, View view, RecyclerView parent, RecyclerView.State state) {
        super.getItemOffsets(outRect, view, parent, state);
        outRect.bottom = mDividerHeight;//底部间隔
    }

    @Override
    public void onDrawOver(Canvas c, RecyclerView parent, RecyclerView.State state) {
        super.onDrawOver(c, parent, state);
        //这里会直接绘制在itemView之上，覆盖一部分itemView
        for (int i = 0; i < parent.getChildCount(); i++) {
            View view = parent.getChildAt(i);
            if(needCover(parent.getChildAdapterPosition(view))) {
                c.drawRect(new Rect(view.getLeft(), view.getTop(),
                        view.getLeft() + mCoverWidth, view.getBottom()), mPaint);
            }else {

            }
            c.drawRect(new Rect(view.getLeft(), view.getBottom(), view.getRight(), view.getBottom() + mDividerHeight), mPaint);
        }
    }

    private boolean needCover(int position) {
        return position % 5 == 0;
    }

}

```
效果图：

![](https://raw.githubusercontent.com/mianli/-/master/recyclerview/decoration_ondrawover.png)

下方代码实现了RecyclerView横向或者横向都可以设置divider的功能：


```
public class LSDividerItemDecoration extends RecyclerView.ItemDecoration {

    //只支持一行的RecyclerView之间的间隔
    public static final int HORIZONTAL_LIST = LinearLayoutManager.HORIZONTAL;

    public static final int VERTICAL_LIST = LinearLayoutManager.VERTICAL;

    @IntDef({HORIZONTAL_LIST, VERTICAL_LIST})
    @Retention(RetentionPolicy.SOURCE)
    public @interface Oriention {}

    private int mDividerLength;

    private int mDividerLengthBound;

    private @Oriention int mOrientation;
    private int mColor;

    //需要显示的总数量
    private int mTotalSize;
    //第一个item前面是否有间隔
    private boolean mExceptstart;
    //最后一个item后面是否有间隔
    private boolean mExceptEnd;

    private Paint mPaint;

    public LSDividerItemDecoration(@Oriention int orientation, int dividerLength, @ColorInt int color) {
        if(orientation != HORIZONTAL_LIST && orientation != VERTICAL_LIST) {
            throw new IllegalArgumentException("orientaion设置错误");
        }
        this.mOrientation = orientation;
        this.mDividerLength = orientation == HORIZONTAL_LIST ?
                Global.var.scaler.scaleY(dividerLength) : Global.var.scaler.scaleX(dividerLength);
        this.mDividerLengthBound = mDividerLength;
        this.mColor = color;
        mPaint = new Paint();
        mPaint.setColor(mColor);
        mPaint.setStyle(Paint.Style.FILL);
    }

    /**
     * @param boundHalf 如果exceptStart或exceptEnd为false，最前面或者最后面的item的间隔是否只显示一半
     * @return
     */
    public LSDividerItemDecoration withConfig(int totalSize, boolean exceptstart, boolean exceptEnd,
                                              boolean boundHalf) {
        mTotalSize = totalSize;
        this.mExceptstart = exceptstart;
        this.mExceptEnd = exceptEnd;
        if(boundHalf) {
            mDividerLengthBound = mDividerLength / 2;
        }
        return this;
    }

    @Override
    public void getItemOffsets(Rect outRect, View view, RecyclerView parent, RecyclerView.State state) {
        super.getItemOffsets(outRect, view, parent, state);
        if(mOrientation == VERTICAL_LIST) {

            outRect.bottom = mDividerLength;

            int position = parent.getChildAdapterPosition(view);
            if(position == 0) {
                if(mExceptstart) {
                    outRect.top = 0;
                }else {
                    outRect.top = mDividerLengthBound;
                }
            }else if(position == mTotalSize - 1){
                if(mExceptEnd) {
                    outRect.bottom = 0;
                }else {
                    outRect.bottom = mDividerLengthBound;
                }
            }

        }else {

            outRect.right = mDividerLength;

            int position = parent.getChildAdapterPosition(view);
            if(position == 0) {
                if(mExceptstart) {
                    outRect.left = 0;
                }else {
                    outRect.left = mDividerLengthBound;
                }
            }else if(position == mTotalSize - 1){
                if(mExceptEnd) {
                    outRect.right = 0;
                }else {
                    outRect.right = mDividerLengthBound;
                }
            }
        }
    }

    @Override
    public void onDraw(Canvas c, RecyclerView parent, RecyclerView.State state) {
        super.onDraw(c, parent, state);

        if(mColor == Color.TRANSPARENT) {
            return;
        }
        for (int i = 0; i < parent.getChildCount(); i++) {
            View child = parent.getChildAt(i);
            int position = parent.getChildAdapterPosition(child);
            if(mOrientation == VERTICAL_LIST) {
                if(position == 0) {
                    if(!mExceptstart) {
                        c.drawRect(new Rect(parent.getPaddingLeft(), child.getTop() - mDividerLengthBound,
                                parent.getPaddingRight(), child.getTop()), mPaint);
                    }
                    c.drawRect(new Rect(parent.getPaddingLeft(), child.getBottom(),
                            parent.getPaddingRight(), child.getBottom() + mDividerLength), mPaint);
                }else if(position == mTotalSize - 1){
                    if(!mExceptEnd) {
                        c.drawRect(new Rect(parent.getPaddingLeft(), child.getBottom(),
                                parent.getPaddingRight(), child.getBottom() + mDividerLengthBound), mPaint);
                    }
                }else {
                    c.drawRect(new Rect(parent.getPaddingLeft(), child.getBottom(),
                            parent.getPaddingRight(), child.getBottom() + mDividerLength), mPaint);
                }

            }else {
                if(position == 0) {
                    if(!mExceptstart) {
                        c.drawRect(new Rect(child.getLeft() - mDividerLengthBound,
                                child.getTop(), child.getLeft(), child.getBottom()), mPaint);
                    }
                    c.drawRect(new Rect(child.getRight(), child.getTop(),
                            child.getRight() + mDividerLength, child.getBottom()), mPaint);
                }else if(position == mTotalSize - 1){
                    if(!mExceptEnd) {
                        c.drawRect(new Rect(child.getRight(), child.getTop(),
                                child.getRight() + mDividerLengthBound, child.getBottom()), mPaint);
                    }
                }else {
                    c.drawRect(new Rect(child.getRight(), child.getTop(),
                            child.getRight() + mDividerLength, child.getBottom()), mPaint);
                }
            }
        }
    }
}
```