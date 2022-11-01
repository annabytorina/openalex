from tkinter import E
import requests
import pandas as pd
df=pd.DataFrame(columns=['Автор','ORCID','Публ.','doi','Цит.','публ. за 2022','публ. за 2021','публ. РОСТ','цит. за 2022','цит. за 2021','цит. РОСТ','h-index 2022','h-index 2021','h-index РОСТ']) #создаем таблицу для результатов
url='https://api.openalex.org/authors?filter=last_known_institution.ror:https://ror.org/040a2r459&page=1&per-page=200'
r = requests.get(url)
rj = r.json() 
for index, item in enumerate(rj['results']): #перебираем результаты и берем нужные поля
        count_works_22=count_works_21=count_cited_22=count_cited_21=min_h22=min_h21 = 0
        df.at[index,'Автор']=item['display_name']
        df.at[index,'ORCID']=item['orcid']
       # if item['orcid'] is None:
       #         df.at[index,'ORCID']='нет регистрации'
       # else:
       #         df.at[index,'ORCID']=item['orcid']
        df.at[index,'Публ.']=item['works_count']
        df.at[index,'doi']= item['works_api_url']
        df.at[index,'Цит.']=item['cited_by_count']
        if item['counts_by_year']:       
            if item['counts_by_year'][0]['year'] == 2022:    
                count_works_22 = item['counts_by_year'][0]['works_count']   
                df.at[index,'публ. за 2022'] = count_works_22
                count_cited_22 = item['counts_by_year'][0]['cited_by_count']
                df.at[index,'цит. за 2022'] = count_cited_22
                if item['counts_by_year'][1]['year'] == 2021:
                    count_works_21 = item['counts_by_year'][1]['works_count']
                    df.at[index,'публ. за 2021'] = count_works_21 
                    count_cited_21 = item['counts_by_year'][1]['cited_by_count']
                    df.at[index,'цит. за 2021'] = count_cited_21
                else:
                    count_works_21 = 0
                    df.at[index,'публ. за 2021'] = count_works_21    
            else:
                count_works_22 = 0
                df.at[index,'публ. за 2022']=0
        else:
            count_works_22=count_works_21=count_cited_22=count_cited_21=min_h22=min_h21 = 0
        #df.at[index,'публ. за 2021']=item['counts_by_year'][1]['works_count']
        if count_works_22 - count_works_21 > 0 :
                df.at[index,'публ. РОСТ'] = count_works_22 - count_works_21
        else:
            df.at[index,'публ. РОСТ'] = 0;    
        #df.at[index,'цит. за 2022']=item['counts_by_year'][0]['cited_by_count']
        #df.at[index,'цит. за 2021']=item['counts_by_year'][1]['cited_by_count']
        if count_cited_22 - count_cited_21 > 0 :
                df.at[index,'цит. РОСТ'] = count_cited_22 - count_cited_21
        else:
            df.at[index,'цит. РОСТ'] = 0;
        min_h22 = min(count_works_22,count_cited_22)
        min_h21=min(count_works_21,count_cited_21)
        df.at[index,'h-index 2022']=min_h22
        df.at[index,'h-index 2021']=min_h21
        if min_h22 - min_h21 > 0:
             df.at[index,'h-index РОСТ'] = min_h22 - min_h21
        else:
            df.at[index,'h-index РОСТ'] = 0;
print (df.head())
df.to_excel(r'd:\output2.xlsx')