import streamlit as st
import pandas as pd

# Load your cleaned datasets
table1 = pd.read_csv("table1.csv")  # Transaction data
table2 = pd.read_csv("table2.csv")  # Metadata with responsibilities

st.title("📑 Transaction Document Tracker")

# Sidebar: Select a transaction
st.sidebar.header("Select a Transaction")
transaction_ids = table1['TransactionNumber'].unique()
selected_transaction = st.sidebar.selectbox("Transaction Number", transaction_ids)

# Filter selected transaction row
transaction_entry = table1[table1['TransactionNumber'] == selected_transaction].iloc[0]

st.write("Transaction entry keys:", transaction_entry.keys().tolist())

# Try to find the matching entry in table2
matched_entry = table2[
    (table2['ProcessID'] == transaction_entry['ProcessID']) &
    (table2['SubProcessID'] == transaction_entry['SubProcessID']) &
    (table2['Region'] == transaction_entry['Region']) &
    (table2['IncoTerm'] == transaction_entry['IncoTerm']) &
    (table2['PaymentTerm'] == transaction_entry['PaymentTerm']) &
    (table2['Plant'] == transaction_entry['Plant'])
]

# Show transaction metadata
st.subheader(f"Transaction Details: {selected_transaction}")
st.write("### From Table 1 (Transaction Data)")
st.write(transaction_entry)

# Show document and responsibility info from Table 2
if not matched_entry.empty:
    doc_type = matched_entry.iloc[0]['DocumentType']
    responsible = matched_entry.iloc[0]['ResponsiblePerson']
    verifier = matched_entry.iloc[0]['VerificationPerson']

    st.write("### Required Document & Responsible Parties")
    st.markdown(f"- **Document Type:** {doc_type}")
    st.markdown(f"- **Responsible Person:** {responsible}")
    st.markdown(f"- **Verification Person:** {verifier}")

    # Upload functionality
    st.write("### Upload Required Document")
    uploaded_file = st.file_uploader("Upload Document", type=["pdf", "docx", "xlsx"])
    if uploaded_file:
        st.success(f"✅ Document '{uploaded_file.name}' uploaded successfully!")
else:
    st.warning("⚠️ No matching process details found in Table 2.")
