import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.cluster import KMeans


if __name__ == '__main__':
    X = pd.read_csv('olx.csv')
    X.drop('title', axis=1, inplace=True)
    X.drop('link', axis=1, inplace=True)
    X['price'] = X['price'].replace('[^\d]', '', regex=True).astype(int)
    X['area'] = X['area'].replace('[^\d]', '', regex=True).astype(int)
    X['price_for_meter'] = X['price_for_meter'].replace('[^\d, ^.]', '', regex=True).astype(float)

    X['negotiations'] = X['negotiations'].fillna('Brak')
    ohe_encoder = OneHotEncoder()
    ordinal_encoder = OrdinalEncoder()
    cols_ohe = ['negotiations']
    cols_ordinal = ['city']

    preprocessor = ColumnTransformer(
        transformers=[
            ('ohe_encoder', ohe_encoder, cols_ohe),
            ('ordinal_encoder', ordinal_encoder, cols_ordinal),
        ]
    )

    my_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('clustering', KMeans(n_clusters=3, random_state=42))
    ])

    my_pipeline.fit(X)
    labels = my_pipeline.predict(X)
    X['cluster_label'] = labels

    print(X.head(10))
