from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

def KMeansCoff(scaled_df):
  # Iterate over a range of k clusters to find the optimal number of clusters
  ks = range(2,11)
  sils = []
  inertias = []
  for k in ks:
    kmeans = KMeans(n_clusters=k, n_init = 'auto', random_state=42)
    kmeans.fit(scaled_df)
    sils.append(silhouette_score(scaled_df, kmeans.labels_))
    inertias.append(kmeans.inertia_)
  #plot inertias and silhouette scores for each number of clusters.
  fig, axes = plt.subplots(1,2, figsize=(15,5))
  axes[0].plot(ks, sils)
  axes[0].set_title('Silhouette Scores')
  axes[0].set_xticks(ks)
  axes[1].plot(ks, inertias)
  axes[1].set_title('Inertia')
  axes[1].set_xticks(ks);