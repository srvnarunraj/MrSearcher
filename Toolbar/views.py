from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
from youtubesearchpython import VideosSearch
from Toolbar.models import SearchText 
import requests,os
import json
import wikipediaapi
from bs4 import BeautifulSoup
import urllib.parse
import google.generativeai as genai
import markdown
import time

def getGeminiAnswers(request):
    query = request.GET.get('custom_data', 'Default Message')
    GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(query)
    return  JsonResponse({'message':markdown.markdown(response.text)})

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
    return redirect(all)
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

    api_key = os.environ.get('BOOKS_API_KEY')
    # Construct the API URL with the API key
    url = f'https://www.googleapis.com/books/v1/volumes?q={searchtxt}&key={api_key}'

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

    API_KEY =os.getenv('API_KEY')
    CX=os.getenv('CX')
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={searchkey}"

    response = requests.get(url)
    
    try:
        response.raise_for_status()  # Check for HTTP error
        data = json.loads(response.text)
        
        search_results = data.get('items', [])  # Check if 'items' key exists
        extracted_results = []
        for search_result in search_results:
            htmlTitle = search_result.get('htmlTitle', 'N/A')
            link = search_result.get('link', 'N/A')
            displayLink = search_result.get('displayLink', 'N/A')
            htmlSnippet = search_result.get('htmlSnippet', 'N/A')

            # Extract 'src' values from 'cse_thumbnail', 'cse_image', and 'og:image' lists
            cse_thumbnail = search_result.get('pagemap', {}).get('cse_thumbnail', [])
            thumbnail_src = cse_thumbnail[0]['src'] if cse_thumbnail else 'N/A'

            cse_image = search_result.get('pagemap', {}).get('cse_image', [])
            image_src = 'N/A'
            for img in cse_image:
                if 'src' in img:
                    image_src = img['src']
                    break

            metatags = search_result.get('pagemap', {}).get('metatags', [])
            ogimage_src = 'N/A'
            for meta in metatags:
                if 'og:image' in meta:
                    ogimage_src = meta['og:image']
                    break

            # Choose the first non-null image source
            imgsrc = thumbnail_src if thumbnail_src != 'N/A' else (image_src if image_src != 'N/A' else ogimage_src)

            extracted_results.append({
                'htmlTitle': htmlTitle,
                'link': link,
                'displayLink': displayLink,
                'htmlSnippet': htmlSnippet,
                'imgsrc': imgsrc,  # Store the chosen image source as 'imgsrc'
            })

        # Filter out results where 'imgsrc' is 'N/A'
        filtered_results = [result for result in extracted_results]
        mydict = {
            'input': searchkey,
            'extracted_results': filtered_results,
        }
        return render(request, 'main.html', mydict)
    finally:
        response.close()