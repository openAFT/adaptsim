from scipy import stats
import numpy as np
import adaptfx as afx

def sample_normal(mu, std, n, k):
    samples = np.random.normal(loc=mu, scale=std, size=(n,k))

    return samples

fit_samples = sample_normal(0.9, 0.04, 200, 6)

[shape_var, scale_var] = afx.fit_invgamma_prior(fit_samples)
[shape_std, scale_std] = afx.fit_invgamma_prior_std(fit_samples)

model_samples = sample_normal(0.9, 0.04, 1, 6)
afx.student_t(model_samples, shape_var, scale_var)
afx.student_t_std(model_samples, shape_std, scale_std)
