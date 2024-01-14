# Import standard packages
import pandas as pd
import numpy as np
# setting random state for reproducibility
SEED = 42
np.random.seed(SEED)

import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
pd.set_option('display.max_columns',100)

# set the default output to pandas
from sklearn import set_config
set_config(transform_output='pandas')

# Import modeling tools
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV


from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder

from sklearn.pipeline import Pipeline, make_pipeline

from sklearn.impute import SimpleImputer


from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import f1_score, recall_score, accuracy_score, precision_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay ,classification_report

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression # for classModel


from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier

from sklearn.neighbors import KNeighborsClassifier

from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector


import os
import joblib


from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

from sklearn.metrics import roc_auc_score, RocCurveDisplay

# plt.style.use(('ggplot','tableau-colorblind10'))

from sklearn.inspection import permutation_importance