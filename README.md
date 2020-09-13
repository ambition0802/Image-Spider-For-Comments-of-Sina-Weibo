新浪微博又开始第N界比胸大赛了，论坛里的老哥都在求打包图片，既然这样，我就来当这个好人心吧~

之前没用过python,不过基础的语法看看[菜鸟教程](https://www.runoob.com/python3/python3-tutorial.html)就行了,剩下就是根据自己的需求去查找相关的轮子（现成的Python库）就好了。

爬取新浪微博热评中的图片

https://weibo.com/1595142854/Hswee0sdj?type=comment
https://weibo.com/1802027532/Hk9hG40Pn?type=comment


1.https://weibo.com/1595142854/Hswee0sdj?type=comment打开浏览器输入网址，打开f12，按下回车

2.在f12中发现这种格式的链接是用户评论中的图片链接
https://wx4.sinaimg.cn/thumb180/005KeDszgy1g2ohng3vfkj30u01hc7wh.jpg
(也可能是wx3或这wx2，总之就是wx后面的数字是会变的，经过测试数字范围为[1,4]，任意在范围内改动数字，然后去请求图片发现图片都是可以请求到的，所以这里多个域名应该是用来分流的，新浪的请求量这么大数据库也应该是分布式的)

但是这个链接获取的图片是小图压缩过的，看起来很不爽啊，要看就看大图
在评论区中找到对应的图片，点开图片发现请求的链接如下：
https://wx4.sinaimg.cn/bmiddle/005KeDszgy1g2ohng3vfkj30u01hc7wh.jpg
url中的thumb180变成了bmiddle，这个就是大图了~~~

3.好了，知道用户评论中大图的请求链接格式之后，就要把所有的图片链接都收集起来了。
通过在微博页面上操作，发现点击更多评论会请求这个接口https://weibo.com/aj/v6/comment/big，查看这个接口的返回值，在里面搜索wx4.sinaimg.cn,果然能搜到用户评论中的图片链接，经过测试，发现用户评论（自然包括图片链接了）确实是保存在这个接口中的，每次点击查看更多，就通过这个接口请求下面的评论并展示到页面中。下面就研究下这个接口找到规律就好了


https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4367970740108457&root_comment_max_id=13981136832237499&root_comment_max_id_type=0&root_comment_ext_param=&page=2&filter=hot&sum_comment_number=2127&filter_tips_before=0&from=singleWeiBo&__rnd=1560668732539

观察接口参数，一眼就发现了page=2，尝试只改变page的数值为2去请求下一个分页的评论内容，发现接口返回的内容，和实际点击查看更多获取到的下一页的评论内容是一样的。
这也太简单了吧。。。其他参数都不用关了，将page设置成10000和100000,返回的内容都是一样的，这里后台应该是做了处理，分页序号如果超过了实际最大值，就只返回最后一页的评论，这样子我们循环遍历的时候可以根据返回中的图片的id是否在上一次请求到的图片中存在来判断是否要结束循环。


分析完毕,开始写python脚本


14：17开始分析  到17：51写完脚本



TODO downloadImg可以优化下，通过解析微博评论(html文档)，将用户的微博主页的链接设置为图片的名字，方便直接找到图片对应的用户
新浪微博又开始第N界比胸大赛了，论坛里的老哥都在求打包图片，己然这样，我就来当这个好人心吧~

之前没用过python,不过基础的语法看看[菜鸟教程](https://www.runoob.com/python3/python3-tutorial.html)就行了,剩下就是根据自己的需求去查找相关的轮子（现成的Python库）就好了。

要爬取的新浪微博热评中的图片

https://weibo.com/1595142854/Hswee0sdj?type=comment
https://weibo.com/1802027532/Hk9hG40Pn?type=comment

1. https://weibo.com/1595142854/Hswee0sdj?type=comment打开浏览器输入网址，打开f12，按下回车，在f12中发现这种格式的链接是用户评论中的图片链接：
   	https://wx4.sinaimg.cn/thumb180/005KeDszgy1g2ohng3vfkj30u01hc7wh.jpg
   (也可能是wx3或这wx2，总之就是wx后面的数字是会变的，经过测试数字范围为[1,4]，任意在范围内改动数字，然后去请求图片发现图片都是可以请求到的，所以这里多个域名应该是用来分流的，新浪的请求量这么大数据库也应该是分布式的)

2. 但是这个链接获取的图片是小图压缩过的，看起来很不爽啊，要看就看大图。
   在评论区中找到对应的图片，点开图片发现请求的链接如下：
   https://wx4.sinaimg.cn/bmiddle/005KeDszgy1g2ohng3vfkj30u01hc7wh.jpg
   url中的thumb180变成了bmiddle，这个就是大图了~~

3. 好了，知道用户评论中大图的请求链接格式之后，就要把所有的图片链接都收集起来了。
   通过在微博页面上操作，发现点击更多评论会请求这个接口https://weibo.com/aj/v6/comment/big，查看这个接口的返回值，在里面搜索wx4.sinaimg.cn,果然能搜到用户评论中的图片链接，经过测试，发现用户评论（自然包括图片链接了）确实是保存在这个接口中的，每次点击查看更多，就通过这个接口请求下面的评论并展示到页面中。下面就研究下这个接口找到规律就好了：

   https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4367970740108457&root_comment_max_id=13981136832237499&root_comment_max_id_type=0&root_comment_ext_param=&page=2&filter=hot&sum_comment_number=2127&filter_tips_before=0&from=singleWeiBo&__rnd=1560668732539

4. 观察接口参数，一眼就发现了page=2，尝试只改变page的数值为2去请求下一个分页的评论内容，发现接口返回的内容，和实际点击查看更多获取到的下一页的评论内容是一样的。
   这也太简单了吧，其他参数都不用管了，将page设置成10000和100000,返回的内容都是一样的，这里后台应该是做了处理，分页序号如果超过了实际最大值，就只返回最后一页的评论，这样子我们循环遍历的时候可以根据当前page返回中的图片id是否存在与上一page请求到的图片id来判断是否要结束循环。


分析完毕,开始写python脚本

14：17开始分析  到17：51写完脚本



TODO downloadImg可以优化下，通过解析微博评论(html文档)，将用户的微博主页的链接设置为图片的名字，方便直接找到图片对应的用户
