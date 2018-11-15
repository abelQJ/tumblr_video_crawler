#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
import os.path
from multiprocessing import Pool
import crawler_conf as cf
import common_object as cm
import sys


def _down_load_one_video( video_url , verb = False):
        dir_path = os.path.join(cf.OutPutDir.video_save_dir,cm.CommonFunc().get_today())
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        target_url = cm.Url(video_url)
        cmd = 'cd ' + dir_path + ' && curl -s -L -o ' + target_url.get_md5() + ' ' + video_url
        if verb:
            cmd = 'cd ' + dir_path + ' && curl -L -o ' + target_url.get_md5() + ' ' + video_url
        print(cmd)
        start_time = time.time()
        os.system(cmd)
        end_time = time.time()
        print('download ',video_url, ' over,cost time:', end_time - start_time )

class Downloader:
    def __init__(self , url_dir , out_dir, process_num):
        self.url_dir = url_dir
        self.out_dir = out_dir
        self.process_num = process_num

    def download(self):
        all_video_url = cm.Dir(self.url_dir).walk_dir_get_files_content()
        all_had_down_video = set(cm.Dir(self.out_dir).walk_dir_get_files())
        pool = Pool(processes = self.process_num)
        need_down_video_url = []
        for video_url in all_video_url:
            if cm.Url(video_url).get_md5() not in all_had_down_video:
                need_down_video_url.append(video_url)
        if self.process_num <= 1:
            for video_url in need_down_video_url:
                _down_load_one_video(video_url , True)
        else:   
            map_async_ret = pool.map_async(_down_load_one_video,need_down_video_url)
            map_async_ret.get(365*24*3600)
            pool.close()
            pool.join()


def main():
    if len(sys.argv) != 2:
        print('useage: download_video.py process_num')
        exit()
    process_num = int(sys.argv[1])
    if process_num < 1 or process_num > 1024:
        process_num = cf.DownloaderConf.process_num
    downloader = Downloader(cf.OutPutDir.url_save_dir,cf.OutPutDir.video_save_dir,process_num)
    downloader.download()

if __name__ == '__main__':
    main()
