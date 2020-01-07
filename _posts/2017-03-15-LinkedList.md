---
layout: post
title: LinkedList
date: 2017-03-15
categories: blog
tags: Java
description: Java基础
---

# LinkedList

ArrayList是基于可变大小的数组，而LinkedList是基于双向链表串联。

Java的LinkedList是一种常用的数据容器，与ArrayList相比，LinkedList的增删操作效率更高，而查改操作效率较低。

LinkedList 实现了List 接口，能对它进行列表操作。

LinkedList 实现了Deque 接口，即能将LinkedList当作双端队列使用。

LinkedList 实现了Cloneable接口，能克隆。

LinkedList 实现了java.io.Serializable接口，这意味着LinkedList支持序列化，能通过序列化去传输。

## LinkedList和ArrayList的区别

- 因为Array是基于索引(index)的数据结构，它使用索引在数组中搜索和读取数据是很快的。Array获取数据的时间复杂度是O(1),但是要删除数据却是开销很大的，因为这需要重排数组中的所有数据。

- 相对于ArrayList，LinkedList插入是更快的。因为LinkedList不像ArrayList一样，不需要改变数组的大小，也不需要在数组装满的时候要将所有的数据重新装入一个新的数组，这是ArrayList最坏的一种情况，时间复杂度是O(n)，而LinkedList中插入或删除的时间复杂度仅为O(1)。ArrayList在插入数据时还需要更新索引（除了插入数组的尾部）。

- 类似于插入数据，删除数据时，LinkedList也优于ArrayList。

- LinkedList需要更多的内存，因为ArrayList的每个索引的位置是实际的数据，而LinkedList中的每个节点中存储的是实际的数据和前后节点的位置。