# Android Https

## 两种加密

加密方式分两种，对称加密和非对称加密。这两种方式都有自己的优劣势， https中这两种方式都采用了。 我们约定S是服务端，C是客户端，客户端需要从服务端获取信息；
对称加密

这种加密方式比较简单，就是双方都持有密匙。S和C都持有密匙， S通过密匙加密明文传递给C，C获取加密后的信息，用密匙解密信息。优势: 加密速度快, 劣势: 密匙的传递是个问题，容易被截取，密匙一旦被截取后， 就能轻易破解信息。常见的对称加密算法有DES、3DES、TDEA、Blowfish、RC5和IDEA。
非对称加密

非对称加密中，S和C端都有自己的公钥和私钥。公钥是公开的，私钥是私有的，私钥需要保密的。 这套公钥和私钥的有个两种加密解密流程：

    用公钥加密的信息，用私钥才能解密。因为私钥是私有的， 这种流程用于信息的加密解密；
    用私钥加密信息，用公钥来解密。因为公钥是共有的，这种流程用于认证。

在https中信息传递的密匙的传递是采用非对称加密传递的.
C端需要把信息传递给S端, 需要分几步.

    C端请求S端，S端把自己的公钥传递给C端。
    C用S的公钥把信息加密后传递给S. S用自己的私钥解密获取信息。
    常用的非对称加密算法有RSA、Elgamal、Rabin、D-H、ECC（椭圆曲线加密算法）等。

问：既然对称加密和非对称加密都需要保密好自己的私钥， 那有什么区别呢？

对称加密中，私钥不仅需要自己知道也需要解密方知道。 这样私钥就有一个传递的流程， 这个流程就会有很大风险。 而非对称加密只需要自己保密好自己的私钥就好了。 公钥大家都知道，不需要保密，就少了一个私钥传递的过程。 少了很大的风险。

## HTTPS通信过程

### HTTPS中的SSL/TLS协议

HTTPS = HTTP + SSL/TLS协议
SSL的全称是Secure Sockets Layer，即安全套接层协议，是为网络通信提供安全及数据完整性的一种安全协议。SSL协议在1994年被Netscape发明，后来各个浏览器均支持SSL，其最新的版本是3.0;
TLS的全称是Transport Layer Security，即安全传输层协议，最新版本的TLS建立在SSL 3.0协议规范之上.在理解HTTPS时候,可以把SSL和TLS看做是同一个协议。

### HTTPS加密方式

HTTPS为了兼顾安全与效率，同时使用了对称加密和非对称加密。
数据是被对称加密传输的，对称加密过程需要客户端的一个密钥，为了确保能把该密钥安全传输到服务器端;
采用非对称加密对该密钥进行加密传输，总的来说，对数据进行对称加密，对称加密所要使用的密钥通过非对称加密传输。

### HTTPS通信流程

一个HTTPS请求实际上包含了两次HTTP传输，可以细分为8步。

- 第一次HTTP请求:

1.客户端向服务器发起HTTPS请求，连接到服务器的443端口。
2.服务器端有一个密钥对，即公钥和私钥，是用来进行非对称加密使用的，服务器端保存着私钥，不能将其泄露，公钥可以发送给任何人。
3.服务器将自己的公钥发送给客户端。
4.客户端收到服务器端的公钥之后，会对公钥进行检查，验证其合法性，如果公钥合格，那么客户端会生成一个随机值，这个随机值就是用于进行对称加密的密钥，我们将该密钥称之为client key，即客户端密钥，这样在概念上和服务器端的密钥容易进行区分。然后用服务器的公钥对客户端密钥进行非对称加密，这样客户端密钥就变成密文了，至此，HTTPS中的第一次HTTP请求结束。

- 第二次HTTP请求:

1.客户端会发起HTTPS中的第二个HTTP请求，将加密之后的客户端密钥发送给服务器。
2.服务器接收到客户端发来的密文之后，会用自己的私钥对其进行非对称解密，解密之后的明文就是客户端密钥，然后用客户端密钥对数据进行对称加密，这样数据就变成了密文。
然后服务器将加密后的密文发送给客户端。
3.客户端收到服务器发送来的密文，用客户端密钥对其进行对称解密，得到服务器发送的数据。这样HTTPS中的第二个HTTP请求结束，整个HTTPS传输完成。

### 数字证书

- 为什么需要数字证书

在https中需要证书，证书的作用是为了防止"中间人攻击"的。 如果有个中间人M拦截客户端请求,然后M向客户端提供自己的公钥，M再向服务端请求公钥,作为"中介者" 这样客户端和服务端都不知道,信息已经被拦截获取了。这时候就需要证明服务端的公钥是正确的.
怎么证明呢?
就需要权威第三方机构来公正了.这个第三方机构就是CA. 也就是说CA是专门对公钥进行认证，进行担保的，也就是专门给公钥做担保的担保公司。 全球知名的CA也就100多个，这些CA都是全球都认可的，比如VeriSign、GlobalSign等，国内知名的CA有WoSign。

- 数字证书怎么起作用

不论什么平台，设备的操作系统中都会内置100多个全球公认的CA，说具体点就是设备中存储了这些知名CA的公钥。当客户端接收到服务器的数字证书的时候，会进行如下验证：

1.首先客户端会用设备中内置的CA的公钥尝试解密数字证书，如果所有内置的CA的公钥都无法解密该数字证书，说明该数字证书不是由一个全球知名的CA签发的，这样客户端就无法信任该服务器的数字证书。
2.如果有一个CA的公钥能够成功解密该数字证书，说明该数字证书就是由该CA的私钥签发的，因为被私钥加密的密文只能被与其成对的公钥解密。
3.除此之外，还需要检查客户端当前访问的服务器的域名是与数字证书中提供的“颁发给”这一项吻合，还要检查数字证书是否过期等。

- 证书链

一般CA不会直接去使用自己的私钥去签名某网站的证书, 一般CA会签发一个子证书, 然后用这子证书去签网站的证书. 有可能有多个子证书. 如果父证书是可以被信任的,那么这个子证书就是可以被信任的.

### Android中HTTPS的使用

在代码中配置https的证书的代码如下:

```
//配置: 
 setCertificates(builder, application.getAssets().open("xxxx.cer"));

/**
 * 设置签名证书
 *
 * @param builder
 * @param certificates
 */
public void setCertificates(OkHttpClient.Builder builder, InputStream... certificates) {
    try {

        //创建X.509格式的CertificateFactory
        CertificateFactory certificateFactory = CertificateFactory.getInstance("X.509");

        // 创建一个默认类型的KeyStore，存储我们信任的证书
        KeyStore keyStore = KeyStore.getInstance(KeyStore.getDefaultType());
        keyStore.load(null);

        //从asserts中获取证书的流
        int index = 0;
        for (InputStream certificate : certificates) {
            String certificateAlias = Integer.toString(index++);
            //将证书ca作为信任的证书放入到keyStore中
            keyStore.setCertificateEntry(certificateAlias, certificateFactory.generateCertificate(certificate));
            try {
                if (certificate != null)
                    certificate.close();
            } catch (IOException e) {
                LogUtils.debugInfo("https证书错误1");
            }
        }

        //创建TLS类型的SSLContext对象， that uses our TrustManager
        SSLContext sslContext = SSLContext.getInstance("TLS");
        //TrustManagerFactory是用于生成TrustManager的，我们创建一个默认类型的TrustManagerFactory
        TrustManagerFactory trustManagerFactory = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
        trustManagerFactory.init(keyStore);
        sslContext.init(null, trustManagerFactory.getTrustManagers(), new SecureRandom());

        //配置到OkHttpClient 或者
        builder.sslSocketFactory(sslContext.getSocketFactory());
    } catch (Exception e) {
        e.printStackTrace();
        LogUtils.debugInfo("https证书错误2");
    }
}
```

需要注意的是,如果自定义X509TrustManager的时候一定要复写其中三个重要的方法, 如下错误的代码:

```
TrustManager tm = new X509TrustManager() {
    public void checkClientTrusted(X509Certificate[] chain, String authType)
            throws CertificateException {
              //do nothing，接受任意客户端证书
    }

    public void checkServerTrusted(X509Certificate[] chain, String authType)
            throws CertificateException {
              //do nothing，接受任意服务端证书
    }

    public X509Certificate[] getAcceptedIssuers() {
        return null;
    }
};

sslContext.init(null, new TrustManager[] { tm }, null);
```

正确的做法:

```
new X509TrustManager() {
          @Override
          public void checkClientTrusted(X509Certificate[] chain,
                  String authType)
                  throws CertificateException {

          }

          @Override
          public void checkServerTrusted(X509Certificate[] chain,
                  String authType)
                  throws CertificateException {
              for (X509Certificate cert : chain) {

                  // Make sure that it hasn't expired.
                  cert.checkValidity();

                  // Verify the certificate's public key chain.
                  // ca是通过证书流获取的证书
                  try {
                      cert.verify(((X509Certificate) ca).getPublicKey());
                  } catch (NoSuchAlgorithmException e) {
                      e.printStackTrace();
                  } catch (InvalidKeyException e) {
                      e.printStackTrace();
                  } catch (NoSuchProviderException e) {
                      e.printStackTrace();
                  } catch (SignatureException e) {
                      e.printStackTrace();
                  }
              }
          }

          @Override
          public X509Certificate[] getAcceptedIssuers() {
              return new X509Certificate[0];
          }
      }
}
```
