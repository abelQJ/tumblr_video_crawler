import os
import re
import time
import os.path
import hashlib
import subprocess



class RegexTpl:
    post_id_extract_re = re.compile(r'data-post-id="\d+"')
    video_url_extract_re = re.compile(r'https://\w+.tumblr.com/video_file/t:[^"]+')

class UrlTpl:
    user_page_url_tpl = 'https://{_USER_NAME_}.tumblr.com/page/{_PAGE_}'
    user_video_page_url_tpl = 'https://www.tumblr.com/video/{_USER_NAME_}/{_POST_ID_}/700/'


class CommonFunc:
    def __init__(self):
        pass

    def get_today(self):
        return time.strftime("%Y-%m-%d")

class Dir:
    def __init__(self, path):
        self.path = path

    def walk_dir_get_files(self):
        for parent,child_dirs,child_files in os.walk(self.path):        
            for file in child_files:
                file_full_path = os.path.normpath(os.path.join(parent,file))
                yield file_full_path  

    # get all file content line list
    def walk_dir_get_files_content(self):
        line_list = []
        for file in self.walk_dir_get_files():
            with open(file,'r') as rf:
                line_list.extend(rf.readlines())
        return list(set(line_list))


class Url:
    def __init__(self,url):
        self.url = url

    def get_md5(self):
        md5 = hashlib.md5()
        md5.update(self.url.encode('utf8'))
        return md5.hexdigest()

    def get_page_content(self):
        cmd = 'curl ' + self.url
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

class User:
    def __init__(self , user_name, max_page_num, max_exc_num):
        self.user_name = user_name
        self.max_page_num = max_page_num
        self.max_exc_num = max_exc_num

    def get_page_url(self , page_num):
        return UrlTpl.user_page_url_tpl.replace('{_USER_NAME_}',self.user_name).replace('{_PAGE_}',str(page_num))

    def get_page_post_id_list(self , page_num):
        user_page_url = self.get_page_url(page_num)
        user_page = Url(user_page_url)
        oringin_post_id_list = RegexTpl.post_id_extract_re.findall(user_page.get_page_content())
        post_id_list = map(lambda x:x.replace('data-post-id=','').strip('"'),oringin_post_id_list)
        return list(set(post_id_list))

    def get_post_detail_page_url(self , post_id):
        return UrlTpl.user_video_page_url_tpl.replace('{_USER_NAME_}',self.user_name).replace('{_POST_ID_}',post_id)

    def get_video_url_list_in_post(self , post_id):
        post_page = Url(self.get_post_detail_page_url(post_id))
        video_url_list = RegexTpl.video_url_extract_re.findall(post_page.get_page_content())
        print(video_url_list)
        return list(set(video_url_list))

    def get_video_url_list_in_page(self , page_num):
        video_url_list = []
        post_id_list = self.get_page_post_id_list(page_num)
        for post_id in post_id_list:
            video_url_list.extend(self.get_video_url_list_in_post(post_id))
        return list(set(video_url_list))

    def get_user_all_video_url(self , out_dir):
        dir_path = os.path.join(out_dir , CommonFunc().get_today())
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_name = self.user_name +'_video_url.txt'
        full_file_name = os.path.join(dir_path,file_name)
        output = open(full_file_name,'w')
        page_num = 2
        except_num = 0
        while True:
            try:
                print('handle user:',self.user_name,",page:",page_num)
                page_post_id = self.get_page_post_id_list(page_num)
                video_url_list = self.get_video_url_list_in_page(page_num)
                if len(video_url_list) == 0 and len(page_post_id) == 0:
                    break
                print(video_url_list)
                for url in video_url_list:
                    output.write(url + '\n')
            except Exception as e:
                print('error happen when handle,user:',self.user_name,',page:',page_num,"exception:",str(e))
                except_num = except_num + 1
            finally:
                page_num = page_num + 1 
            if page_num > self.max_page_num or except_num > self.max_exc_num:
                break 

