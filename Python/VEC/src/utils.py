"""
"""

import numpy as np

import VEClib as algs
    
# initialize the stochastic block models with different parameter settings:        
def SBM_param_init_n_unequalcomm(K, N, lambda_n, alpha_n, r=0.5):
    """
    create SBM model parameters
    community weights are balanced = [r, 1-r]
    """
    SBM_params = {}
    if K>2:
        print 'this function cannot support K>2, warning'
    SBM_params['K'] = K
    SBM_params['N'] = N
    SBM_params['lambda_n'] = float(lambda_n)
    SBM_params['alpha'] = alpha_n/float(N)
    SBM_params['B0'] = lambda_n * np.eye(K) + (1-lambda_n)*np.ones((K,K)) 
    z = [r, 1.0-r]
    SBM_params['a'] = z
    return SBM_params

# initialize the stochastic block models with different parameter settings:        
def SBM_param_init_n_badQ(K, N, lambda_n, alpha_n, qr=1.0):
    """
    create SBM model parameters
    community weights are balanced = [1/k,...1/k]
    """
    SBM_params = {}
    SBM_params['K'] = K
    SBM_params['N'] = N
    SBM_params['lambda_n'] = float(lambda_n)
    SBM_params['alpha'] = alpha_n/float(N)
    SBM_params['B0'] = lambda_n * np.eye(K) + (1-lambda_n)*np.ones((K,K)) 
    SBM_params['B0'][1][1] = qr
    z = np.ones((1,K))
    SBM_params['a'] = z[0]/float(K)
    return SBM_params
            
#%%    
"""
updated 11-23-16
The following sub-block is a quick by-pass to the LDA approach for clustering
NOTE: the current by-pass uses the fast Gibbs Sampling approach
NOTE: the current implementation imported the bag-of-words model into 
"""
from sklearn.feature_extraction.text import CountVectorizer
import lda
def SBM_learn_deepwalk_lda(G, num_paths, length_path, emb_dim, rw_filename, emb_filename):
    """
    learning SBM model through deepwalk, using gensim package
    File I/O involved:
    first write all the randwalks on disc, then read to learn word2vec
    speed is relatively slow, but scales well to very large dataset
    Inputs:
    G: graph
    num_paths: number of random walks starting from each node
    length_path: length of each random walk
    rw_filename: file name to store the created corpus of sentences from graph G
    emb_filename: file name to store the learned embeddings of the nodes
    emb_dim: the dimensionality of the embeddings
    """
    print '1 building alias auluxy functions'
    S = algs.build_node_alias(G)    
    print '2 creating random walks'
    algs.create_rand_walks(S, num_paths, length_path, rw_filename)
    print '3 learning lda models'
    q = []
    f = open(rw_filename,'rb')
    for l in f:
        q.append(l.strip())
    vec = CountVectorizer(min_df=1)
    c = vec.fit_transform(q)
    names = vec.get_feature_names() # BoW feature names = nodes
    del q  # do this to make sure it minimizes the 
    model = lda.LDA(n_topics=emb_dim, n_iter=1000, random_state=1)
    model.fit(c)
    m = model.topic_word_
    # now lets construct a dictionary first:
    model_w2v = {}
    for i in range(len(names)):
        key = str(names[i])
        vector = m[:,i]
        model_w2v[key]=vector
    return model_w2v 
    
def SBM_learn_deepwalk_lda_another(G, num_paths, length_path, emb_dim, rw_filename, emb_filename):
    """
    learning SBM model through deepwalk, using gensim package
    File I/O involved:
    first write all the randwalks on disc, then read to learn word2vec
    speed is relatively slow, but scales well to very large dataset
    Inputs:
    G: graph
    num_paths: number of random walks starting from each node
    length_path: length of each random walk
    rw_filename: file name to store the created corpus of sentences from graph G
    emb_filename: file name to store the learned embeddings of the nodes
    emb_dim: the dimensionality of the embeddings
    """
    print '1 building alias auluxy functions'
    S = algs.build_node_alias(G)    
    print '2 creating random walks'
    algs.create_rand_walks(S, num_paths, length_path, rw_filename)
    print '3 learning lda models'
    q = []
    f = open(rw_filename,'rb')
    for l in f:
        q.append(l.strip())
    return q
#    vec = CountVectorizer(min_df=1)
#    c = vec.fit_transform(q)
#    names = vec.get_feature_names() # BoW feature names = nodes
#    del q  # do this to make sure it minimizes the 
#    model = lda.LDA(n_topics=emb_dim, n_iter=1000, random_state=1)
#    model.fit(c)
#    m = model.topic_word_
#    # now lets construct a dictionary first:
#    model_w2v = {}
#    for i in range(len(names)):
#        key = str(names[i])
#        vector = m[:,i]
#        model_w2v[key]=vector
#    return model_w2v 
    
    
def lda_to_mat(ldamodel, nodelist, emb_dim):
    # util functions to put dictionary model into matrices, row-wise indexed
    N = len(nodelist)
    X = np.zeros((N, emb_dim))
    for i in xrange(N):
        keyid = nodelist[i]
        if keyid in ldamodel:
            X[i,:] = ldamodel[keyid]
        else:
            print 'node', keyid, 'is missing'
    return X
def lda_to_mat_deepwalkdata(ldamodel, N, emb_dim):
    X = np.zeros((N, emb_dim))
    for i in xrange(N):
        keyid = str(i)+'10'
        if keyid in ldamodel:
            X[i,:] = ldamodel[keyid]
        else:
            print 'node', keyid, 'is missing'
    return X
def lda_normalize_embs(mat, option = 0):
    newmat = np.zeros(mat.shape)
    ## row-norms
    if option ==0:
        print 'option 0, no normalization'
        newmat = np.copy(mat)
    if option ==2:
        print 'option 2, l2 normalization'
        norms = np.linalg.norm(mat,  axis = 1)
        for i in range(len(mat)):
            newmat[i,:] = mat[i,:]/norms[i]
    if option ==1:
        print 'option 1, l1 normalization'
        norms = np.sum(mat, axis = 1)
        for i in range(len(mat)):
            newmat[i,:] = mat[i,:]/norms[i]
    return newmat
    
def clustering_embs(mat, K):
    ## apply k-means clustering algorithm to get labels
    from sklearn.cluster import KMeans
    k_means2 = KMeans(n_clusters=K, max_iter=100, precompute_distances=False)
    k_means2.fit(mat)
    y_hat = k_means2.labels_
    return y_hat    
    
def clustering_embs_noramlized(mat, K, option =0):
    ## apply k-means clustering algorithm to get labels
    from sklearn.cluster import KMeans
    ## row-norms, try L2 norm first
    if option ==0:
        print 'option 0, no normalization'
    if option ==2:
        print 'option 2, l2 normalization'
        norms = np.linalg.norm(mat,  axis = 1)
        for i in range(len(mat)):
            mat[i,:] = mat[i,:]/norms[i]
    if option ==1:
        print 'option 1, l1 normalization'
        norms = np.sum(mat, axis = 1)
        for i in range(len(mat)):
            mat[i,:] = mat[i,:]/norms[i]
    ##
    k_means2 = KMeans(n_clusters=K, max_iter=100, precompute_distances=False)
    k_means2.fit(mat)
    y_hat = k_means2.labels_
    return y_hat    

def maxfinding_embs_noramlized(mat, K, option =1):
    ## simply go and find the maximum
    ## row-norms, try L2 norm first
    if option ==0:
        print 'option 0, no normalization'
    if option ==2:
        print 'option 2, l2 normalization'
        norms = np.linalg.norm(mat,  axis = 1)
        for i in range(len(mat)):
            mat[i,:] = mat[i,:]/norms[i]
    if option ==1:
        print 'option 1, l1 normalization'
        norms = np.sum(mat, axis = 1)
        for i in range(len(mat)):
            mat[i,:] = mat[i,:]/norms[i]
    ##%%
    y_hat = []
    for i in range(len(mat)):
        y_hat.append(np.argmax(mat[i,:]))
#    k_means2 = KMeans(n_clusters=K, max_iter=100, precompute_distances=False)
#    k_means2.fit(mat)
#    y_hat = k_means2.labels_
    return y_hat  

#%% Unsure of the purpose of the following functions:
def cal_modularity(G, nodelist, y):
    m = G.size()
    m = float(m)
    Q = 0.0
    n = len(nodelist)
    k = []
    for e in nodelist:
        k.append(float(len(G[e])))
    for i in range(n):
        for j in range(i+1, n):
            if y[i] == y[j]:
                if G.has_edge(nodelist[i], nodelist[j]):
                    A = 1.0 - k[i]*k[j]/m
                else:
                    A = -1*k[i]*k[j]/m
                Q += A
    return 2*Q/m

def save_clusters_in_parallel(y, y_est, filename):
    """
    helper function to save the learned clustering results
    y - ground truth labels
    y_est - learned labels
    filename - to save results
    """
    f = open(filename, 'w')
    for i in y:
        f.write(str(y[i]) + ','+str(y_est[i])+'\n')
    f.close()
    return 1

def SBM_visual_tsne(labels, X):
    from . import tsne
    import pylab as Plot
    Y = tsne.tsne(X, 2)
    Plot.figure()
    Plot.scatter(Y[:, 0], Y[:, 1], 20, labels)
    Plot.show()
    return Y

def parse_txt_data(edgename, nodename):
    """
    additional helper fucntion for parsing graph data
    in txt files by Christy
    edgename: edge files,  each line: u,v  (node ids of a edge)
    nodename: node file, each line: nodeid, node-labels
    """
    model_params = {}
    G = nx.Graph()
    # add edges
    f = open(edgename, 'r')
    for l in f:
        c = l.split()
        G.add_edge(c[0], c[1], weight=1.0)
    f.close()
    # add nodes
    g = open(nodename, 'r')
    for l in g:
        c = l.split()
        G.node[c[0]]['community'] = c[1]
    g.close()
    # get overall graph info
    nds = G.nodes()
    model_params['N'] = len(nds)
    labels = [G.node[i]['community'] for i in nds]
    uK = set(labels)
    model_params['K'] = len(uK)
    return G, model_params

def get_true_labels(G):
    """
    only for Christy's format
    """
    nodeslist = G.nodes()
    labels = [G.node[i]['community'] for i in nodeslist]
    ln = [int(t) for t in labels]
    return ln

