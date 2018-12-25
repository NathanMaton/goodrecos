from django.shortcuts import render, get_object_or_404, redirect

def contact_list(request):
    book_dict={
    'author':'Suzanne Collins',
    'title':'The Hunger Games',
    'img_url':'https://images.gr-assets.com/books/1447303603m/2767052.jpg'
    }
    return render(request, 'simple/simple.html',book_dict)