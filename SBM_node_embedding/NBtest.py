"""
Create Figure, compare three algorithms across

collecting results from nmi, ccr, ars, and modularity
"""

import pickle
import itertools
import networkx as nx
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from src import SBMlib as SBM
from src import VEClib as algs
from src import ABPlib as ABP

# MACRO parameter setting
rw_filename = 'sentences.txt'
emb_filename = 'emb.txt'
num_paths = 10
length_path = 60
emb_dim = 50
winsize = 8

if __name__ == '__main__':
    # generating multiple graphs for the same parameter setting
    rand_tests = 5
    # setting storage space for results
    nmi_arry = {}
    ccr_arry = {}
    ars_arry = {}
    # parameter setting
    c_array = [4.0, 5.0, 6.0, 8.0, 10.0, 15.0, 20.0]
    K_array = [2]  # number of communities
    N_array = [1000] # number of nodes
    lambda_array = [0.9] # B0 = lambda*I + (1-lambda)*ones(1,1)
    # scanning through parameters
    for c, K, N, lambda_n in itertools.product(c_array, K_array, N_array, lambda_array):
        print 'K:', K, 'N:', N, 'c:', c, 'lambda:', lambda_n
        model_sbm1 = SBM.SBM_param_init1(K, N, lambda_n, c)
        for rand in range(rand_tests):
            print 'Beginning iteration', rand+1, 'of', rand_tests, '...'
            strsub1 = 'K'+str(K)+'N'+str(N)+'c'+str(c)+'la'+str(lambda_n)+'rd'+str(rand) # for saving results
            # simulate graph
            G = SBM.SBM_simulate_fast(model_sbm1)
            ln, nodeslist = SBM.get_label_list(G)
            # algo1: proposed deepwalk algorithm
            print 'starting VEC algorithm...'
            model_w2v = algs.SBM_learn_deepwalk_1(G, num_paths, length_path, emb_dim, rw_filename, emb_filename, winsize)
            X = model_w2v[nodeslist]
            k_means = KMeans(n_clusters=K, max_iter=100, precompute_distances=False)
            k_means.fit(X)
            y_our = k_means.labels_
            nmi_arry, ccr_arry, ars_arry = algs.summary_res(nmi_arry, ccr_arry, ars_arry, ln, y_our, 'deep', 'c', c, rand)
            # algo2: spectral clustering
            A = nx.to_scipy_sparse_matrix(G)
            print 'starting spectral clustering...'
            sc = SpectralClustering(n_clusters=K, affinity='precomputed', eigen_solver='arpack')
            sc.fit(A)
            y_sc = sc.labels_
            nmi_arry, ccr_arry, ars_arry = algs.summary_res(nmi_arry, ccr_arry, ars_arry, ln, y_sc, 'sc', 'c', c, rand)
            # algo3: belief propogation
            print 'starting ABP algorithm...'
            r = 3
            m, mp, lambda1 = ABP.abp_params(model_sbm1)
            y_abp = ABP.SBM_ABP(G, r, lambda1, m, mp)
            nmi_arry, ccr_arry, ars_arry = algs.summary_res(nmi_arry, ccr_arry, ars_arry, ln, y_abp, 'abp', 'c', c, rand)
    savename = 'exp101.pkl'
    res = [nmi_arry, ccr_arry, ars_arry]
    pickle.dump(res, open(savename, 'wb'), protocol=2)

###################
### use the following script to retrivle data and make new pltos
#import SBMmodels as SBM
#import networkx as nx
#from sklearn.cluster import KMeans
#from sklearn.cluster import SpectralClustering
#from sklearn import metrics
#import time
#import itertools
#import scipy
#import numpy as np
#import math
#import pickle
#
# ############ def plot_res_3_new(res, thr_wk, thr_hd,K):
#fname = 'exp1.pkl'
#res = pickle.load(open(fname, 'rb'))
#nmi_arry = res[0]
#ccr_arry = res[1]
#ars_arry = res[2]
#
#thr_wk  = 0.395
#thr_pr  = 1.574
#thr_hd  = 4.28
#import matplotlib.pyplot as plt
#nmi = res[0]
#ccr = res[1]
#ars = res[2]
#tm = nmi['deep'].keys()
#param = tm[0].split('-')[0]
#x_array = [float(z.split('-')[1].strip()) for z in tm ]
#x_array = sorted(x_array)
#tm = [param + '- ' + str(v) for v in x_array]
## get nmi for three algs, mean and std
#nmi_deep_mean = [np.mean(nmi['deep'][z].values()) for z in tm]
#nmi_sc_mean = [np.mean(nmi['sc'][z].values()) for z in tm]
#nmi_abp_mean = [np.mean(nmi['abp'][z].values()) for z in tm]
#nmi_deep_std = [np.std(nmi['deep'][z].values()) for z in tm]
#nmi_sc_std = [np.std(nmi['sc'][z].values()) for z in tm]
#nmi_abp_std = [np.std(nmi['abp'][z].values()) for z in tm]
## get ccr for three algs
#ccr_deep_mean = [np.mean(ccr['deep'][z].values()) for z in tm]
#ccr_sc_mean = [np.mean(ccr['sc'][z].values()) for z in tm]
#ccr_abp_mean = [np.mean(ccr['abp'][z].values()) for z in tm]
#ccr_deep_std = [np.std(ccr['deep'][z].values()) for z in tm]
#ccr_sc_std = [np.std(ccr['sc'][z].values()) for z in tm]
#ccr_abp_std = [np.std(ccr['abp'][z].values()) for z in tm]
## plot
## x - ccr, o - nmi
## b- - deep, r-- - sc, g-. - adp
#plt.figure(1, figsize=(10, 6))
#
#plt.errorbar(x_array, nmi_deep_mean, yerr=nmi_deep_std, fmt='bo-.', markersize=8,linewidth= 1.5)
#plt.errorbar(x_array, nmi_sc_mean, yerr=nmi_sc_std, fmt='rs-.', markersize=8,linewidth= 1.5)
#plt.errorbar(x_array, nmi_abp_mean, yerr=nmi_abp_std, fmt='g<-.', markersize=8,linewidth= 1.5)
#
#plt.errorbar(x_array, ccr_deep_mean, yerr=ccr_deep_std, fmt='bo-', markersize=8,linewidth= 1.5)
#plt.errorbar(x_array, ccr_sc_mean, yerr=ccr_sc_std, fmt='rs-', markersize=8,linewidth= 1.5)
#plt.errorbar(x_array, ccr_abp_mean, yerr=ccr_abp_std, fmt='g<-', markersize=8,linewidth= 1.5)
#
#plt.legend(['NMI-New', 'NMI-SC', 'NMI-ABP', 'CCR-New', 'CCR-SC', 'CCR-ABP'], loc=0)
#plt.xlabel(param)
#plt.xlim(x_array[0]-0.1,x_array[-1]+0.1)
#plt.ylim(-0.05,1.05)
#plt.plot([thr_wk, thr_wk],[0,1],'k--', linewidth= 2.5)
#plt.plot([thr_pr, thr_pr], [0,1], 'k--', linewidth = 2.5)
#plt.plot([thr_hd, thr_hd], [0,1], 'k--', linewidth = 2.5)
##    plt.plot(x_array, [1./float(K)]*len(x_array), 'r--')
##    plt.plot(x_array, [1.0]*len(x_array), 'r--')
#plt.show()
#figurename = 'exp1'
#plt.savefig(figurename+'.eps',bbox_inches='tight', format='eps')
#plt.savefig(figurename+'.png',bbox_inches='tight', format='png')
##    return x_array
