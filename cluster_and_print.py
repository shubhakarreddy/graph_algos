import pickle
import sys
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

with open(sys.argv[1]) as f:
    snv_vectors = pickle.load(f)

embedded_vecs = []
for read in snv_vectors:
    if len(snv_vectors[read]) != 0:
        for entry in snv_vectors[read]:
            vector = entry[2].split()
            embedded_vecs += [[0 if x == '.' else 1 for x in vector]]

print len(embedded_vecs)

km_cls = KMeans(n_clusters=3, random_state=0, n_jobs=-3).fit(embedded_vecs).predict(embedded_vecs)



# reduced = TSNE(n_components=2, random_state=0, verbose=0).fit_transform(embedded_vecs)
# plt.scatter(reduced[:,0], reduced[:,1], c=km_cls, s=2, alpha=0.4, edgecolors="none")
