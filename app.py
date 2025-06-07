import streamlit as st
import pandas as pd

# Load the CSVs (no spaces in column names)
table1 = pd.read_csv("table1.csv")
table2 = pd.read_csv("table2.csv")

st.title("📄 Document Upload for Transactions")

# Select a transaction number from table1
transaction_ids = table1['TransactionNumber'].unique()
selected_transaction = st.selectbox("Select Transaction Number", transaction_ids)

# Get the selected transaction row
transaction_entry = table1[table1['TransactionNumber'] == selected_transaction].iloc[0]

st.write("Transaction Entry Keys:", transaction_entry.keys())

# Find matching rows in table2
matching_rows = table2[
    (table2['ProcessID'] == transaction_entry['ProcessID']) &
    (table2['SubProcessID'] == transaction_entry['SubProcessID']) &
    (table2['Region'] == transaction_entry['Region']) &
    (table2['IncoTerm'] == transaction_entry['IncoTerm']) &
    (table2['PaymentTerm'] == transaction_entry['PaymentTerm']) &
    (table2['Plant'] == transaction_entry['Plant'])
]

# Show matching document types and uploaders
st.subheader("Upload Documents for the Selected Transaction")

for idx, row in matching_rows.iterrows():
    doc_type = row['DocumentType']
    st.markdown(f"**Document Type:** {doc_type}")
    uploaded_file = st.file_uploader(f"Upload for: {doc_type}", key=f"{selected_transaction}_{idx}")
    if uploaded_file:
        st.success(f"Uploaded '{uploaded_file.name}' for {doc_type}")
