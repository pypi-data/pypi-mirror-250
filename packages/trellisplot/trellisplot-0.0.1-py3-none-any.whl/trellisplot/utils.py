import numpy as np
from scipy.stats import gaussian_kde

def jitter(x, y):
    '''x is a (n, ) numpy array. Need to add a bit of jitter so the scatter plot doesn't all show up on the same place.'''
    x= np.array(x)
    y= np.array(y).astype(float)

    envelopes = []
    max_kernel = 1
    random_generate = lambda a: np.random.uniform(-a, a)
    
    for unique_val in np.unique(x):
        y_subset = y[x==unique_val]
        
        kde = gaussian_kde(y_subset)
        kde_y_subset = kde(y_subset)
        envelopes= envelopes + list(kde_y_subset)

    
    envelopes = np.array(envelopes)
    envelopes = envelopes/(2*envelopes.max())*0.75
    x = x + random_generate(envelopes)

    return x