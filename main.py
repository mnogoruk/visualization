import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

EUROPEAN_QUALITY = {"min alcohol": 8.5, "max volatile acidity": 1.2, "min pH": 2.8, "max pH": 3.6}


class Filter:

    def __init__(self, data_frame):
        self.data_frame = data_frame

    def gte(self, field, value):
        return Filter(self.data_frame[self.data_frame[field] >= value])

    def gt(self, field, value):
        return Filter(self.data_frame[self.data_frame[field] > value])

    def lte(self, field, value):
        return Filter(self.data_frame[self.data_frame[field] <= value])

    def lt(self, field, value):
        return Filter(self.data_frame[self.data_frame[field] < value])

    def get(self):
        return self.data_frame


def read_dataframe():
    while_wine_dataset_url = 'https://raw.githubusercontent.com/mnogoruk/visualization/main/winequality-white.csv'
    red_wine_dataset_url = 'https://raw.githubusercontent.com/mnogoruk/visualization/main/winequality-red.csv'

    white_wine_data_frame = pd.read_csv(while_wine_dataset_url, delimiter=';', error_bad_lines=False)
    red_wine_data_frame = pd.read_csv(red_wine_dataset_url, delimiter=';', error_bad_lines=False)

    white_wine_data_frame['type'] = 'white'
    red_wine_data_frame['type'] = 'red'

    merged_data_frame = pd.concat([white_wine_data_frame, red_wine_data_frame], ignore_index=True)
    return merged_data_frame


def avg_alcohol_per_different_wine_types(dataframe):
    dry_wine = Filter(dataframe).lte('residual sugar', 3).get()
    semi_dry_wine = Filter(dataframe).gt('residual sugar', 3).lte('residual sugar', 7).get()
    semi_sweet_wine = Filter(dataframe).gt('residual sugar', 7).lte('residual sugar', 12).get()
    sweet_wine = Filter(dataframe).gt('residual sugar', 12).get()
    avg_alcohol = pd.DataFrame(data={
        'type': ['dry wines', 'semi-dry wines', 'semi-sweet wines', 'sweet wines'],
        'average alcohol': [dry_wine['alcohol'].mean(), semi_dry_wine['alcohol'].mean(),
                            semi_sweet_wine['alcohol'].mean(), sweet_wine['alcohol'].mean()]})
    fig = px.bar(avg_alcohol, x='type', y='average alcohol')
    fig.show()
    # sns.barplot(x='type', y='average alcohol, %', data=avg_alcohol)


def corr_matrix(dataframe):
    df_correlation = dataframe.corr()
    fig, axes = plt.subplots(ncols=2, figsize=(16, 6))
    sns.heatmap(ax=axes[0], data=df_correlation, vmin=-1, vmax=1, annot=True)
    sns.heatmap(ax=axes[1], data=df_correlation[['quality']].sort_values(by='quality', ascending=False, key=abs),
                annot=True)
    fig.show()


def part_of_european_quality(dataframe):
    european_quality_wines = Filter(dataframe) \
        .gt('alcohol', EUROPEAN_QUALITY["min alcohol"]) \
        .lt('volatile acidity', EUROPEAN_QUALITY['max volatile acidity']) \
        .gt('pH', EUROPEAN_QUALITY['min pH']) \
        .lt('pH', EUROPEAN_QUALITY['max pH']).get()
    european_quality_wines_amount = european_quality_wines[['type']].count()['type']
    df_amount = dataframe[['type']].count()['type']
    not_european_quality_wines_amount = df_amount - european_quality_wines_amount
    q_df = pd.DataFrame(data={
        'type': ['вина не европейского качества', "вина европейского качества"],
        'amount': [not_european_quality_wines_amount, european_quality_wines_amount]
    })

    european_quality_wines_mean_quality = european_quality_wines['quality'].mean()
    not_european_quality_wines_mean_quality = \
        dataframe[~dataframe.apply(tuple, 1).isin(european_quality_wines.apply(tuple, 1))][
            'quality'].mean()
    fig, ax = plt.subplots(figsize=(16, 6))
    df = pd.DataFrame(data={
        "type": ('оценка для вин с европейским качеством', 'оценка для вин без европейского качества'),
        "quality": (european_quality_wines_mean_quality, not_european_quality_wines_mean_quality)
    })
    sns.barplot(ax=ax, data=df, x='type', y='quality')
    fig.show()
    fig = px.pie(q_df, values='amount', names='type', width=700)
    fig.show()


def main():
    dataframe = read_dataframe()
    avg_alcohol_per_different_wine_types(dataframe)
    corr_matrix(dataframe)
    part_of_european_quality(dataframe)


if __name__ == '__main__':
    main()
