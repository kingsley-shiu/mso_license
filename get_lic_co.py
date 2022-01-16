# %%
import json

import pandas as pd
import requests

#%%
def get_hk_mso():
    url = "https://eservices.customs.gov.hk/MSOS/wsrh/loadSearchLicenseGrid?searchBy=ALL&rowsPerPage=99999&currPage=1"

    r = requests.get(url)

    mso = r.content

    df_mso = pd.DataFrame(json.loads(mso.decode('utf8'))['pubSrchList'])
    df_mso = df_mso[['coName', 'coNameChn', 'licExprDt', 'licNum']].drop_duplicates()

    return df_mso


get_hk_mso()
#%%
sg_mso_url = "https://eservices.mas.gov.sg/fid/institution/print"
