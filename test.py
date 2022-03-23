# 第好几个方法实例
import os
from time import sleep

import requests  # 先导入爬虫的库，不然调用不了爬虫的函数
from lxml import etree
import xlwt


def save_img(img_url, name):
	if img_url.split('/')[-1] == "moren.jpg":
		img_url = "http://open.ahau.edu.cn/moren.jpg"
	d = 'img//'
	path = d + name + img_url.split('/')[-1]
	try:
		if not os.path.exists(d):
			os.mkdir(d)
		if not os.path.exists(path):
			r = requests.get(img_url)
			r.raise_for_status()
			print()
			with open(path, 'wb') as f:
				f.write(r.content)
				f.close()
				print("图片保存成功")
		else:
			print("图片已存在")
	except:
		print("图片获取失败")


def get_data(id):
	# cookie需要更新，直接上链接复制就行
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
		"Cookie": "MNOPQ61F2; ASPSESSIONIDASCRCCQC=OCFGGDKDGNMJMGAFFAMNFAJC; OKLCW05mfQ0A0e2=KTtCA9df264hqErZOS9nk37X_D9pph4s2z8FDPRXJdRIhNv3yoOKLehKbNTVUyW9TicCmjxnDuydmcaR632waaSUlMPRLBeI0J1GlMcZu7Jwm"
	}  # 设置头部信息,伪装浏览器
	url = "http://jsxx.ahau.edu.cn/jsxx_show.asp?ID=" + str(id)
	response = requests.get(url, headers=headers)  # get方法访问,传入headers参数，
	response.encoding = "GBK"
	print("状态码:", response.status_code)  # 200！访问成功的状态码
	if response.status_code == 412:
		print("请更换cookie")
		return
	# print( response.text )
	# print(response.content)
	wb_data = response.text

	html = etree.HTML(wb_data)  # 将页面转换成文档树

	# print(html)

	a = html.xpath('//img/@src')
	# print(a[1])

	b = html.xpath('//strong/text()')  # 提取标题中内容
	print(b)
	if len(b) == 0:
		print("系统无信息")
		return
	name = b[0]
	test = html.xpath('//div[@align="left"]/text()')
	img_url = "http://jsxx.ahau.edu.cn"  # 图片前缀
	img_url = img_url + a[1]

	test.insert(0, img_url)
	test.insert(0, name)
	test.insert(0, id)
	# print(test)
	# print(img_url)  #打印b，这里的b是一个数组
	save_img(img_url, name)
	return test


def init_file(sheet):
	head = ["网页id", '姓名', '头像img_url', '专业名称：', '研究方向：', '技术职务：', '行政职务：', '办公电话：', '办公传真：', 'E-mail：',
			'实验室主页：',
			'通讯地址：', '邮政编码：', '\u3000主要教学经历与成果', '\u3000主要研究领域', '\u3000主要科研项目', '\u3000主要科研成果', '\u3000代表性论文论著']
	for i in range(0, len(head)):
		sheet.write(0, i, head[i])


if __name__ == '__main__':
	book = xlwt.Workbook(encoding='utf-8', style_compression=0)
	sheet = book.add_sheet('mysheet', cell_overwrite_ok=True)
	init_file(sheet)  # 初始化excel第一行信息

	sum = 50  # 设定爬取数量 sum
	id = 1991000  # id号,起始号
	index = 0
	for n in range(0, sum):
		sleep(1)
		print("---------------检索第%d条-------------" % (n + 1))
		info = get_data(id + n)
		# print(info)
		if info is None:
			print("无信息跳过")
			continue
		print("第%d条成功，进行存储--------" % n)
		for i in range(0, len(info)):
			sheet.write(index + 1, i, info[i])
		index = index + 1

	book.save('test.xls')
