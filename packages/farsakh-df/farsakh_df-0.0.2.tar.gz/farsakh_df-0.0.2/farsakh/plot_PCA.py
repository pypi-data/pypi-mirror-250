import plotly.express as px
import plotly.io as pio


import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn import set_config
set_config(transform_output='pandas')
pd.set_option('display.max_columns',100)


def update_scatter3d(fig):
    fig.update_traces({'marker':{'size':3}})
    fig.show(config={'scrollZoom':False})



def plot_PCA(preprocessor, X_train, y_train, X_test, y_test, color_target='target', pairplot = False):


  X = pd.concat([X_train,X_test], axis=0)

  y = pd.concat([y_train,y_test], axis=0)


  X_tf = preprocessor.fit_transform(X)



  # Instantiate PCA to make 3 principal components
  pca = PCA(n_components=3)
  # Create and define the principal components
  principal_components = pca.fit_transform(X_tf)


  # Concatenate principal components with target
  plot_df_pca = pd.concat([principal_components, y], axis=1)

  if pairplot == True:
    # Concatenate principal components with target
    plot_df_pca = pd.concat([principal_components, y], axis=1)
    # Plot with color coding based on target
    g_pca = sns.pairplot(data=plot_df_pca,  vars=principal_components.columns, hue='Training')
    g_pca.fig.suptitle('Visualizing First 3 PCs - Colored by Training', y=1.01);

  # Make a 3d scatter plot with a PC on each axis and color by the target
  # Change template style to plotly_dark
  fig = px.scatter_3d(plot_df_pca, x='pca0',y='pca1',z='pca2', width=800, height=600, color = color_target, template = 'plotly_dark')
  update_scatter3d(fig)

  return fig, pca


# ====================================================================
target = "Training"

preprocessor, X_train, y_train, X_test, y_test = preprocessor_maker(df, target, num_imputer='constant', fill_num = 0, cat_scale = True)

fig, pca_3 = plot_PCA(preprocessor, X_train, y_train, X_test, y_test, color_target = y_train.name)

# Sum of variance explained by 3 principal components
pca_3.explained_variance_ratio_.sum()
