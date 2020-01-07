

# ArrayList

ArrayList底层是使用数组实现的，里面有个类属性：*elementData*    
它有三个构造方法：
- ArrayList()
- ArrayList(int initialCapacity)
- ArrayList(Collection<? extends E> c)

第一个构造函数中会默认给定一个空数组。

```
private static final Object[] DEFAULTCAPACITY_EMPTY_ELEMENTDATA = {};
...
public ArrayList() {
    this.elementData = DEFAULTCAPACITY_EMPTY_ELEMENTDATA;
}

```

第二个构造方法可以指定一个数组的空间大小：

```
private static final Object[] EMPTY_ELEMENTDATA = {};
...
public ArrayList(int initialCapacity) {
    if (initialCapacity > 0) {
        this.elementData = new Object[initialCapacity];
    } else if (initialCapacity == 0) {
        this.elementData = EMPTY_ELEMENTDATA;
    } else {
        throw new IllegalArgumentException("Illegal Capacity: "+
                                           initialCapacity);
    }
}
```

当然如果你指定的这个空间大小为0，它也会创建一个空数组。

第三个构造方法可以给定一个集合

```
public ArrayList(Collection<? extends E> c) {
    elementData = c.toArray();
    if ((size = elementData.length) != 0) {
        // c.toArray might (incorrectly) not return Object[] (see 6260652)
        if (elementData.getClass() != Object[].class)
            elementData = Arrays.copyOf(elementData, size, Object[].class);
    } else {
        // replace with empty array.
        this.elementData = EMPTY_ELEMENTDATA;
    }
}
```

如果给定的这个集合大小不为0，ArrayList将会创建一个同样大小的数组，并且将集合中的所有数据复制到新创建的数组当中。如果给定的集合大小为0，会创建一个空数组。

那ArrayList是如何进行扩容的呢？
因为在默认构造方法中，仅仅是创建了一个空的数组，所以这在内存上占据了比较小的一个空间。但是在增加数据时会动态的进行扩容。

```
public boolean add(E e) {
    ensureCapacityInternal(size + 1);  // Increments modCount!!
    elementData[size++] = e;
    return true;
}
...
private void ensureCapacityInternal(int minCapacity) {
    if (elementData == DEFAULTCAPACITY_EMPTY_ELEMENTDATA) {
        minCapacity = Math.max(DEFAULT_CAPACITY, minCapacity);
    }

    ensureExplicitCapacity(minCapacity);
}
...
private void ensureExplicitCapacity(int minCapacity) {
    modCount++;

    // overflow-conscious code
    if (minCapacity - elementData.length > 0)
        grow(minCapacity);
}
private void grow(int minCapacity) {
    // overflow-conscious code
    int oldCapacity = elementData.length;
    int newCapacity = oldCapacity + (oldCapacity >> 1);
    if (newCapacity - minCapacity < 0)
        newCapacity = minCapacity;
    if (newCapacity - MAX_ARRAY_SIZE > 0)
        newCapacity = hugeCapacity(minCapacity);
    // minCapacity is usually close to size, so this is a win:
    elementData = Arrays.copyOf(elementData, newCapacity);
}
```

在add方法中，首先会检测是否为使用了默认的构造方法，即数组是否为DEFAULTCAPACITY_EMPTY_ELEMENTDATA，如果是则将数组进行动态扩容，或者说增长数组容量。之后会将取默认大小：DEFAULT_CAPACITY，DEFAULT_CAPACITY的值为**10**。但是这个并不是最终创建数组的大小。在之后会通过一个算法：

```
int newCapacity = oldCapacity + (oldCapacity >> 1);
```
即会在旧大小（初始时为默认大小，即DEFAULT_CAPACITY的值为），最终结果为15。不仅仅如此，其实每次扩容的时候都将会按照此算法进行扩容，且根据以上代码可见，扩容长度为旧长度的1.5倍。

再看remove方法：

```
public E remove(int index) {
    if (index >= size)
        throw new IndexOutOfBoundsException(outOfBoundsMsg(index));

    modCount++;
    E oldValue = (E) elementData[index];

    int numMoved = size - index - 1;
    if (numMoved > 0)
        System.arraycopy(elementData, index+1, elementData, index,
                         numMoved);
    elementData[--size] = null; // clear to let GC do its work

    return oldValue;
}
```

当进行remove操作的时候，会将所删除的索引位置之后的数据进行移动。代码中见：

```
System.arraycopy(elementData, index+1, elementData, index,
                         numMoved);
```

可见，其效率并不高，唯一可说的是copy方式使用了Java底层的复制方式。