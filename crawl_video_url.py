#!/usr/bin/python
# -*- coding: utf-8 -*-
import crawler_conf as cf
import common_object as cm
import sys

class TumblrVideoCrawler:
    def __init__(self , usr_list , max_page_num , max_exception_num ,url_dir, video_dir):
        self.usr_list = usr_list
        self.max_page_num = max_page_num
        self.max_exception_num = max_exception_num
        self.url_dir = url_dir
        self.video_dir = video_dir

    def crawl(self):
        for user_name in self.usr_list:
            user = cm.User(user_name , self.max_page_num, self.max_exception_num)
            user.get_user_all_video_url(self.url_dir)

def main():
    if len(sys.argv) != 2:
        print('useage: crawl_video_url.py user_list.txt')
        print('\tuser_list.txt contains the user name who you want to crawl,one user per line')
        exit()
    user_list = open(sys.argv[1],'r').readlines()
    user_list = map(lambda u:u.strip('\n \t'),user_list)
    crawler = TumblrVideoCrawler(user_list , cf.CrawlerConf.max_page_num , 
                                 cf.CrawlerConf.max_exception_num,cf.OutPutDir.url_save_dir,
                                 cf.OutPutDir.video_save_dir)
    crawler.crawl()


if __name__ == '__main__':
    main()
