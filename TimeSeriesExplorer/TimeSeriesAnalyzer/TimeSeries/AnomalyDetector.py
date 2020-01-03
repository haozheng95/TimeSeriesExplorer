import numpy as np
from scipy import stats

def get_outliers(samples, threshold=0.05):
    '''
    :param samples: np.array
    :return: outliers: np.array
    '''
    mu = np.mean(samples)
    sigma = np.std(samples)
    prob = stats.norm.pdf(samples, mu, sigma)
    prob_mu = np.mean(prob)
    prob_sigma = np.std(prob)
    prob_prob = stats.norm.pdf(prob, prob_mu, prob_sigma)
    outliers_indices = prob_prob < threshold

    return outliers_indices

