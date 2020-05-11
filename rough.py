import pandas as pd

nsdq = pd.read_csv('NASDAQcompanylist.csv')
#nsdq.set_index('Symbol', inplace=True)

print(nsdq.head())
print(nsdq.shape)


options = [{'label':sector,'value':sector} for sector in nsdq.Sector.unique()]


print(nsdq.Symbol.unique())
