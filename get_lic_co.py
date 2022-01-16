# %%
import json

import pandas as pd
from requests_html import HTMLSession

#%%
def get_hk_mso():
    session = HTMLSession()
    url_auth = "https://eservices.customs.gov.hk/MSOS/wsrh/001s1w?searchBy=ALL"
    
    url = "https://eservices.customs.gov.hk/MSOS/wsrh/loadSearchLicenseGrid?searchBy=ALL&rowsPerPage=99999&currPage=1"

    r = session.get(url_auth)
    r = session.get(url)

    mso = r.content

    df_mso = pd.DataFrame(json.loads(mso.decode('utf8'))['pubSrchList'])
    df_mso = df_mso[['coName', 'coNameChn', 'licExprDt', 'licNum']].drop_duplicates()

    return df_mso


get_hk_mso()
#%%

sg_mso_url = "https://eservices.mas.gov.sg/fid/institution/print"

