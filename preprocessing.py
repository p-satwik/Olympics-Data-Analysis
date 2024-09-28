import pandas as pd

def doprocess(df,region_df):

    df = df[df['Season']=='Summer']

    df = df.merge(region_df, on='NOC', how='left')

    df.drop_duplicates(inplace=True)

    df = pd.concat([df,pd.get_dummies(df['Medal'],dtype=int)],axis=1)
    return df
