import math
import itertools
import pandas as pd

pd.set_option('display.width', 800)
pd.set_option("display.precision", 2)
pd.set_option('display.max_columns', None)


if __name__ == '__main__':
    df = pd.read_csv('movies_bd_v5.csv', sep=',', encoding='utf-8')
    print(f"Dataset contains {df.shape[0]} rows and {df.shape[1]} columns")
    print(f"Dataset columns: {', '.join(df.columns.tolist())}")
    print('Dataset column types:')
    print(df.dtypes)
    print('Dataset NAN-values distribution:')
    print(df.isnull().sum())
    df['profit'] = df['revenue'] - df['budget']
    df['release_date'] = pd.to_datetime(df['release_date'], format="%m/%d/%Y")
    df['month'] = df['release_date'].dt.strftime("%B")
    ans = {
        1: df.loc[df['budget'] == df['budget'].max()]['original_title'].item(),
        2: df.loc[df['runtime'] == df['runtime'].max()]['original_title'].item(),
        3: df.loc[df['runtime'] == df['runtime'].min()]['original_title'].item(),
        4: int(df['runtime'].mean().round()),
        5: int(df['runtime'].median().round()),
        6: df.loc[df['profit'] == df['profit'].max()]['original_title'].item(),
        7: df.loc[df['profit'] == df['profit'].min()]['original_title'].item(),
        8: len(df.loc[df['profit'] > 0]),
        9: df.loc[df['release_year'] == 2008].sort_values(by=['profit'], ascending=False).iloc[0]['original_title'],
        10: df.loc[df['release_year'].isin([2012, 2013, 2014])].sort_values(by=['profit'], ascending=True).iloc[0][
            'original_title'],
        11: df['genres'].str.split('|').apply(pd.Series).stack().value_counts().index[0],
        12: df.loc[df['profit'] > 0]['genres'].str.split('|').apply(pd.Series).stack().value_counts().index[0]}
    df['cast'] = df['cast'].str.split('|')
    df = df.explode(['cast'])
    df['genres'] = df['genres'].str.split('|')
    df = df.explode(['genres'])
    df['director'] = df['director'].str.split('|')
    df = df.explode(['director'])
    df['production_companies'] = df['production_companies'].str.split('|')
    df = df.explode(['production_companies'])
    tmp_df = df[['original_title', 'director', 'revenue']].drop_duplicates()
    ans[13] = tmp_df.groupby('director')['revenue'].sum().sort_values(ascending=False).index[0]
    tmp_df = df[['original_title', 'director', 'genres']].drop_duplicates()
    ans[14] = tmp_df.loc[tmp_df['genres'] == 'Action'].groupby('director')['original_title'].count().sort_values(
        ascending=False).index[0]
    ans[15] = df.loc[df['release_year'] == 2012][['cast', 'revenue']].drop_duplicates().groupby('cast')[
        'revenue'].sum().sort_values(ascending=False).index[0]
    tmp_df = df[['original_title', 'cast', 'budget']].drop_duplicates()
    ans[16] = tmp_df.loc[tmp_df['budget'] > tmp_df['budget'].mean()]['cast'].value_counts().index[0]
    tmp_df = df[['original_title', 'cast', 'genres']].drop_duplicates()
    ans[17] = tmp_df.loc[tmp_df['cast'] == 'Nicolas Cage']['genres'].value_counts().index[0]
    tmp_df = df.loc[df['production_companies'] == 'Paramount Pictures'][
        ['original_title', 'production_companies', 'profit']].drop_duplicates()
    ans[18] = tmp_df.loc[tmp_df['profit'] == tmp_df['profit'].min()]['original_title'].item()
    tmp_df = df[['original_title', 'release_year', 'revenue']].drop_duplicates()
    ans[19] = tmp_df.groupby('release_year')['revenue'].sum().sort_values(ascending=False).index[0]
    tmp_df = df.loc[df['production_companies'].str.contains('Warner Bros')][
        ['original_title', 'release_year', 'profit']].drop_duplicates()
    ans[20] = tmp_df.groupby('release_year')['profit'].sum().sort_values(ascending=False).index[0]
    tmp_df = df[['original_title', 'month', 'release_date']].drop_duplicates()
    ans[21] = tmp_df['month'].value_counts().index.tolist()[0]
    ans[22] = len(tmp_df.loc[tmp_df['release_date'].dt.month.isin([6, 7, 8])])
    tmp_df = df.loc[df['release_date'].dt.month.isin([12, 1, 2])][
        ['original_title', 'director', 'release_year']].drop_duplicates()
    ans[23] = tmp_df['director'].value_counts().index.tolist()[0]
    df['original_title_len'] = df['original_title'].str.len()
    tmp_df = df[['original_title', 'production_companies', 'original_title_len']].drop_duplicates()
    ans[24] = tmp_df.groupby('production_companies')['original_title_len'].mean().sort_values(ascending=False).index[0]
    df['overview_words'] = df['overview'].str.split(' ').apply(len)
    tmp_df = df[['original_title', 'production_companies', 'overview_words']].drop_duplicates()
    ans[25] = tmp_df.groupby('production_companies')['overview_words'].mean().sort_values(ascending=False).index[0]
    tmp_df = df[['original_title', 'release_year', 'vote_average']].drop_duplicates()\
        .sort_values(by=['vote_average'], ascending=False)
    top_vote_movies = tmp_df.iloc[0:math.floor((len(tmp_df) * 0.01))][['original_title', 'vote_average']]\
        .reset_index(drop=True)
    ans[26] = top_vote_movies.to_dict('records')
    actor_pairs = pd.Series([], dtype='object')
    tmp_df = df[['original_title', 'cast']].drop_duplicates().groupby('original_title')['cast'].apply(list)
    for x in tmp_df:
        if len(x) > 1:
            actor_pairs = pd.concat([actor_pairs, pd.Series(y for y in itertools.combinations(x, 2))], axis=0)
    most_frequent_actor_pairs = actor_pairs.value_counts()[actor_pairs.value_counts() ==
                                                           actor_pairs.value_counts().max()]
    ans[27] = most_frequent_actor_pairs.rename_axis('actor_pair').reset_index(name='count').to_dict('records')
    print("\nAnswers on questions:")
    for i, answer in ans.items():
        print(f"\t{i})\t{answer}")
