from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector
# set the default output to pandas
from sklearn import set_config
set_config(transform_output='pandas')



def preprocessor_maker(df, target, num_imputer='mean', fill_num = 0, ord_features=[], ord_orders=[]
            , ord_imputer='constant', fill_ord='NA', cat_imputer='constant'
            ,fill_cat='NA',  random_state=42, num_scale = True, ord_scale = True, cat_scale = True , test_size=None):


    y = df[target]
    X = df.drop([target] , axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_state, test_size=test_size)

    indicator_arr = [0,0,0]

    if (len(X_train.select_dtypes('number').columns)):
        num_selector = make_column_selector(dtype_include='number')

        if num_imputer == 'constant':
            num_imputer1 = SimpleImputer(strategy='constant', fill_value = fill_num)
        else:
            num_imputer1 = SimpleImputer(strategy=num_imputer)

        if num_scale == True:
            scaler = StandardScaler()
            num_pipe = make_pipeline(num_imputer1, scaler)
        else:
            num_pipe = make_pipeline(num_imputer1)


        num_tuple = ('numeric',num_pipe, num_selector)

        indicator_arr[0] = 1



  # ================================================
    if len(ord_features):

        ord_cols = ord_features


        if ord_imputer == 'constant':
            impute_na_ord = SimpleImputer(strategy='constant', fill_value=fill_ord)
        else:
            impute_na_ord = SimpleImputer(strategy=ord_imputer)


        ord_encoder = OrdinalEncoder(categories=ord_orders)

        # # Making a final scaler to scale category #'s
        # scaler_ord = StandardScaler()

        if ord_scale == True:
            scaler_ord = StandardScaler()
            ord_pipe = make_pipeline(impute_na_ord, ord_encoder, scaler_ord)
        else:
            ord_pipe = make_pipeline(impute_na_ord, ord_encoder)

        # ord_pipe = make_pipeline(impute_na_ord, ord_encoder, scaler_ord)



        ord_tuple = ('ordinal', ord_pipe, ord_cols)
        # indicator_arr.append(ord_tuple)
        indicator_arr[1] = 1
  # ==================================================================

    # (New) Select columns with make_column_selector----------------------------------------------
    if (len(X_train.select_dtypes('object').columns)):
        # cat_selector = make_column_selector(dtype_include='object')

        if len(ord_features):
            ohe_cols = X_train.select_dtypes('object').drop(columns=ord_cols).columns


        else:
            ohe_cols = X_train.select_dtypes('object').columns


        if cat_imputer == 'constant':
            freq_imputer = SimpleImputer(strategy='constant', fill_value=fill_cat)
        else:
            freq_imputer = SimpleImputer(strategy=cat_imputer)
            ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')


        if cat_scale == True:
            scaler_cat = StandardScaler()
            cat_pipe = make_pipeline(freq_imputer, ohe, scaler_cat)
        else:
            cat_pipe = make_pipeline(freq_imputer, ohe)


        cat_tuple = ('categorical',cat_pipe, ohe_cols)
        indicator_arr[2] = 1


  # =======================================================================


    if indicator_arr[0] == 1 and indicator_arr[1] == 1 and indicator_arr[2] == 1:
        all_tuple = [num_tuple, ord_tuple, cat_tuple]

    elif indicator_arr[0] == 1 and indicator_arr[1] == 1 and indicator_arr[2] == 0:
        all_tuple = [num_tuple, ord_tuple]

    elif indicator_arr[0] == 1 and indicator_arr[1] == 0 and indicator_arr[2] == 1:
        all_tuple = [num_tuple, cat_tuple]

    elif indicator_arr[0] == 0 and indicator_arr[1] == 1 and indicator_arr[2] == 1:
        all_tuple = [ord_tuple, cat_tuple]

    elif indicator_arr[0] == 1 and indicator_arr[1] == 0 and indicator_arr[2] == 0:
        all_tuple = [num_tuple]

    elif indicator_arr[0] == 0 and indicator_arr[1] == 0 and indicator_arr[2] == 1:
        all_tuple = [cat_tuple]

    elif indicator_arr[0] == 0 and indicator_arr[1] == 1 and indicator_arr[2] == 0:
        all_tuple = [ord_tuple]

    else:
        print('Error')



    preprocessor = ColumnTransformer(all_tuple, verbose_feature_names_out=False)

    return preprocessor, X_train, y_train, X_test, y_test

