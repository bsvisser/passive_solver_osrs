# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 17:09:09 2022

@author: Brent Visser
"""
from io import StringIO 
import streamlit as st
import pandas as pd
import csv
import pandas as pd 
import itertools
import numpy as np
 
reload_data = True
if reload_data:
    passives = {}
    df = pd.read_csv("passives.csv") 
    
allrelics = df.values[1:].ravel()
allrelics = sorted(list(set(allrelics.tolist()))[1:])
b_allrelics = allrelics

def valid(testlist, combinedlists, reqnumrelics): # (testlist, combinedlists?, reqnumrelics)
    overlapsuperlist = []
    for reliclist in combinedlists:
        overlapsuperlist.append([value for value in testlist if value in reliclist])
    
    length_overlaplists = []
    for overlaplist in overlapsuperlist: 
        length_overlaplists.append(len(overlaplist))
        
    if min(length_overlaplists-reqnumrelics) >= 0:
        return True
    else:
        return False
  
    
with st.expander("Kies relics die je hebt, sla ze op of importeer ze", expanded=False):
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
         # Can be used wherever a "file-like" object is accepted:
         stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
         string_data = stringio.read()
         saved_relics = string_data.split(',')
         #saved_relics = [reli.replace('"', '') for reli in saved_relics]
         allrelics = [value for value in allrelics if value in saved_relics]

    if st.checkbox("Update mijn lijst (upload eerst je file en klik dan hier)"):          
          minlist = list(set(b_allrelics) - set(allrelics)) + list(set(b_allrelics) - set(allrelics))
          n_opt = st.multiselect("Voeg de relics die je nieuw hebt toe:", minlist)
          allrelics += n_opt
          csvlist = ",".join(allrelics)
          st.download_button('Download je relics', str(csvlist), "relics.txt", mime='text/csv')
          
    options = st.multiselect("Of selecteer relics die je hebt/voeg toe aan wat je net hebt geupload:", allrelics)
    if len(options)>1:
          allrelics = [value for value in allrelics if value in options]
          csvlist = ",".join(allrelics)
          st.download_button('Download je relics', str(csvlist), "relics.txt", mime='text/csv')
    
st.title("Passive Solver")

results = []

st.sidebar.table(allrelics)

targetpassives = st.multiselect("Welke passives wil je?", df.columns)


numrelics = st.slider("Hoeveel relic slots heb je?", min_value=1, max_value=7, value=5, step=1)

reqnumrelics = []
for i in targetpassives:
    reqnumrelics.append(int(df[i][0]))
    

masterlist = []

for tp in targetpassives:
    masterlist.append(list(set(df[tp].values[1:]))[1:])

reqfrags = False

if st.checkbox("Verplichte relics?"):   #multiselect
    flat_list =[item for sublist in masterlist for item in sublist]
    
    reqfrags = st.multiselect("Welke frag moet erin zitten?", flat_list) #flatlist
    
    
    if numrelics < max(reqnumrelics): #len
            st.error("Een set effect kan niet geactiveerd worden, te weinig relics")
        
if st.button("Run"):
    st.sidebar.table(allrelics)

    comblist = [value for value in allrelics if value in masterlist]
    st.write(comblist)
    combinations = itertools.combinations(comblist, numrelics)
    
    for possibility in combinations:
        st.spinner(text="In progress...")
        if len(set(possibility)) < len(possibility) or np.nan in possibility:
            pass
        else:
            if valid(possibility, masterlist, reqnumrelics):
                #print(reqfrags)
                if reqfrags != False and not (set(reqfrags).issubset(set(possibility))):
                    pass
                else:
                    results.append(list(set(possibility)))

    st.table(set(map(tuple, results)))

                        
    
