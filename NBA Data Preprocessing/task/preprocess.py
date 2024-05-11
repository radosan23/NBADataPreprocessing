import pandas as pd
import os
import requests


def get_data():
    if not os.path.exists('../Data'):
        os.mkdir('../Data')
    if 'nba2k-full.csv' not in os.listdir('../Data'):
        url = "https://www.dropbox.com/s/wmgqf23ugn9sr3b/nba2k-full.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/nba2k-full.csv', 'wb').write(r.content)


def clean_data(path):
    df = pd.read_csv(path)
    df['b_day'] = pd.to_datetime(df.b_day, format='%m/%d/%y')
    df['draft_year'] = pd.to_datetime(df.draft_year, format='%Y')
    df['team'] = df['team'].fillna('No Team')
    df['height'] = df['height'].apply(lambda x: x.split()[2]).astype(float)
    df['weight'] = df['weight'].apply(lambda x: x.split()[3]).astype(float)
    df['salary'] = df['salary'].apply(lambda x: x[1:]).astype(float)
    df['country'] = df['country'].where(df.country == 'USA', 'Not-USA')
    df['draft_round'] = df['draft_round'].replace('Undrafted', '0')
    return df


def feature_data(df):
    df['version'] = pd.to_datetime(df['version'], format='NBA2k%y')
    df['age'] = (df['version'].dt.year - df['b_day'].dt.year)
    df['experience'] = (df['version'].dt.year - df['draft_year'].dt.year)
    df['bmi'] = df['weight'] / df['height'] ** 2
    df = df.drop(columns=['version', 'b_day', 'draft_year', 'weight', 'height'])
    df = df.drop(columns=(df.columns[(df.nunique() > 50) & (df.dtypes == object)]))
    return df


def multicol_data(df, threshold=0.5):
    corr = df.drop(columns='salary').corr(numeric_only=True).unstack()
    corr_pairs = corr[abs(corr) > threshold].index
    corr_pairs = set([tuple(sorted(x)) for x in corr_pairs if x[0] != x[1]])
    for pair in corr_pairs:
        if pair[0] in df.columns and pair[1] in df.columns:
            df = df.drop(columns=df[['salary', *pair]].corr()['salary'].idxmin())
    return df


def main():
    get_data()
    data_path = "../Data/nba2k-full.csv"
    df_clean = clean_data(data_path)
    df_feat = feature_data(df_clean)
    multicol_data(df_feat)


if __name__ == '__main__':
    main()
