from django.http import HttpResponse
from django.shortcuts import redirect, render
from youtubesearchpython import VideosSearch
from Toolbar.models import SearchText 
import requests
from bs4 import BeautifulSoup
import urllib.parse
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

def images(request):
    searchkey =  SearchText.objects.all().last()
    searchkey = str(searchkey)
    query = urllib.parse.quote_plus(searchkey)
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    image_elements = soup.find_all('img')
    image_urls = [img['src'] for img in image_elements]
    mydict={
        'input':searchkey,
        'images':image_urls[1:]   
    }
    print(mydict['images'])
    return render(request,'main.html',mydict)

def books(request):
    # if request.method=='POST':
    stxt = SearchText.objects.all().last()
    searchtxt = str(stxt)
    url = 'https://www.googleapis.com/books/v1/volumes?q=' + searchtxt
    r = requests.get(url)
    result = r.json()
    result_list = []
    for i in range(10):
        result_dict = {
            'title': result['items'][i]['volumeInfo']['title'],
            'subtitle': result['items'][i]['volumeInfo'].get('subtitle'),
            'description': result['items'][i]['volumeInfo'].get('description','...')[:200],
            'count': result['items'][i]['volumeInfo'].get('pageCount', '...'),
            'thumbnail': result['items'][i]['volumeInfo'].get('imageLinks', {}).get('thumbnail'),
            'preview': result['items'][i]['volumeInfo'].get('previewLink'),
        }
        result_list.append(result_dict)
    context = {
        'results': result_list,
        'input': searchtxt,
    }
    return render(request, 'main.html', context)

def all(request):
    searchkey =  SearchText.objects.all().last()
    searchkey = str(searchkey)
    mydict={
        'input':searchkey,
    }
    return render(request,'main.html',mydict)