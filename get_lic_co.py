# %%
import json

import pandas as pd
from requests_html import HTMLSession


def get_hk_mso():
    session = HTMLSession()
    
    url_auth = "https://eservices.customs.gov.hk/MSOS/wsrh/001s1w?searchBy=ALL"
    url = "https://eservices.customs.gov.hk/MSOS/wsrh/loadSearchLicenseGrid?searchBy=ALL&rowsPerPage=99999&currPage=1"

    r = session.get(url_auth) #sync the agreement in session
    r = session.get(url)

    mso = r.content

    df_mso = pd.DataFrame(json.loads(mso.decode('utf8'))['pubSrchList'])
    df_mso = df_mso.drop_duplicates(['coName', 'coNameChn'])
    df_mso = df_mso.rename(columns={'coName': 'mso_name', 'coNameChn': 'mso_name_cn'})
    df_mso['cntry_code'] = 'HK'
    df_mso = df_mso[['cntry_code', 'mso_name', 'mso_name_cn']]

    return df_mso


# %%
def get_sg_mso():

    session = HTMLSession()
    sg_mso_url = "https://eservices.mas.gov.sg/fid/custom/printpartial"
    r = session.get(sg_mso_url)

    df_mso = pd.read_html(r.text)[0]

    mso_cond = (df_mso['Licence Type/Status'].isin(['Money-changing Licensee']) |
                df_mso['Activity/Business Type'].isin(['Money-changing Service',
                                                       'Cross-border Money Transfer Service',
                                                       'Domestic Money Transfer Service',
                                                       'E-money Issuance Service', ])
                )
    df_mso = df_mso.drop_duplicates(['Organisation Name'])
    df_mso = df_mso[mso_cond].rename(columns={'Organisation Name': 'mso_name'})
    df_mso['cntry_code'] = 'SG'
    df_mso = df_mso[['cntry_code', 'mso_name']]

    return df_mso


# %%
df_hk_mso = get_hk_mso()
df_sg_mso = get_sg_mso()
df_mso = pd.concat([df_hk_mso, df_sg_mso])

# %%
