import sys
from data_proc import load_data, process_data, add_lr_features
from pandas import read_pickle, DataFrame
from constants import TARGET_COL

if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise ValueError('Input filename.csv is not given!')
    else:
        filename = sys.argv[1]
        features = load_data(filename)
        X = process_data(features)
    
        lgbm_main = read_pickle('models/lgbm_main.pkl.gz')
        lr_prod = read_pickle('models/lr_prod.pkl.gz')

        add_lr_features(X, lr_models=lr_prod)
        pred = DataFrame(lgbm_main.predict(X), columns=TARGET_COL[:3])
        pred[TARGET_COL[-1]] = pred.sum(axis=1)
        pred.to_csv(f'predicted_{filename}', index=False)
        print(f'Prediction saved to predicted_{filename}')
        