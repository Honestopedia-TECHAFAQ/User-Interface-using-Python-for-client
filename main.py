import streamlit as st
import pandas as pd
import os

def load_datasets():
    alternative_parts_dataset = pd.DataFrame()
    stock_information_dataset = pd.DataFrame()
    return alternative_parts_dataset, stock_information_dataset
def generate_master_part_number(dataset):
    counter = len(dataset) + 8000000
    return f'SPL{counter}'
def main():
    st.title('Alternative Parts Search, Stock Information, and UI Demonstration')
    st.sidebar.header('Upload Alternative Parts Dataset (CSV)')
    alternative_parts_file = st.sidebar.file_uploader('Choose a file', type='csv')
    st.sidebar.header('Upload Stock Information Dataset (XLS)')
    stock_information_file = st.sidebar.file_uploader('Choose a file', type='xls')
    alternative_parts_dataset, stock_information_dataset = load_datasets()

    if alternative_parts_file is not None:
        alternative_parts_dataset = pd.read_csv(alternative_parts_file)

    if stock_information_file is not None:
        stock_information_dataset = pd.read_excel(stock_information_file)
    st.sidebar.header('Search')
    search_term = st.sidebar.text_input('Enter search term:')
    search_button = st.sidebar.button('Search')
    if search_button:
        results_alternative_parts = alternative_parts_dataset[
            (alternative_parts_dataset['Material number'] == search_term) |
            (alternative_parts_dataset['Part number'] == search_term) |
            (alternative_parts_dataset['Substitute material'] == search_term) |
            (alternative_parts_dataset['Alternative part'] == search_term) |
            (alternative_parts_dataset['Main alternative part'] == search_term)
        ]
        master_part_number = generate_master_part_number(alternative_parts_dataset)
        alternative_parts_dataset.loc[results_alternative_parts.index, 'Master part number'] = master_part_number
        alternative_parts_dataset.to_csv('alternative_parts_data.csv', index=False)
        st.subheader('Alternative Parts Search Results:')
        st.write(results_alternative_parts)
        st.subheader('Master Part Number:')
        st.write(master_part_number)
        results_stock_information = stock_information_dataset[stock_information_dataset['Item code'] == search_term]
        st.subheader('Stock Information:')
        st.write(results_stock_information[['Item code', 'SPL Master', 'Item description', 'Stock on hand', 'Location']])
    st.header('UI Demonstration')

    st.markdown("### Linked Items Lookup")
    linked_item_code = st.text_input('Enter Linked Item Code:')
    lookup_button = st.button('Lookup Linked Item')
    if lookup_button:
        linked_item_result = alternative_parts_dataset[alternative_parts_dataset['Part number'] == linked_item_code]

        if not linked_item_result.empty:
            st.subheader('Linked Item Information:')
            st.write(linked_item_result[['Material number', 'Part number', 'Substitute material', 'Alternative part', 'Main alternative part']])
        else:
            st.warning(f'Linked Item with code {linked_item_code} not found.')

if __name__ == '__main__':
    main()
