# -*- coding: utf-8 -*-
from lxml import html
from bs4 import BeautifulSoup as bs
import xlwt,xlrd,urllib.request,requests,os,re,shutil,time,wget

# manganelo.com
class MangaDownload:
	def __init__(self,path):
		self.path=path
		self.save_path=""
		
		
	def check_path(self):
		page=requests.get(self.path)
		soup = bs(page.content, "lxml")
		if "404" not in soup.title.text and soup.title.text!="":
			manga_info_panel = soup.find_all("div",{"class":"panel-story-info"})
			manga_chapter_panel = soup.find_all("div",{"class":"panel-story-chapter-list"})
			if len(manga_info_panel)==0 or len(manga_chapter_panel)==0:
				return None,None
			else:
				return manga_info_panel,manga_chapter_panel
		else:
			return None,None
	
	def get_save_folder(self,chap_name):
		cur_dir=os.path.dirname(os.getcwd())
		if not os.path.isdir(cur_dir+"\\media\\manga\\"):
			os.mkdir(cur_dir+"\\media\\manga\\")
		if not os.path.isdir(cur_dir+"\\media\\manga\\Manga1"):
			os.mkdir(cur_dir+"\\media\\manga\\Manga1\\")
		if not os.path.isdir(cur_dir+"\\media\\manga\\Manga1\\%s\\"%chap_name):
			os.mkdir(cur_dir+"\\media\\manga\\Manga1\\%s\\"%chap_name)
		return cur_dir+"\\media\\manga\\Manga1\\%s\\"%chap_name
		
	def get_chapter_list(self,mcp,chap_list=None):
		chapter_soup_list=mcp[0].find_all("ul",{"class":"row-content-chapter"})[0].find_all("li",{"class":"a-h"})
		chapter_list=[]
		for chapter_soup in chapter_soup_list:
			chap_path=chapter_soup.find("a").get("href")
			chap_name=chapter_soup.find("a").text
			chapter_list.append((chap_name,chap_path))
		return chapter_list
		
	def download(self,chap_list):
		mip,mcp=self.check_path()
		chapter_path_list = self.get_chapter_list(mcp,chap_list)
		for chapter_path in chapter_path_list[:10]:
			chap_page=requests.get(chapter_path[1])
			save_path=self.get_save_folder(chapter_path[0])
			chap_soup=bs(chap_page.content,"lxml")
			image_soup_list=chap_soup.find_all("div",{"class":"container-chapter-reader"})[0].find_all("img")
			image_path_list=[(elem.get("alt"),elem.get("src")) for elem in image_soup_list]
			print(image_path_list)
			for image_path in image_path_list:
				# time.sleep(5)
				# r = requests.get(image_path[1], stream=True)
				# print(image_path[1])
				# if r.status_code == 200:
				# 	r.raw.decode_content = True
				# 	with open("%s\\%s" % (save_path,image_path[0]), 'wb') as f:
				# 		shutil.copyfileobj(r.raw, f)
				# 	print('Image sucessfully Downloaded: ', image_path[0])
				# else:
				# 	print('Image Couldn\'t be retreived')
				print(urllib.request.urlopen(image_path[1]))
		
		
		
path="https://manganelo.com/manga/hyer5231574354229"
#path="http://talhacelik.com"
mg=MangaDownload(path)
#mg.check_path()
mg.download(None)


