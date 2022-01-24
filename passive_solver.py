# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 17:09:09 2022

@author: Brent Visser
"""

import streamlit as st
import pandas as pd
import csv
import pandas as pd 
import itertools
import numpy as np
    
def valid(testlist, list1, list2, reqrelics):
    overlap_list1 = [value for value in testlist if value in list1]
    overlap_list2 = [value for value in testlist if value in list2]
    
    
    if len(overlap_list1) >= reqrelics[0] and len(overlap_list2) >= reqrelics[1]:
        return True
    else:
        return False
    
reload_data = True
#passive dicts: 1e entry passive numbers, tweede entry fragments
if reload_data:
    passives = {}
    df = pd.read_csv("passives.csv") 
    
allrelics = df.values[1:].ravel()
allrelics = list(set(allrelics.tolist()))[1:]
    
with st.expander("Kies relics die je hebt, sla ze op of importeer ze", expanded=False):
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
         # Can be used wherever a "file-like" object is accepted:
         dataframe = pd.read_csv(uploaded_file)
         st.write(dataframe)
            
            
    options = st.multiselect(allrelics)
    st.download_button('Download je relics', options, "relics.txt")
    
st.title("Passive Solver")

results = []


targetpassive = st.selectbox('Welke passive (1) wil je?',
     df.columns)

targetpassive2 = st.selectbox(
    'Welke passive (2) wil je?',
     df.columns)

if targetpassive == targetpassive2:
    st.error("Kan niet hetzelfde zijn")

numrelics= st.slider("Hoeveel relic slots heb je?", min_value=1, max_value=7, value=5, step=1)
reqrelics = [int(df[targetpassive][0]), int(df[targetpassive2][0])]


reqfrags = False
if st.checkbox("Verplichte relic?"):
    l1 = list(set(df[targetpassive].values[1:]))[1:]
    l2 = list(set(df[targetpassive2].values[1:]))[1:]
    reqfrags = st.selectbox("Welke frag moet erin zitten?", l1+l2)

if numrelics < reqrelics[0] or numrelics < reqrelics[1]:
        st.error("Kan niet geactiveerd worden, te weinig relics")
        
if st.button("Run"):
    my_bar = st.progress(0)
    list1 = list(df[targetpassive][1:])
    list2 = list(df[targetpassive2][1:])
    
    comblist = list1+list2
    
    combinations = itertools.combinations(comblist, numrelics)
    
    for possibility in combinations:
        st.spinner(text="In progress...")
        if len(set(possibility)) < len(possibility) or np.nan in possibility:
            pass
        else:
            if valid(possibility, list1, list2, reqrelics):
                print(reqfrags)
                if reqfrags != False and reqfrags not in possibility:
                    pass
                else:
                    results.append(possibility)

    st.table(results)
                        
    
