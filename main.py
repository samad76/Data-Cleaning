import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="📒 File Converter and Cleaner",
    page_icon="🧹",
    layout="wide",
)
st.title("📒 File Converter and Cleaner")
st.write(
    "This tool allows you to convert and clean CSV files. You can upload a CSV file, and it will be converted to a different format (e.g., JSON, Excel) and cleaned by removing empty rows and columns."
)

files = st.file_uploader(
    "Upload a CSV file or excel file",
    type=["csv", "xlsx"],
    accept_multiple_files=True,
    label_visibility="collapsed",
    help="Upload a CSV file to convert and clean.",
)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        if ext not in ["csv", "xlsx"]:
            st.error(f"Unsupported file format: {ext}. Please upload a CSV or Excel file.")
            continue
        # Read the uploaded file into a DataFrame
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
        # Display the file name
        st.subheader(f"File: {file.name}")
        # Display the file size
        st.write(f"File size: {file.size / 1024:.2f} KB")
        # Display the file type
        st.write(f"File type: {ext.upper()}")
        # Display the number of rows and columns
        st.write(f"Number of rows: {df.shape[0]}")
        st.write(f"Number of columns: {df.shape[1]}")
             
               
        if st.checkbox(f"Fill missing values - {file.name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("Missing values filled with column means.")
            st.dataframe(df.head())
            
    selected_columns = st.multiselect(
        f"Select columns {file.name}",
        options=df.columns,
        default=df.columns,
        label_visibility="collapsed",
        help="Select columns to keep in the cleaned file.",
     )
    df = df[selected_columns]
    st.dataframe(df.head())
    if st.checkbox(f" Show Chart - {file.name}") and not df.select_dtypes(include=["number"]).empty:
        st.subheader("Chart")
        st.bar_chart(df.select_dtypes(include=["number"]).iloc[:,:2])
    # Remove empty rows and columns
    df.dropna(how="all", inplace=True)
    df.dropna(axis=1, how="all", inplace=True)
    st.success("Empty rows and columns removed.")
    # Display the cleaned DataFrame 
    st.subheader("Cleaned DataFrame")
    st.dataframe(df)
    # Convert the cleaned DataFrame to different formats
    json_data = df.to_json(orient="records", lines=True)
    excel_data = BytesIO()
    df.to_excel(excel_data, index=False)
    excel_data.seek(0)
    # Download buttons for different formats
    formate_choice = st.radio(
        "Select the format to download",
        ("JSON", "Excel", "CSV"),
        label_visibility="collapsed",
        help="Select the format to download the cleaned file.",
        key=file.name,
    )
    if formate_choice == "JSON":
        st.download_button(
            label="Download as JSON",
            data=json_data,
            file_name=f"{file.name.split('.')[0]}.json",
            mime="application/json",
        )
    elif formate_choice == "Excel":
        st.download_button(
            label="Download as Excel",
            data=excel_data,
            file_name=f"{file.name.split('.')[0]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    elif formate_choice == "CSV":
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv_data,
            file_name=f"{file.name.split('.')[0]}.csv",
            mime="text/csv",
        )
    else:
        st.error("Please select a format to download.")
        st.stop()
        st.success("File downloaded successfully.")
            