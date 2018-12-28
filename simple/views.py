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



#Routes
def contact_list(request):	
    return render(request, 'simple/simple.html')


def recos(request):
	gr_id = int(request.GET['i'])
	d = test(gr_id)
	return render(request, 'simple/result.html', d )





##Helper functions.
def getreadbooks(indices,b):
	#needs indices
	read = b.iloc[indices,:]
	#create dict object
	read['goodreads_book_id'] = read['goodreads_book_id'].apply(lambda x:'https://www.goodreads.com/book/show/'+str(x))
	ans = read[['book_id','goodreads_book_id', 'authors', 'title','image_url','small_image_url','average_rating']]
	#t = {'t':ans[['authors','title','image_url']].values.tolist()}
	t = ans[['authors','title','image_url','goodreads_book_id']].values.tolist()
	return t


def randomsample(n):
	M = pd.read_csv('pivot.csv')
	uidlist = np.array(M.user_id.values.tolist())
	np.random.shuffle(uidlist)
	res = {'d':uidlist[:n]}
	return res


def findksimilarusers(user_id, M, metric, k):
    similarities=[]
    indices=[]
    model_knn = NearestNeighbors(metric = metric, algorithm = 'brute') 
    model_knn.fit(M)

    distances, indices = model_knn.kneighbors(M.iloc[user_id-1, :].values.reshape(1, -1), n_neighbors = k+1)
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
	recos['goodreads_book_id'] = recos['goodreads_book_id'].apply(lambda x:'https://www.goodreads.com/book/show/'+str(x))
	ans = recos[['book_id','goodreads_book_id', 'authors', 'title','image_url','small_image_url','average_rating']]
	#d = {'c':ans[['authors','title','image_url']].values.tolist()}
	c=ans[['authors','title','image_url','goodreads_book_id']].values.tolist()
	return c

def test(u):
	b = pd.read_csv( 'books.csv' )
	M = pd.read_csv('pivot.csv')
	#h = pd.read_csv('hardcode.csv')
	row = M.iloc[u,:].nonzero()[0]
	read_indices = M.iloc[u,row][1:6].index.astype(int)
	#call the readbooks function I wrote.
	t = getreadbooks(read_indices,b)
	similarities,indices = findksimilarusers(u,M,'correlation',4)
	c = create_reco(similarities,indices,M,b,u) # fa = final answer
	fa = {'t':t,'c':c}
	return fa

