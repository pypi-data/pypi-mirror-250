def overView(df):
  for key in df:
    print(f"Value Counts for '{key}'")
    print('*'*30)

    print(df[key].value_counts())
    print('*'*30)

    print(f"Value type is '{df[key].dtypes}'")
    print('*'*30)
    print(f"Value decription:- \n{df[key].describe()}")
    print('*'*30)

    print(f"Value unique = {round((df[key].nunique()/len(df)*100),2)}%")
    print('*'*30)

    print(f"Value NaN = {round((df[key].isna().sum()/len(df)*100), 2)}%")
    print('*'*30)

    print('\n')
    print('/'*40)