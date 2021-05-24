import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

def ksiazkiviews(request):
    books = []
    url = 'https://www.googleapis.com/books/v1/volumes'

    if request.method == 'POST':
        params = {
            'q' : request.POST['search'],
            'maxResults' : request.POST['number'],
            'filter': request.POST['author'],
            'langRestrict': request.POST['lang'],
            'orderBy': request.POST['order'],
            'key': settings.BOOKS_API_KEY
        }
        r = requests.get(url, params=params).json()
        MaxResults = params['maxResults']
        MaxResults_count = int(MaxResults) * 2
        print(MaxResults_count)
        if r['totalItems'] == 0:
            messages.warning(request, 'Ta książka nie istnieje')

        else:
            results = r['items']
            books2 = []
            for result in results:
                xx = list(result['volumeInfo'].keys())
                books2.append(xx)
            check = [x for l in books2 for x in l]
            count_check = (check.count('authors')+check.count('publishedDate'))

            if count_check == MaxResults_count:
                for result in results:
                    books_data = {
                        "TOTALITEMS": r['totalItems'],
                        "ID" : result['id'],
                        "Tytuł" : result['volumeInfo']['title'],
                        "Autorzy" : result['volumeInfo']['authors'],
                        "Data_publikacji" : result['volumeInfo']['publishedDate'],
                        #"Liczba_stron" : result['volumeInfo']['pageCount'],
                        "Okładka" : result['volumeInfo']['imageLinks']['smallThumbnail'],
                        "Język" : result['volumeInfo']['language'],
                        "Link" : result['volumeInfo']['previewLink']
                    }
                    books.append((books_data))
            else:
                for result in results:
                    books_data = {
                        "TOTALITEMS": r['totalItems'],
                        "ID" : result['id'],
                        "Tytuł" : result['volumeInfo']['title'],
                        "Okładka" : result['volumeInfo']['imageLinks']['smallThumbnail'],
                        "Język" : result['volumeInfo']['language'],
                        "Link" : result['volumeInfo']['previewLink']
                    }
                    books.append((books_data))
                print("brak")
                messages.warning(request, 'Znaleziono książkę ale nie zawiera ona wszystkich informacji - Przepraszam nie mogę tego wyświetlić. Zmień kryteria wyszukiwania')
    context = {
        'books' : books
    }

    return render(request, 'ksiazkiviews.html', context)

