from django.shortcuts import render, get_object_or_404, redirect

import numpy as np
import pandas as pd
import sklearn.metrics as metrics
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import correlation, cosine
from sklearn.metrics import pairwise_distances
from sklearn.metrics import mean_squared_error
from math import sqrt
import sys, os


def findksimilarusers(user_id, ratings, metric, k):
    similarities=[]
    indices=[]
    model_knn = NearestNeighbors(metric = metric, algorithm = 'brute') 
    model_knn.fit(ratings)

    distances, indices = model_knn.kneighbors(ratings.iloc[user_id-1, :].values.reshape(1, -1), n_neighbors = k+1)
    similarities = 1-distances.flatten()
    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i]+1 == user_id:
            continue;
            
    return similarities,indices

def create_reco(similarities,indices,M,b,u):
	t = M.loc[u]
	be = M.loc[indices.flatten()[1:][0]+1]
	r = be.align(t,join='left')
	r = np.array(r)
	df2 = pd.DataFrame(r).transpose()
	if len(df2[df2[0]>4]) < 5:
	    df2f = df2[df2[0]>3]
	else:
	    df2f = df2[df2[0]>4]
	df2f2 = df2[df2[1]>0]
	il =df2f[:5].index #il = items list
	ila = df2f.index #ila = items list all
	s = df2.iloc[ila,1] #start finding recos
	tempdf = pd.DataFrame(s)
	t2 = tempdf[tempdf[1]<1][:5].index
	recos = b.iloc[t2,:]
	ans = recos[['book_id','goodreads_book_id', 'authors', 'title','image_url','small_image_url','average_rating']]
	d = {'d':ans[['authors','title','image_url']].values.tolist()}
	return d

def test(u):
	b = pd.read_csv( 'books.csv' )
	M = pd.read_csv('pivot.csv')
	h = pd.read_csv('hardcode.csv')
	d = {'d':h[['authors','title','image_url']].values.tolist()}
	similarities,indices = findksimilarusers(u,M,'correlation',4)
	fa = create_reco(similarities,indices,M,b,u) # fa = final answer
	#probably can delete
	book_dict={
    'author':'Suzanne Collins',
    'title':'The Hunger Games',
    'img_url':'https://images.gr-assets.com/books/1447303603m/2767052.jpg'
    }
	return fa


def contact_list(request):
    d = test(40)
    
    return render(request, 'simple/simple.html',d)