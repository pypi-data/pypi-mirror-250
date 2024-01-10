import __local__
from luma.clustering.affinity import AffinityPropagation
from luma.visual.result import ClusterPlot

from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=500, centers=7, cluster_std=1.0, random_state=10)

ap = AffinityPropagation()
ap.fit(X)

plot = ClusterPlot(estimator=ap, X=X, cmap='RdYlBu')
plot.plot()

