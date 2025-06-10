import numpy as np
import pandas as pd
from CBFV.composition import generate_features

file_name =  'Numericalized_DS.xlsx'


df = pd.read_excel(file_name)
print(df['formula'])
df2= df['formula'].to_frame()
df2['target']=df['target']
print(df2)

unique_formulae = df['formula'].unique()
print(f'{len(unique_formulae)} unique compositions')

X_unscaled, y, formulae_train, skipped_train = generate_features(df2, elem_prop='jarvis', drop_duplicates=False, extend_features=True, sum_feat=True)

features = ['avg_AtomicWeight', 'mode_NdValence','avg_CovalentRadius', 'dev_CovalentRadius',
       'range_NsValence', 'range_NValence', 'mode_NValence',
       'avg_NdValence', 'avg_NpValence', 'sum_NdValence', 'max_NValence',
       'min_Electronegativity','range_NdValence', 'max_AtomicWeight', 'dev_Electronegativity',
       'range_Electronegativity','mode_CovalentRadius', 'min_NdValence',
       'range_CovalentRadius','range_NpValence', 'avg_Electronegativity', 'dev_NfValence', 'sum_NValence',
       'range_NfValence', 'min_CovalentRadius','range_AtomicWeight', 'avg_NValence',
       'dev_NValence','sum_NpValence', 'max_CovalentRadius','min_NValence']

X_unscaled = X_unscaled[features]
X_unscaled['formula'] = df2['formula']
X_unscaled.to_excel('FinalDS_TransformJarvis.xlsx',index=False)

df3 = X_unscaled.copy()
print(df3)

