from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

BASE_CRAIGS_LIST_URL = 'https://sfbay.craigslist.org/search/hhh?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)

    final_url = BASE_CRAIGS_LIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, features='html.parser')
    post_listing = soup.find_all('li', {'class': 'result-row'})

    final_posting = []

    for post in post_listing:
        post_title = str(post.find(class_='result-title').text)[:20]
        post_url = post.find('a').get('href')

        if  post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_url = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            print(post_image_url)
            post_image_url = BASE_IMAGE_URL.format(post_image_url)
            print(post_image_url)
        else:
            post_image_url = 'https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500'
        final_posting.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_posting': final_posting
    }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)