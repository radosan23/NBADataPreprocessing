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


def main():
    get_data()
    data_path = "../Data/nba2k-full.csv"
    clean_data(data_path)


if __name__ == '__main__':
    main()
