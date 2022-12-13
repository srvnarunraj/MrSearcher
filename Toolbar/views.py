import os
from django.http import HttpResponse
from django.shortcuts import redirect, render
from youtubesearchpython import VideosSearch
from Toolbar.models import SearchText 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

def startup(request):
    return render(request,'index.html')

def search(request):
    stxt=request.POST['q']
    if stxt.isspace() == False and len(stxt)!=0:
        input = SearchText(Searchtext=stxt)
        input.save()
    inputval = {
        'input':input
    }
    return render(request,'main.html',inputval)

def videos(request):
    # if request.method =='POST':
            stxt = SearchText.objects.all().last()
            stxt=str(stxt)
        # stxt=request.POST['q']
            video = VideosSearch(str(stxt),limit=10)
            result_list=[]
            for i in video.result()['result']:
                result_dict = {
                    'input':stxt,
                    'title':i['title'],
                    'duration':i['duration'],
                    'thumbnails':i['thumbnails'][0]['url'],
                    'channel':i['channel']['name'],
                    'link':i['link'],
                    'views':i['viewCount']['short'],
                    'published':i['publishedTime'],
                }
                desc=''
                if i['descriptionSnippet']:
                    for j in i['descriptionSnippet']:
                        desc+=j['text']
                result_dict
                result_list.append(result_dict)
                context={
                    'results':result_list,
                    'input':stxt,
                }
            return render(request,'main.html',context)
        # else:
        #     return redirect('/')    
    # else:
    #     return redirect('/')

def images(request):
    searchkey =  SearchText.objects.all().last()
    searchkey = str(searchkey)
    mypath= "E:\\chromedriver.exe"
    myoptions = webdriver.ChromeOptions()
    myoptions.add_experimental_option('detach',True)
    s= Service(mypath)
    driver = webdriver.Chrome(options=myoptions,service=s)
    driver.get('https://images.google.com/')
    box=driver.find_element("xpath",'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    mykey=str(searchkey)
    box.send_keys(mykey)
    box.send_keys(Keys.ENTER)
    try:
        n=mykey
        pd='E:/Python Search Engine/MrSearch/static/images/'
        path = os.path.join(pd,n)
        os.mkdir(path)
    except:
        pass
    for i in range(1,21):
        try:
            img = driver.find_element('xpath','//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img').screenshot(path+'\img'+str(i)+'.png')
        except:
            pass
        searchtxt=searchkey
        x = 'E:\Python Search Engine\MrSearch\static\images\\'
            # searchtxt='Robot'
        url=x+searchtxt
        size = os.listdir(url)
        location=[]
        myurl='images//'+searchtxt+'//'
        for i in size:
            location.append(myurl+i+'')
        mydict={
            'size':size,
            'input':searchkey,
            'locate':location   
        }
    return render(request,'main.html',mydict)
        
