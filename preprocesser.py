import pandas as pd


def preprocess(df, region_df):
    #Filtering the summer season
    df=df[df['Season']=='Summer']

    #merge the df with regin_df
    df=df.merge(region_df, on='NOC', how='left')

    #Droping Duplicates
    df.drop_duplicates(inplace=True)

    #one Hot Encoding
    df=pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df