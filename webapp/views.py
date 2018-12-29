# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import urllib2
from bs4 import BeautifulSoup
from webapp.form import HomeForm
from django.shortcuts import render
from django.http import HttpResponse
from collections import defaultdict
import traceback

# Create your views here.

def get(request):
    if request.method=='GET':
        form=HomeForm()
        return render(request,'home.html',{'form':form})
    else:
        form=HomeForm()
        url=request.POST['SeedUrl']
        depth=int(request.POST['Depth'])
        if depth > 0:
            content,flag=crawl(url,depth)
            if type(content)!=list:
                return render(request,'content.html',{'content':content,'form':form,'flag':flag})
            else:
                return render(request,'content.html',{'content':content,'form':form,'flag':flag})
        else:
            return render(request,'content.html',{'error':"Enter depth greater than 0",'form':form,'flag':'Not Ok'})
        #return HttpResponse(html)

def crawl(baseurl,depth):
    try:
        html=urllib2.urlopen(baseurl).read()
        sp=BeautifulSoup(html,features="html.parser")
        urls=[baseurl]
        links=defaultdict(list)
        n=1
        url=baseurl
        while depth > 0:
            for img in sp.findAll('img',loadlate=True):
                link=img['loadlate']
                if link.startswith('http') or link.startswith('https'):
                    #html_tags=html_tags+'<img src="'+link+'" class="column" height="80">'
                    links[url].append(str(link))
                elif link=='#':
                    pass
                elif link=='/':
                    pass
                elif link.startswith('//'):
                    links[url].append(str(link))
                    #html_tags=html_tags+'<img src="http:'+link+'" class="column" height="80">'
                else:
                    #html_tags=html_tags+'<img src="'+baseurl+link+'" class="column" height="80">'
                    links[url].append(str(link))
            depth-=1
            url=baseurl+'&start='+str(n)
            urls.append(url)
            html=urllib2.urlopen(baseurl+'&start='+str(n)).read()
            n+=10       
#            print url
            #print links
        return dict(links),'OK'
    except:
        traceback.print_exc()
        return "Kinldy enter a valid Seed URL" ,'','Not Ok'


