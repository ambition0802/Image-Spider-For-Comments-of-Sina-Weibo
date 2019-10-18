# -*- coding: utf-8 -*-
#指定脚本为utf-8编码

import sys
import requests
import json
from pyquery import PyQuery as pq 
import os
import time


'''
	根据图片的src判断是否是用户评论中的图片
	srcOfPic包含了'.sinaimg.cn/thumb',则返回true，否则false
'''
def isCommentImg(srcOfPic):
	return '.sinaimg.cn/thumb' in srcOfPic

'''
	根据图片的src来获取图片的名字
	//wx4.sinaimg.cn/thumb180/9f4d6352ly1g2ok5ayrocj20u00y0n7o.jpg
	上面链接中的9f4d6352ly1g2ok5ayrocj20u00y0n7o.jpg就是图片的名字
'''
def getImgName(srcOfPic):
	srcArr = srcOfPic.split("/")
	imgName = srcArr[len(srcArr)-1]
	return imgName

'''
	下载图片
'''
def downloadImg(fileDir, imgName):
	#判断文件的目录是否存在,不存在的话创建他
	if not os.path.exists(fileDir):
		os.makedirs(fileDir)

	#要下载的图片的url
	url = 'https://wx4.sinaimg.cn/bmiddle/'+imgName
	res = requests.get(url)
	img = res.content
	filePath = fileDir + imgName
	fileWriter = open(filePath, 'wb')
	fileWriter.write(img)
	print(url, ' 下载完成！')

'''
	获取新浪微博的热评的评论
'''
def getCommontsHtml(weiboId,pageNum):
	#新浪微博的域名
	sinaRealmName = 'https://weibo.com'

	#获取评论的接口
	bigCommentsApi = '/aj/v6/comment/big'

	'''
		调用新浪接口的cookie
		先暂时直接去浏览器上拿来用,之后在搞自动获取cookie的  TODO
	'''
	Cookie='SINAGLOBAL=3093814988429.984.1570710524997; SUB=_2AkMq_W7Nf8NxqwJRmP4VyWLhaIhwyg3EieKcoZ8WJRMxHRl-yT83qk8DtRB6AX1AIWmrmjNcfXv6QgcD3O728mGPHv5J; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWAAUPYPUDyN8khYT-mbU7z; Apache=5930130329974.999.1571408069328; ULV=1571408069657:5:5:2:5930130329974.999.1571408069328:1570964691931; Ugrow-G0=1ac418838b431e81ff2d99457147068c; YF-V5-G0=f5a079faba115a1547149ae0d48383dc; YF-Page-G0=89906ffc3e521323122dac5d52f3e959|1571408553|1571408553'
	#获取评论接口的请求头
	headers={'Cookie':Cookie}

	#获取评论的接口的基本参数
	ajwvr='6'
	id=weiboId
	from1='singleWeiBo'
	__rnd='1560670611591'

	#获取评论的接口的基本参数放到payload中
	payload = {'ajwvr':ajwvr,'id':id,'from':from1,'__rnd':__rnd}
	#获取热评第一页的内容是不需要带page参数的
	if pageNum != 1:
		payload.update({'page':pageNum})
		

	r = requests.get(sinaRealmName+bigCommentsApi,headers=headers,params=payload)

	'''
	#获取返回内容
	text = r.text
	#将返回内容写到文件中
	responseFile = open('./response.text', 'w')
	responseFile.write(text)
	'''

	#获取返回内容
	response = r.text
	print("pageNum : ",pageNum)
	print("response = " + response)	
	
	responseJson = json.loads(response) 
	
	data = responseJson['data']
	#评论内容
	contentHtml = data['html']
	return contentHtml

'''
	main方法
'''
def main(weiboId, filePath):
	pageNum = 1

	lastImgName = ''

	while True:

		contentHtml = getCommontsHtml(weiboId, pageNum)

		#通过PyQuery来解析评论内容的html,获取所有img的标签
		contentHtml = pq(contentHtml)
		imgs = contentHtml('img').items()

		#遍历img tag,获取图片链接
		for img in imgs:
			srcOfImg = img.attr('src')
			if isCommentImg(srcOfImg):
				imgName = getImgName(srcOfImg)
				if imgName == lastImgName:
					return
				downloadImg(filePath, imgName)
				lastImgName = imgName
			   #下载每张图片的时间间隔为2s
				time.sleep(2)

		pageNum = pageNum + 1 
		#获取每一页评论的时间间隔为30s
		time.sleep(30)

"""
	脚本入口
	第一个入参为微博id（https://weibo.com/aj/v6/comment/big 接口的 id参数）
	比如下面这条微博 调用https://weibo.com/aj/v6/comment/big接口的时候传的参数中名为'id'的参数的值为4367970740108457
	https://weibo.com/1595142854/Hswee0sdj?type=comment  
	还没有找到方法通过某条任务的链接来获取微博id
	第二个参数为保存图片的本地目录
"""
if __name__ == '__main__':
	weiboId = sys.argv[1]

	filePath = sys.argv[2]
	if filePath.endswith('/'):
		main(weiboId, filePath)
	else:
		print("保存图片的目录请以'/'结尾")
