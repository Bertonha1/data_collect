# %%
import requests

from tqdm import tqdm

from bs4 import BeautifulSoup

import pandas as pd


headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # 'cookie': '_gid=GA1.2.1813957869.1729109294; _ga=GA1.2.1896330004.1729109294; __gads=ID=7a4c97aa23c39666:T=1729109293:RT=1729112487:S=ALNI_MahB6hE_WEXCPfjPT9IDzZ4fjEnYQ; __gpi=UID=00000a5d9da61cda:T=1729109293:RT=1729112487:S=ALNI_MbnLGlUmcO6-mZhx4QTcGpo3oP6sA; __eoi=ID=2f5990ac03aecd63:T=1729109293:RT=1729112487:S=AA-Afjbogod66NcfmROIfQElsfJl; FCNEC=%5B%5B%22AKsRol8-AC6xnr5oAmIgtx-1ZWJHpMFbY0zS0lSZe58e_bHB6_hbYzwTq65C27lmMYZzDWs-l0c1uylKizx22LrhB_l6eGf2f4-9UJ8am3CfOLfeLsciT94-IvAExVnnmOV39HHJ7bx4u4LNGVX5dV131ml0l6yFYQ%3D%3D%22%5D%5D; _ga_DJLCSW50SC=GS1.1.1729112486.2.1.1729112489.57.0.0; _ga_D6NF5QC4QT=GS1.1.1729112486.2.1.1729112489.57.0.0',
        'priority': 'u=0, i',
        'referer': 'https://www.residentevildatabase.com/personagens/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Opera GX";v="113", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0',
    }

def get_content(url):   
    response = requests.get(url, headers=headers)
    return response


def get_basic_infos(soup):
    div = soup.find("div", class_="td-page-content")
    paragrafo = div.find_all("p")[1]
    ems = paragrafo.find_all("em")
    data = {}
    for i in ems:
        chave,valor, *_ = i.text.split(':')
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")
        
    return data

def get_aparicoes(soup):
    lis = (soup.find("div", class_="td-page-content")
                    .find("h4")
                    .find_next()
                    .find_all("li"))
    
    aparicoes = [i.text for i in lis]
    return aparicoes

def get_personagens_infos(url):
    resp = get_content(url)

    if resp.status_code != 200:
        print("Não foi possível obter os dados ")
        return {}
    else:     
        soup = BeautifulSoup(resp.text)
        data = get_basic_infos(soup)
        data['Aparicoes'] = get_aparicoes(soup)
        return data
    
def get_links():
    url = "https://www.residentevildatabase.com/personagens/"

    resp = requests.get(url, headers=headers)
    soup_personagens = BeautifulSoup(resp.text)
    ancoras = (soup_personagens.find("div", class_="td-page-content")
    .find_all("a"))

    links = [i['href'] for i in ancoras]
    return links


# %%

# %%

links = get_links()
data = []
for i in tqdm(links):
    d = get_personagens_infos(i)
    d["link"] = i
    nome = i.split("/")[-1].replace("-"," ").title()
    d["Nome"] = nome
    data.append(d)


# %%
df = pd.DataFrame(data)

df
# %%
df.to_csv("dados_re.csv",index=False, sep=";")

#%%
df.to_parquet("dados_re.parquet",index=False)

# %%
df_new = pd.read_parquet("dados_re.parquet")
df_new

#%%
df.to_pickle("dados_re.pkl")