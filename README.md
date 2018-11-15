# tumblr_video_crawler
一个专门爬取tumblr视频的爬虫

# 工作原理
这个爬虫工作分两步：
1. 爬取指定用户列表的视频链接.
2. 使用爬取的链接自动批量并发下载.

# 使用方法
1. 爬取视频链接
```
crawl_video_url.py user_list.xt 
```
其中user_list.txt代表需要爬取的用户名列表，一行一个用户。爬取到的内容会保存到OutPutDir.url_save_dir指定的目录

2. 批量下载视频
```
download_video.py process_num
```
其中process_num是一个数字，代表下载时的并发数，并不是越大越好需要结合自己的带宽情况。下载的视频会保存到OutPutDir.video_save_dir指定的目录

3. 爬取下载一步到位
```
crawl_video_url.py user_list.xt && download_video.py process_num
```
当你收集好用户名列表后，执行这句命令，并设置电脑不待机，一天大概能下好几十G的资源，**哥只能帮你们到这儿了~**

# 其他说明
1. 该爬虫在网页请求和视频下载时使用了curl,所以务必保证机器上已安装了curl
2. tumblr网站访问本身是需要翻墙的,为使curl也能翻墙需要设置https代理，设置命令如下：
```
    export http_proxy=domain:port
    export https_proxy=domain:port
```
3. 爬取到视频url和视频的保存地址可以在配置中设置，相关内容如下：
```
class OutPutDir:
    url_save_dir = './video_url_list/'
    video_save_dir = './video_list'
```
4. 爬取用户视频时会有一个最大页数设置，和最大错误数设置，这两个参数都是为了避免爬虫进入死循环，相关内容如下：
```
class CrawlerConf:
    max_page_num = 50
    max_exception_num = 10
```

