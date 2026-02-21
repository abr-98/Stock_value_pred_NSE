from sklearn.linear_model import LinearRegression

def linear_explaination(X, y):

    model = LinearRegression()
    model.fit(X, y)

    coefficients = model.coef_
    feature_names = X.columns

    explanation = dict(zip(feature_names, coefficients))

    return explanation
    