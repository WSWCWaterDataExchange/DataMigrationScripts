#!/usr/bin/env python
import pandas as pd
import numpy as np
from sodapy import Socrata
import os

workingDir="C:/Tseganeh/0WaDE/Data/TestOutputs"
os.chdir(workingDir)

fileInput="DWR_Water_Right_-_Net_Amounts.csv"
allocCSV="waterallocations.csv"
siteCSV="sites.csv"
WSdimCSV="watersources.csv"
MethodsCSV="methods.csv"
varCSV="variables.csv"

##from https://dev.socrata.com/foundry/data.colorado.gov/a8zw-bjth
# client = Socrata("data.colorado.gov", None)
## authenticated client (needed for non-public datasets):
# client = Socrata(data.colorado.gov,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")
# top100 = client.get("a8zw-bjth", limit=100)
## Convert to pandas DataFrame
# df = pd.DataFrame.from_records(top100)

##OR read csv
df = pd.read_csv(fileInput)
df100 = df.head(100)

columns=['WaterSourceUUID', 'WaterSourceNativeID',	'WaterSourceName', 'WaterSourceTypeCV',
         'WaterQualityIndicatorCV',	'GNISFeatureNameCV', 'Geometry']

dtypesx = ['BigInt	NVarChar(250)	NVarChar(250)	NVarChar(250)	NVarChar(100)	NVarChar(100)',
           'NVarChar(250)	Geometry']

#assumes dtypes inferred from CO file
outdf100=pd.DataFrame(columns=columns)
#
#existing corresponding fields
destCols=['WaterSourceNativeID', 'WaterSourceName']
sourCols=['WDID', 'Water Source']
outdf100[destCols] = df100[sourCols]
"""
outdf100.WaterSourceNativeID = df100.WDID   #TODO check this
outdf100.WaterSourceName = df100['Water Source']
"""
#filter the whole table based on a unique combination of site ID, SiteName
outdf100 = outdf100.drop_duplicates(subset=['WaterSourceNativeID', 'WaterSourceName'])   #
outdf100 = outdf100.reset_index(drop=True)
#hardcode
outdf100.WaterSourceTypeCV = 'Unknown'
outdf100.WaterQualityIndicatorCV = 'Unknown'
#outdf100.GNISFeatureNameCV
#outdf100.Geometry

#9.10.19 add UUID for dim tables
# no-loop approach?
#native source identifer and the organization univeral id
for ix in range(len(outdf100.index)):
    outdf100.loc[ix, 'WaterSourceUUID'] = "_".join(["CODWR",str(outdf100.loc[ix, 'WaterSourceNativeID'])])

#9.9.19: Adel: check all 'required' (not NA) columns have value (not empty)
#'WaterSourceNativeID',
requiredCols=['WaterSourceUUID', 'WaterSourceTypeCV', 'WaterQualityIndicatorCV']
#replace blank strings by NaN, if there are any
outdf100 = outdf100.replace('', np.nan)
#outdf100_nullMand = outdf100.loc[outdf100.isnull().any(axis=1)] --for all cols#any cell of these columns is null
#(outdf100["WaterSourceNativeID"].isnull()) |
outdf100_nullMand = outdf100.loc[(outdf100["WaterSourceUUID"].isnull()) | (outdf100["WaterSourceTypeCV"].isnull()) |
                                (outdf100["WaterQualityIndicatorCV"].isnull())]
#outdf100_nullMand = outdf100.loc[[False | (outdf100[varName].isnull()) for varName in requiredCols]]
if(len(outdf100_nullMand.index) > 0):
    outdf100_nullMand.to_csv('watersources_mandatoryFieldMissing.csv')  # index=False,
#ToDO: purge these cells if there is any missing? #For now left to be inspected

#write out
outdf100.to_csv(WSdimCSV, index=False)

print("Done watersources")