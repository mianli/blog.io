
---
layout: post
title: UrlConnection
date: 2017-06-08
categories: blog
tags: Java
description: Java基础
---


# UrlConnection

正在传输的类型由conyent-type加以标记。

格式：
```
http://host[":"port][abs_path]
```

端口为空默认为80；

![](http://upload-images.jianshu.io/upload_images/9028834-347fd899fccb6bf8?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

- 请求报文

1. 请求行

请求方法、URL字段、HTTP协议版本组成

```
Method Request-URI HTTP-Version CRLF
```

Method表示请求方法；        
Request-URI是一个统一资源标识符；       
HTTP-Version表示请求的HTTP协议版本；  
CRLF表示回车和换行（除了作为结尾的CRLF外，不允许出现单独的CR或LF字符）。

- 请求方法

8种：GET,POST,DELETE,PUT,HEAD,TRACE,CONNECT,OPTIONS     

    GET：请求获取Request-URI所标识的资源
    POST：在Request-URI所标识的资源后附加新的数据
    HEAD：请求获取由Request-URI所标识的资源的响应消息报头
    PUT： 请求服务器存储一个资源，并用Request-URI作为其标识
    DELETE ：请求服务器删除Request-URI所标识的资源
    TRACE ： 请求服务器回送收到的请求信息，主要用于测试或诊断
    CONNECT： HTTP/1.1协议中预留给能够将连接改为管道方式的代理服务器。
    OPTIONS ：请求查询服务器的性能，或者查询与资源相关的选项和需求


- 请求报头   

key-value形式

- 空行

请求头部会以一个空行，发送回车符和换行符，通知服务器以下不会有请求头  ？？？


- 请求数据

请求数据不再GET中使用，而是在POST中使用。POST方法适用于需要客户填写表单的场合，与请求数据相关的最常用的请求头是Content-Type和Content-Length

HTTP响应报文


![](http://upload-images.jianshu.io/upload_images/9028834-7f39dd51649f476d?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

由状态行、消息报头、空行、响应正文组成

    HTTP-Version Status-Code Reason-Phrase CRLF
    
    HTTP-Version表示服务器HTTP协议的版本；
    Status-Code表示服务器发回的响应状态代码；
    Reason-Phrase表示状态代码的文本描述。 

- 状态代码


    100~199：指示信息，表示请求已接收，继续处理
    200~299：请求成功，表示请求已被成功接收、理解、接受
    300~399：重定向，要完成请求必须进行更进一步的操作
    400~499：客户端错误，请求有语法错误或请求无法实现
    500~599：服务器端错误，服务器未能实现合法的请求

常见的状态码如下：

    200 OK：客户端请求成功
    400 Bad Request：客户端请求有语法错误，不能被服务器所理解
    401 Unauthorized：请求未经授权，这个状态代码必须和WWW-Authenticate报头域一起使用
    403 Forbidden：服务器收到请求，但是拒绝提供服务
    500 Internal Server Error：服务器发生不可预期的错误
    503 Server Unavailable：服务器当前不能处理客户端的请求，一段时间后可能恢复正常

- 通用报头

既可以出现在请求报头，也可以出现在响应报头中

    Date：表示消息产生的日期和时间
    Connection：允许发送指定连接的选项
    例如指定连接是连续的，或者指定“close”选项，通知服务器，在响应完成后，关闭连接
    Cache-Control：用于指定缓存指令，缓存指令是单向的（响应中出现的缓存指令在请求中未必会出现），且是独立的（一个消息的缓存指令不会影响另一个消息处理的缓存机制）

- 请求报头


    HOST：请求的主机名
    User-Agent：发送请求的浏览器类型、操作系统等信息
    Accept：客户端可识别的内容类型列表，用于指定客户端接收那些类型的信息
    Accept-Encoding：客户端可识别的数据编码
    Accept-Language：表示浏览器所支持的语言类型
    Connection：允许客户端和服务器指定与请求/响应连接有关的选项，例如这是为Keep-Alive则表示保持连接。
    Transfer-Encoding：告知接收端为了保证报文的可靠传输，对报文采用了什么编码方式。
    
- 响应报头
    
来自服务器

    Location：用于重定向接受者到一个新的位置，常用在更换域名的时候
    Server：包含可服务器用来处理请求的系统信息，与User-Agent请求报头是相对应的

- 实体报头
用来定义被传送资源的信息。即可用于请求也可用于响应。


    Content-Type：发送给接收者的实体正文的媒体类型
    Content-Lenght：实体正文的长度
    Content-Language：描述资源所用的自然语言，没有设置则该选项则认为实体内容将提供给所有的语言阅读
    Content-Encoding：实体报头被用作媒体类型的修饰符，它的值指示了已经被应用到实体正文的附加内容的编码，因而要获得Content-Type报头域中所引用的媒体类型，必须采用相应的解码机制。
    Last-Modified：实体报头用于指示资源的最后修改日期和时间
    Expires：实体报头给出响应过期的日期和时间

### TCP三次握手


1. 客户端随机选取一个系列号作为自己的初始序列号发送给服务器。
> 客户端发送连接请求报文段，将SYN位置为1，Sequence Number为x；然后，客户端进入SYN_SEND状态，等待服务器的确认；

2. 服务端使用ack对客户端进行确认
> 服务器收到客户端的SYN报文段，需要对这个SYN报文段进行确认，设置Acknowledgment Number为x+1(Sequence Number+1)；同时，自己自己还要发送SYN请求信息，将SYN位置为1，Sequence Number为y；服务器端将上述所有信息放到一个报文段（即SYN+ACK报文段）中，一并发送给客户端，此时服务器进入SYN_RECV状态；

3. 客户端受到服务端报文段，并确认收到消息准备建立连接
> 客户端收到服务器的SYN+ACK报文段。然后将Acknowledgment Number设置为y+1，向服务器发送ACK报文段，这个报文段发送完毕以后，客户端和服务器端都进入ESTABLISHED状态，完成TCP三次握手。

### 四次挥手

首先请求关闭连接的可以是客户端，也可以是服务端。以客户端举例。

1. 客户端发送一个FIN，用来请求关闭和服务端之间的数据发送，客户端进入**FIN_WAIT_1**状态
2. 服务端收到FIN之后，发送一个ACK给客户端，确认序号为收到序号+1，服务端进入**CLOSE_WAIT**
3. 服务端发送一个FIN，用来请求关闭和客户端之间的数据传送，服务端进入**LAST_ACK**状态。
4. 客户端收到FIN后，接着发送一个ACK给服务端，客户端进入**TIME_WAIT**状态。服务端收到客户端的ACK报文段之后就关闭连接。客户端等待2MSL后依然没有受到回复，证明服务端已经关闭连接，自己也接着关闭连接。

[TCP三次握手详解及释放连接过程](https://www.cnblogs.com/laowz/p/6947539.html)

[TCP协议中的三次握手和四次挥手](https://www.cnblogs.com/thrillerz/p/6464203.html)


URI:Uniform Resource Identifier，表示的是一个资源

URL：Uniform Recource Locator,表示的是一个地址。一般不超过2048个字节，即2kb，超过此限制浏览器可能不识别。

##### 设置连接参数

setAllowUserInteraction：设置是否允许用户交互，比如弹出一个验证对话框。

setDoInput:设置是否允许URL connection进行输入，意即允许客户端进行读取网络数据。

setDoOutPut:设置是否允许URL connection进行输出，意即允许客户端进行写网络数据。

setIfModifiedSince：有些协议支持跳过对象的获取，除非对象最近修改的超过了给定的时间。参数必须为非零值，指的是1970年1月1日的格林豪治时间以来的毫秒数。只有在对象最近被修改的时间超过（晚于）这个时间，才会获取该对象。

setUseCaches：是否允许使用cache。有些协议会缓存文档。有时，可能使用“tunnel through”和忽略缓存（比如浏览器中的重新载入）更重要一些。

HTTP请求允许设置头信息一个key带多个用逗号隔开的value。
设置请求属性，即设置头信息使用方法：==setRequestProperty==/==addRequestProperty==。二者区别在于，set方式会清除该key之前的value值，相当于重新设置，而add会在之前的value基础上继续添加header属性。

可以通过使用**setDefaultAllowUserInteraction**和**setDefaultUseCaches**设置默认的allowUserInteraction和useCaches属性。通过代码可以看到defaultAllowUserInteration和defaultUseCaches为静态属性。即可以通过该属性来设置UrlConnection默认的属性，但是可以针对独立UrlConnection分别设置不同的这两个属性。

上述的方法均有各自相应的get方法


##### 获取响应

getContent:这个方法首先通过调用getContentType方法来确定内容类型。如果这是应用程序第一次发现特定的内容类型，将会创建一个该内容类型的内容处理程序。

如果应用程序使用setContentHandlerFactory方法建立了内容处理程序工厂实例，那么该实例的createContentHandler方法将内容类型作为参数调用，结果是该内容类型的内容处理程序。

如果还没有设置内容处理程序工厂，或者工厂的createContentHandler方法返回null，那么应用程序将加载名为sun.net.www.content.<contentType>的类

getHaderField（int n ）：获取索引为n的头部信息字段的数据。可以结合getHeaderFieldKey通过迭代来获取完整的头部信息。

getInputStream：获取从网络读取的数据

getOutputStream:获取从客户端写入连接段的数据

getContentEncoding:获取头信息中的content-encoding

getContentType:获取头信息中的content-type

getDate:获取头信息中的时间

getExpiration:获取头信息中到期的时间

getLastModifed：获取最近被修改的时间

通常getContent和getInputStream是我们更关心的方法。在请求之后调用inputStream和outputStream上的close方法可以释放与此实例相关的网络资源，除非特定的协议规范为其指定了不同的行为。

##### HttpUrlConnection

1. 通过调用URL.openConnection()并且进行类型转换来获取HttpUrlConnection实例；
2. 准备请求数据。请求的首要属性为URI。请求头可以包含像凭证，首选content-type，和session cookies等。
3. 如果需要可以上传请求体。HTTPURLConnection实例必须设置setDoOutput（true），同样可以通过URLConnection.getOutputStream()来拿到请求的数据。
4. 读取响应。响应头包括一些元数据：content-type，长度，修改时间和session cookies。响应数据可以通过UrlConnection.getInputStream()读取，如果没有响应数据，你将会得到一个空的流。
5. 断开连接。一旦响应体被读取之后，需要调用disconnecte()来进行断开连接，这会释放连接的资源。

```
URL url = new URL("http://www.android.com/");
//打开连接
HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
try {
//读取输入流
 InputStream in = new BufferedInputStream(urlConnection.getInputStream());
 readStream(in);
} finally {
//断开连接
 urlConnection.disconnect();
}
```

如果你请求的服务器使用的是HTTPS，比如：**URL url = new URL("https://www.xxx.com/");**那么强制装换类型后获取到的实例是HttpsUrlConnection的实例。

HTTPURLConnection会跟踪到5个HTTP重定向。

如果响应体包含错误数据，URLConnection.getInputStream将会抛出IO异常，可以通过getErrorStream来获取错误数据流。但使用UrlConnection.getHeaderFields头信息可以正常获取。

##### POST 内容

必须调用setOutput(true)进行设置以允许可以发送数据。为了更好的性能体验，可以使用setFixedLengthStreamingMode和setChunkedStreamingMode进行配置，否则，HttpUrlConnection会在传输数据之前，强制缓存完整的请求实体在内存中。这会增加（设置耗尽）堆和增加延迟。

setFixedLengthStreamingMode:如果请求体的大小是知道的，那么可以调用HttpURLConnection的setFixedLengthStreamingMode (int contentLength) 方法，该方法会告诉Android要传输的请求头Content-Length的大小，这样Android就无需读取整个请求体的大小，从而不必一下将请求体全部放到内存中，这样就避免了请求体占用巨大内存的问题。

setChunkedStreamingMode:如果请求体的大小不知道，那么可以调用setChunkedStreamingMode (int chunkLength)方法。该方法将传输的请求体分块传输，即将原始的数据分成多个数据块，chunkLength表示每块传输的字节大小。比如我们要传输的请求体大小是10M，我们将chunkLength设置为1024 * 1024 byte，即1M，那么Android会将请求体分10次传输，每次传输1M，具体的传输规则是：每次传输一个数据块时，首先在一行中写明该数据块的长度，比如1024 * 1024，然后在后面的一行中写入要传输的数据块的字节数组，再然后是一个空白行，这样第一数据块就这样传输，在空白行之后就是第二个数据块的传输，与第一个数据块的格式一样，直到最后没有数据块要传输了，就在用一行写明要传输的字节为0，这样在服务器端就知道读取完了整个请求体了。

如果设置的chunkLength的值为0，那么表示Android会使用默认的一个值作为实际的chunkLength。

使用setChunkedStreamingMode方法的前提是服务器支持分块数据传输，分块数据传输是从HTTP 1.1开始支持的，所以如果你的服务器只支持HTTP 1.0的话，那么不能使用setChunkedStreamingMode方法。

这个类返回的outputStream和inputStream没有缓冲。大多情况下应该调用BufferOutputStream和BufferInputStream来包装返回的流。只进行大量读写的调用者可能会去忽略缓冲。


```
HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
try {
 urlConnection.setDoOutput(true);
 urlConnection.setChunkedStreamingMode(0);

 OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
 writeStream(out);

 InputStream in = new BufferedInputStream(urlConnection.getInputStream());
 readStream(in);
} finally {
 urlConnection.disconnect();
}
```


输入输出流不会被缓冲，调用者需要通过使用BufferedInputStream和BufferedOutputStream对返回的输入输出流进行处理。
当和服务端进行大量数据传输时，使用流进行对数据量的限制。除非你一次性需要整个实体。

##### 处理网络登录

当你连接某些网络的时候，它们可能会阻塞互联网直到你点击登录页面。这种登录页面通常通过使用HTTP重定向来呈现。你可以通过URLConnection.getUrl()来测试当前连接是否发生了重定向。这个检测必须在获取到请求体之后才能够使用，并且在调用UrlConnection.getHeaderFields()或者UrlConnection.getInpuStream()才能够触发。

```
HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
try {
 InputStream in = new BufferedInputStream(urlConnection.getInputStream());
 if (!url.getHost().equals(urlConnection.getURL().getHost())) {
   // we were redirected! Kick the user out to the browser to sign on?
 }
 ...
} finally {
 urlConnection.disconnect();
}
```

### 请求处理

步骤：

1. 实例化URL对象
2. 实例化HttpUrlConnection对象
3. 设置连接属性、传递参数等
4. 获取返回码判断是否成功
5. 读取输入流
6. 关闭链接

### GET方式

```java
HttpURLConnection urlConnection = null;
try {
    URL url = new URL("Http://xxx");
    urlConnection = (HttpURLConnection) url.openConnection();
    //设置请求方法，默认是GET。GET、POST、HEAD、OPTIONS、PUT、DELETE、TRACE
    urlConnection.setRequestMethod("GET");
    //设置其他头部信息
    //设置字符集
    urlConnection.setRequestProperty("Charset", "UTF-8");
    urlConnection.setRequestProperty("Content-type", "application/json");
    urlConnection.setRequestProperty("DeviceType", "xxxxxx");
    urlConnection.connect();
    if(urlConnection.getResponseCode() == HttpURLConnection.HTTP_OK) {
        InputStream is = urlConnection.getInputStream();
        String json = getResponse(is);
        // TODO: PASS
        is.close();
    }
} catch (MalformedURLException e) {
    e.printStackTrace();
} catch (IOException e) {
    e.printStackTrace();
}finally {
    if(urlConnection != null) {
        urlConnection.disconnect();
    }
}
```

#### POST方式

```java
URL url = new URL("http://xxx");
HttpURLConnection connection = (HttpURLConnection) url.openConnection();
connection.setRequestMethod("POST");
connection.setDoOutput(true);
connection.setDoInput(true);
//设置其他头部信息
//设置字符集
connection.setRequestProperty("Charset", "UTF-8");
connection.setRequestProperty("Content-type", "application/json");
connection.setRequestProperty("DeviceType", "xxxxxx");
connection.connect();

OutputStream os = connection.getOutputStream();
String json = "{\"key\", \"value\"}";
os.write(json.getBytes());
os.flush();
os.close();

connection.connect();
if(connection.getResponseCode() == HttpURLConnection.HTTP_OK) {
    InputStream is = connection.getInputStream();
    String response = getResponse(is);
    // TODO pass
}

connection.disconnect();
```

简单的文件上传示例：

```java
HttpURLConnection connection = null;
try {
    URL url = new URL("http:xxxx");
    connection = (HttpURLConnection) url.openConnection();
    // 设置每次传输的流大小，可以有效防止手机因为内存不足崩溃
    // 此方法用于在预先不知道内容长度时启用没有进行内部缓冲的 HTTP请求正文的流。
    connection.setChunkedStreamingMode(51200); // 128K
    // 不使用缓存
    connection.setUseCaches(false);
    // 设置请求方式
    connection.setRequestMethod("POST");
    // 设置编码格式
    connection.setRequestProperty("Charset", "UTF-8");
    // 设置容许输出
    connection.setDoOutput(true);

    // 上传文件
    FileInputStream file = new FileInputStream(Environment.getExternalStorageDirectory().getPath()
            + "/xxxx.apk");
    OutputStream os = connection.getOutputStream();
    byte[] b = new byte[1024];
    int count = 0;
    while((count = file.read(b)) != -1){
        os.write(b, 0, count);
    }
    os.flush();
    os.close();

    // 获取返回数据
    if(connection.getResponseCode() == 200){
        InputStream is = connection.getInputStream();
        String respones = getResponse(is);
        // TODO pass
    }
} catch (MalformedURLException e) {
    e.printStackTrace();
} catch (Exception e) {
    e.printStackTrace();
} finally {
    if(connection != null){
        connection.disconnect();
    }
}
```

文件断点下载：

1. 
    1）设置断点请求setRequestProperty("range", "bytes=start-stop")。start和stop分别为开始点和结束点

    2）通过RandomAccessFile来将下载的字节插入到指定的位置
    
2） 对于输出流的三个方法的对比：

    os.write(byte[] buffer)：每次读取的字节数可能小于buffer的大小，造成数据错误。有时可能影响比较小，比如图片，但是如果是安装包等敏感文件则会造成不可使用的问题。
    
    os.write(int oneByte)：效率低
    
    os.write(byte[] buffer, int byteOffset, int byteCount):效率较高，通常建议使用
    
```
private int start = 0;
private int stop = 1024 * 1024;
private void download() throws IOException {
    HttpURLConnection connection = null;
    URL url = new URL("http://xxx");
    connection = (HttpURLConnection) url.openConnection();
    connection.setRequestMethod("GET");
    //设置开始下载位置和结束下载位置，单位为字节
    connection.setRequestProperty("range", "bytes=" + start + "-" + stop);
    String path = Environment.getExternalStorageState() + "/klxt.apk";
    //断点下载使用文件对象RandomAccessFile
    RandomAccessFile randomAccessFile = new RandomAccessFile(path, "rw");
    //移动指针到开始位置
    randomAccessFile.seek(start);
    connection.connect();
    InputStream is = null;
    if(connection.getResponseCode() == HttpURLConnection.HTTP_PARTIAL) {
        is = connection.getInputStream();
        int count = 0;
        byte[] buffer = new byte[1024];
        while ((count = is.read()) != -1) {
            randomAccessFile.write(buffer, 0, count);
        }
    }

    if(randomAccessFile != null) {
        randomAccessFile.close();
    }
    if(is != null) {
        is.close();
    }

    start = stop + 1;
    stop += stop;
}
```