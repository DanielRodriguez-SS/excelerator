from datetime import datetime
import streamlit as st
import pandas as pd
 
master_file = st.file_uploader("Upload the master file")

if master_file:
    df_master = pd.read_excel(master_file)

    st.dataframe(df_master)

    store_name_column = st.number_input("Enter the numner of the column where 'Store Name' is located:", min_value=0)
    store_name_row = st.number_input("Enter the numner of the row where 'Store Name' is located:", min_value=0)

    all_stores = df_master.iloc[store_name_row + 1:, store_name_column].to_list()
    store_label = df_master.iloc[store_name_row,store_name_column]

    if store_label == 'Store Name':
        st.write(f'Total Stores: {len(all_stores)}')
        all_codes = df_master.iloc[store_name_row, store_name_column + 1:].to_list()
        st.write(f'Total Codes: {len(all_codes)}')
        season_ranging_data = {}
        season_ranging_data['Store'] = []
        season_ranging_data['ITEMNUMBER'] = []
        season_ranging_data['PRODUCTNAME'] = []

        for index_code, code in enumerate(all_codes):
            for index_store ,store in enumerate(all_stores):
                if (df_master.iloc[index_store + (store_name_row+1), index_code + (store_name_column+1)] == 'R') or (df_master.iloc[index_store + (store_name_row+1), index_code + (store_name_column+1)] == 1):
                    season_ranging_data['Store'].append(store)
                    season_ranging_data['ITEMNUMBER'].append(code)
                    season_ranging_data['PRODUCTNAME'].append(df_master.iloc[store_name_row-2, index_code + store_name_column+1])
        df_new_season = pd.DataFrame(season_ranging_data)

        chunk_size = 5000

        chunks = [df_new_season.iloc[i:i + chunk_size] for i in range(0, len(df_new_season), chunk_size)]

        for idx, chunk in enumerate(chunks):
            st.dataframe(chunk, hide_index=True)

    else:
        st.warning('Stores not found, please verify the cell')
