from django.shortcuts import render, get_object_or_404, redirect
import numpy as np
import pandas as pd
import sklearn.metrics as metrics
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import correlation, cosine
from sklearn.metrics import pairwise_distances
from sklearn.metrics import mean_squared_error
from math import sqrt
import sys
import os

# Used https://yapf.now.sh/ to reformat code to pep8.

# Routes - Basic routes just to display a home and results page.
def home(request):
    return render(request, 'simple/simple.html')


def recos(request):
    user_id = int(request.GET['i'])
    d = recommend(user_id)
    return render(request, 'simple/result.html', d)


# Helper functions.
def recommend(user_id):
    books = pd.read_csv('books.csv')
    pivot_data = pd.read_csv('pivot.csv')
    row = pivot_data.iloc[user_id, :].nonzero()[0]
    read_indices = pivot_data.iloc[user_id, row][1:6].index.astype(int)

    #Get list of books user already read and liked
    t = getreadbooks(read_indices, books)
    #find similar users
    similarities, indices = findksimilarusers(user_id, pivot_data,
                                              'correlation', 4)
    #use similar users to get recommendations
    c = create_reco(similarities, indices, pivot_data, books,
                    user_id)  # fa = final answer
    # combine list of already read books and recommendations
    fa = {'t': t, 'c': c}
    return fa


def getreadbooks(indices, books):
    read = books.iloc[indices, :]  #get list of read books
    # prep df for hyperlinking in view
    read['goodreads_book_id'] = read['goodreads_book_id'].apply(
        lambda x: 'https://www.goodreads.com/book/show/' + str(x))
    ans = read[[
        'book_id', 'goodreads_book_id', 'authors', 'title', 'image_url',
        'small_image_url', 'average_rating'
    ]]
    #turn results into a list to be appended to the Django context dict var
    t = ans[['authors', 'title', 'image_url',
             'goodreads_book_id']].values.tolist()
    return t


def findksimilarusers(user_id, pivot_data, metric, k):
    similarities = []
    indices = []
    model_knn = NearestNeighbors(metric=metric, algorithm='brute')
    model_knn.fit(pivot_data)

    distances, indices = model_knn.kneighbors(
        pivot_data.iloc[user_id - 1, :].values.reshape(1, -1),
        n_neighbors=k + 1)
    similarities = 1 - distances.flatten()
    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i] + 1 == user_id:
            continue

    return similarities, indices


def create_reco(similarities, indices, pivot_data, b, u):
    t = pivot_data.loc[u]
    be = pivot_data.loc[indices.flatten()[1:][0] + 1]
    r = be.align(t, join='left')
    r = np.array(r)
    df2 = pd.DataFrame(r).transpose()
    if len(df2[df2[0] > 4]) < 5:
        df2f = df2[df2[0] > 3]
    else:
        df2f = df2[df2[0] > 4]
    df2f2 = df2[df2[1] > 0]
    il = df2f[:5].index  #il = items list
    ila = df2f.index  #ila = items list all
    s = df2.iloc[ila, 1]  #start finding recos
    tempdf = pd.DataFrame(s)
    t2 = tempdf[tempdf[1] < 1][:5].index
    recos = b.iloc[t2, :]
    recos['goodreads_book_id'] = recos['goodreads_book_id'].apply(
        lambda x: 'https://www.goodreads.com/book/show/' + str(x))
    ans = recos[[
        'book_id', 'goodreads_book_id', 'authors', 'title', 'image_url',
        'small_image_url', 'average_rating'
    ]]
    #d = {'c':ans[['authors','title','image_url']].values.tolist()}
    c = ans[['authors', 'title', 'image_url',
             'goodreads_book_id']].values.tolist()
    return c


#Unused function, left in there in case we want to shuffle things in the future.
def randomsample(n):
    pivot_data = pd.read_csv('pivot.csv')
    uidlist = np.array(pivot_data.user_id.values.tolist())
    np.random.shuffle(uidlist)
    res = {'d': uidlist[:n]}
    return res
