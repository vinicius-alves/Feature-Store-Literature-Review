
from scholarly import scholarly
import time
import pandas as pd
from tqdm.notebook import tqdm

#keywords
strings_to_search = ['''"feature store" meachine learning''']

results = []
pbar = tqdm(total = 0)
for string_to_search in strings_to_search:
    search_query = scholarly.search_pubs(string_to_search, year_low = 2017)
    pbar.total += search_query.total_results
    has_results = True
    while has_results:
        try:
            next_result = next(search_query)
            results.append(next_result)
        except StopIteration: 
            has_results = False
        pbar.update(1)
        time.sleep(0.5)
        
        

df_results = pd.DataFrame(results)
df_results_bib = pd.DataFrame(df_results['bib'].tolist()).add_prefix('bib_')

#remove duplicates
df_results = df_results[~df_results['pub_url'].duplicated(keep ='first')]
df_results= pd.concat([df_results, df_results_bib], axis = 1).drop(columns = ['bib'])

df_results['text_to_search'] = df_results['bib_abstract'].str.lower() +' ' + df_results['bib_title'].str.lower()

#remove publication without 'feature store' in abstract and title
idx = None
for string_to_search in ['feature store']:
    string_to_search = string_to_search.replace("\"",'')
    idy = df_results['text_to_search'].str.contains(string_to_search)
    if idx is None:
        idx = idy
    else:
        idx = (idx) & (idy)

df_results = df_results[idx].drop(columns = ['text_to_search'])

df_results.to_excel('Publicacoes_Google_Scholar.xlsx')
