from django.shortcuts import render
#这是django给我们的视图类
from django.views.generic import View 
# Create your views here.
from .models import Upload
#导入 model
from django.http import HttpResponsePermanentRedirect,HttpResponse
import random
import string
import datetime
import json

class HomeView(View):
	#专门用于处理get请求
	def get(self,request):
		#如果收到get请求,我们就返回base.html
		u = Upload.objects.all()
		return render(request,"content.html",{"content":u})
	def post(selfself,request):#post请求
		if request.FILES:#如果有文件,向下执行,没有文件的情况,前端已处理好
			file = request.FILES.get('file')#获取文件
			name = file.name#获取文件名
			size = int(file.size)#获取文件大小
			with open('static/file/'+name,'wb') as f:#写文件到static/file
				f.write(file.read())
			code = ''.join(random.sample(string.digits,8))#生成8位的code
			u = Upload(
				code = code,
				path = 'static/file/'+name,
				name = name,
				Filesize = size,
				PCIP=str(request.META['REMOTE_ADDR']),#获取上传文件的用户ip
			)
			u.save()
			return HttpResponsePermanentRedirect("/S/"+code)
			# 使用 HttpResponsePermanentRedirect 重定向到展示文件的页面.这里的 code 唯一标示一个文件。
class DisplayView(View):
	#展示文件的视图类
	def get(self,request,code):
		#支持get请求,并且可以接收一个参数,这里的code需要和配置路由的code保持一致
		u = Upload.objects.filter(code=str(code))
		#ORM 查找
		if u:
			#如果u有内容,u的访问次数+1,否则返回给前端的也是空的
			for i in u:
				i.DownloadDocount+=1
				i.save()
		return render(request,'content.html',{"content":u})

class MyView(View):#定义一个MyView用于完成用户管理功能
	def get(self,request):
		IP = request.META['REMOTE_ADDR']#获取用户的IP
		u = Upload.objects.filter(PCIP=str(IP))
		for i in u:
			i.DownloadDocount+=1#访问量+1
			i.save()
		return render(request,'content.html',{"content":u})

class SearchView(View):
	def get(self,request):
		code = request.GET.get("kw")#获取get请求中的kw的值,及搜索的内容
		u = Upload.objects.filter(name=str(code))
		data = {}#定义一个空字典,将查询的结果放入字典中
		if u:
			for i in range(len(u)):
				'''将符合条件的数据放到data中'''
				u[i].DownloadDocount += 1
				u[i].save()
				data[i] = {}
				data[i]['download'] = u[i].DownloadDocount
				data[i]['filename'] = u[i].name
				data[i]['id'] = u[i].id
				data[i]['ip'] = str(u[i].PCIP)
				data[i]['size'] = u[i].Filesize
				data[i]['time'] = str(u[i].Datetime.strftime('%Y-%m-%d %H:%M'))
				# 时间格式化
				data[i]['key'] = u[i].code
		return HttpResponse(json.dumps(data), content_type="application/json")
		# django 使用 HttpResponse 返回json 的标准方式,content_type是标准写法