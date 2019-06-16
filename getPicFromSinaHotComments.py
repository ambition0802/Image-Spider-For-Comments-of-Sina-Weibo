# -*- coding: utf-8 -*-
#指定脚本为utf-8编码

import sys
import requests
import json
from pyquery import PyQuery as pq 
import os

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
	Cookie='SINAGLOBAL=3830920360065.313.1557148481279; SUB=_2AkMrigF0f8NxqwJRmP4RzGLra4h_wgHEieKd1vCvJRMxHRl-yT83qkUOtRB6AAovmxW7GNrEnA4Ffi-HP1qYqzCd945I; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WF.7DBAUaXoZfhOArNkWz6A; UOR=fulibus.net,widget.weibo.com,fulibus.net; _s_tentry=fulibus.net; Apache=8803758653206.477.1560665785919; ULV=1560665785943:16:10:1:8803758653206.477.1560665785919:1560595319875; Ugrow-G0=9ec894e3c5cc0435786b4ee8ec8a55cc; YF-V5-G0=d30fd7265234f674761ebc75febc3a9f; WBtopGlobal_register_version=3cccf158e973a877; YF-Page-G0=530872e91ac9c5aa6d206eddf1bb6a70|1560670612|1560670597'

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

		pageNum = pageNum + 1 

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

	
	


	

