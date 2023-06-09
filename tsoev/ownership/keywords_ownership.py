import numpy as np
import pandas as pd
from api.moz import get_url_metrics

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def test_ranking_pos():
    df = pd.read_csv('semrush file.csv')
    df.head(3)

    index_list = []
    for kw in df['Keyword'].unique():
        if df['Keyword'].tolist().count(kw) == 1:
            index = df[df['Keyword'] == kw].index[0]
            index_list.append(index)
        else:
            index = df[df['Keyword'] == kw].sort_values(by='Position').index[0]
            index_list.append(index)

    result_df = df[df.index.isin(index_list)]
    return result_df


def insert_pa_data(df):
    for index, row in df.iterrows():
        moz_url_metric = get_url_metrics([row[1]])  # url = row[1]
        if moz_url_metric is None:
            continue
        df.loc[index, 'PA'] = moz_url_metric[0]['upa']
    return df


def get_ownership_data(filtered_df):
    """ Method 2 - Based on Keyword Ownership Score"""
    # Generate expectations
    for kw in filtered_df['Keyword'].unique():

        subdf = filtered_df[filtered_df['Keyword'] == kw]

        for col in ['Position', 'Traffic', 'PA']:  # used to be Search Vol, Keyword Difficulty, PA

            mean = subdf[col].mean()
            if mean != 0:
                values = []
                if col == 'Position':
                    for i in subdf.index:
                        print("[get_ownership_data] >>>>>>>>>>>>: ", subdf[col][i], mean)
                        values.append(1 - float(subdf[col][i]) / mean)
                else:
                    for i in subdf.index:
                        values.append(float(subdf[col][i]) / mean)

                index = subdf.index.tolist()
                filtered_df.loc[index, '% of Avg ' + col] = values
            else:
                filtered_df.loc[:, '% of Avg ' + col] = [0] * len(filtered_df)

    # Assign weight to each category and generate weighted values
    weighted = []
    for i in filtered_df.index:
        value = filtered_df['% of Avg Position'][i] * 0.3 + \
                filtered_df['% of Avg Traffic'][i] * 0.4 + \
                filtered_df['% of Avg PA'][i] * 0.3

        weighted.append(value)

    filtered_df.loc[:, 'Weighted Value'] = weighted

    # Generate the Score
    filtered_df.loc[:, 'Keyword Ownership Score'] = 27 * np.log(filtered_df['Weighted Value']) + 100
    filtered_df.loc[:, 'Keyword Ownership Score'] = filtered_df['Keyword Ownership Score'].round(
        0)  # [0] * len(filtered_df)

    return filtered_df
