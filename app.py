import streamlit as st
import pandas as pd

# --- Load Data ---
# Replace these with your actual data sources
table1 = pd.read_csv("table1.csv")
table2 = pd.read_csv("table2.csv")
table1.columns = table1.columns.str.strip()  # Remove leading/trailing spaces
table2.columns = table2.columns.str.strip()  # Remove leading/trailing spaces

st.title("📑 Transaction Document Tracker")

# --- Select Transaction ---
st.write("Table 1 loaded:", table1.shape)
st.write("Table 2 loaded:", table2.shape)
st.sidebar.header("Select a Transaction")
transaction_ids = table1['TransactionNumber'].unique()
selected_transaction = st.sidebar.selectbox("TransactionNumber", transaction_ids)

# --- Filter selected entry from Table 2 ---
transaction_entry = table1[table1['TransactionNumber'] == selected_transaction].iloc[0]

# --- Match entry in Table 2 ---
matched_entry = table2[
    (table2['ProcessID'] == transaction_entry['ProcessID']) &
    (table2['SubProcessID'] == transaction_entry['SubProcessID']) &
    (table2['Region'] == transaction_entry['Region']) &
    (table2['IncoTerm'] == transaction_entry['IncoTerm']) &
    (table2['PaymentTerm'] == transaction_entry['PaymentTerm']) &
    (table2['Plant'] == transaction_entry['Plant'])
]

st.subheader(f"Transaction Details: {selected_transaction}")
st.write("### Metadata")
st.write(transaction_entry)

if not matched_entry.empty:
    responsible = matched_entry.iloc[0]['Responsible Person']
    verifier = matched_entry.iloc[0]['Verification Person']
    doc_type = matched_entry.iloc[0]['Document type']

    st.write("### Required Document Type")
    st.markdown(f"- **Document Type:** {doc_type}")
    st.markdown(f"- **Responsible Person:** {responsible}")
    st.markdown(f"- **Verification Person:** {verifier}")

    # Optionally: add file upload interface
    st.write("### Upload Required Document")
    uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx", "xlsx"])
    if uploaded_file:
        st.success(f"Document '{uploaded_file.name}' uploaded successfully!")
else:
    st.warning("No matching process metadata found in Table 1.")
