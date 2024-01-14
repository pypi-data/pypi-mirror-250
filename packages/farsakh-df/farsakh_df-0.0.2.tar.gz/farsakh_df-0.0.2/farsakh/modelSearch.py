
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression # for classModel


from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier

from sklearn.neighbors import KNeighborsClassifier

from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.pipeline import make_pipeline

from .evaluate_regression import evaluate_regression


def modelSearch(preprocessor, X_train, y_train, X_test, y_test, model_type="num", random_state=42):
    if model_type == 'num':
        lin_reg = LinearRegression()
        dec_tree = DecisionTreeRegressor(random_state=random_state)
        bagreg = BaggingRegressor(random_state=random_state)
        rf = RandomForestRegressor(random_state=random_state)

        arrNum = [lin_reg, dec_tree, bagreg, rf]

        for model in arrNum:
            model_name = model.__class__.__name__
            model_selected_pip = make_pipeline(preprocessor, model, memory=model_name)
            model_selected_pip.fit(X_train, y_train)
            print("\n")
            print("\n")
            print(":" * 50)
            print("Model Name:", model_name)
            evaluate_regression(model_selected_pip, X_train, y_train, X_test, y_test)
            print(":" * 50)
            print("\n")
            print("\n")

    elif model_type == 'class':
        dec_tree = DecisionTreeClassifier(random_state=random_state)
        knn = KNeighborsClassifier()
        logreg = LogisticRegression(random_state=random_state, C=1000)
        bagregClass = BaggingClassifier(random_state=random_state)
        rfc = RandomForestClassifier(random_state=random_state)

        arrClass = [dec_tree, knn, logreg, bagregClass, rfc]

        for model in arrClass:
            model_name = model.__class__.__name__
            model_selected_pip = make_pipeline(preprocessor, model, memory=model_name)
            model_selected_pip.fit(X_train, y_train)
            print("\n")
            print("\n")
            print(":" * 50)
            print("Model Name:", model_name)
            evaluate_classification(model_selected_pip, X_train, y_train, X_test, y_test)
            print(":" * 50)
            print("\n")
            print("\n")

