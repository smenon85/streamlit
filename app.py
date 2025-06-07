import streamlit as st
import pandas as pd

# --- Load Data ---
# Replace these with your actual data sources
table1 = pd.read_csv("table1.csv")
table2 = pd.read_csv("table2.csv")
table2.columns = table2.columns.str.strip()  # Remove leading/trailing spaces

st.title("📑 Transaction Document Tracker")

# --- Select Transaction ---
st.sidebar.header("Select a Transaction")
transaction_ids = table2['TransactionNumber'].unique()
selected_transaction = st.sidebar.selectbox("TransactionNumber", transaction_ids)

# --- Filter selected entry from Table 2 ---
transaction_entry = table2[table2['TransactionNumber'] == selected_transaction].iloc[0]

# --- Match entry in Table 1 ---
matched_entry = table1[
    (table1['ProcessID'] == transaction_entry['Process ID']) &
    (table1['SubProcessID'] == transaction_entry['Sub Process ID']) &
    (table1['Region'] == transaction_entry['Region']) &
    (table1['IncoTerm'] == transaction_entry['Inco Term']) &
    (table1['PaymentTerm'] == transaction_entry['Payment Term']) &
    (table1['Plant'] == transaction_entry['Plant'])
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
