from django.http import HttpResponse
from django.shortcuts import redirect, render
from youtubesearchpython import VideosSearch
from Toolbar.models import SearchText 

def startup(request):
    return render(request,'index.html')

def search(request):
    stxt=request.POST['q']
    if stxt.isspace() == False and len(stxt)!=0:
        input = SearchText(SearchText=stxt)
        input.save()
    return render(request,'header.html')

def videos(request):
    # if request.method =='POST':
            stxt = SearchText.objects.latest('SearchText')
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
                    'results':result_list
                }
            return render(request,'main.html',context)
        # else:
        #     return redirect('/')    
    # else:
    #     return redirect('/')

def images(request):
    stxt = SearchText.objects.latest('SearchText')
    return HttpResponse(stxt)
