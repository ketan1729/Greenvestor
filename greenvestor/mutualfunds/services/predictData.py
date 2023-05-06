from datetime import datetime, time

from sklearn.linear_model import LinearRegression

from ..models import Returns

import matplotlib.pyplot as plt
import pandas as pd


def getPrediction(fund):
    returns_list = list(Returns.objects.select_related('fund').filter(fund__symbol=fund)
                        .order_by("year", "quarter")
                        .values("year", "quarter", "value"))

    df = pd.DataFrame(returns_list)

    # Prepare the data for regression
    X = df[['year', 'quarter']]
    y = df['value']

    # Create and fit the linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Create a range of quarters to make predictions for
    yl = []
    ql = []

    for i in range(2018, 2031):
        for j in range(4):
            yl.append(i)
            ql.append(j+1)

    next_quarters = pd.DataFrame({
        'year': yl,
        'quarter': ql,
    })

    # Add a predicted returns column to the range of quarters
    next_quarters['Predicted Returns'] = model.predict(next_quarters[['year', 'quarter']])

    # Plot the actual returns and predicted returns
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(df['year'].astype(str) + ' Q' + df['quarter'].astype(str), df['value'], label='Actual Returns')
    ax.plot(next_quarters['year'].astype(str) + ' Q' + next_quarters['quarter'].astype(str),
            next_quarters['Predicted Returns'], label='Predicted Returns')
    ax.set_xlabel('Quarter')
    ax.set_ylabel('Returns')
    ax.set_title('Actual and Predicted Returns')
    ax.legend()
    # plt.show()

    curr_datetime = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    base_path = "D:\\Rutgers\\Acads\\SE\\Project\\Code\\Greenvestor\\greenvestor" \
                "\\mutualfunds\\static\\mutualfunds\\media"
    image_name = "prediction_" + curr_datetime + ".jpg"
    plt.savefig(base_path + image_name)
    return base_path + image_name
