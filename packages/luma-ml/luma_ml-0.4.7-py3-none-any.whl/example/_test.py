import __local__
from sklearn.datasets import make_blobs, make_moons
import numpy as np

from luma.clustering.density import OPTICS, DENCLUE
from luma.visual.result import ClusterPlot


num = 100
X0, y0 = make_moons(n_samples=num, noise=0.03, random_state=42)
X1, y1 = make_blobs(n_samples=num, 
                    centers=[(-0.75,2.25), (1.0, -2.0)], 
                    cluster_std=0.3, random_state=42)
X2, y2 = make_blobs(n_samples=num, 
                    centers=[(2,2.25), (-1, -2.0)], 
                    cluster_std=0.3, random_state=42)

X = np.vstack((X0, X1, X2))
y = np.vstack((y0, y1 + 2, y2 + 4))

model = DENCLUE(h='auto',
              tol=1e-3,
              max_climb=100,
              min_density=0.0,
              sample_weight=None)

model.fit(X)

plot = ClusterPlot(estimator=model, X=X)
plot.plot()
