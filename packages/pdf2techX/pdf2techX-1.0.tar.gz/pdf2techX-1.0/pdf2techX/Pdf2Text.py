from langchain.text_splitter import RecursiveCharacterTextSplitter
from urllib.parse import urlparse
import os
# import nltk
# nltk.download('punkt')
from urllib.request import urlopen, Request
import PyPDF2
from PyPDF2 import PdfWriter, PdfReader
import io
import requests
import fitz
from .text_clean import replace_w,_clean_missing_1,fix_unknown_char,Initialize_var
from .text_clean import *
from PyPDF2.errors import PdfReadError
import warnings
import pandas as pd


def extract_text(url_link):
    response = requests.get(url=url_link, timeout=120, verify=False)
    pdf_io_bytes = io.BytesIO(response.content)
    pdf = PdfReader(pdf_io_bytes)
    text = " ".join(page.extract_text() for page in pdf.pages)

    # Initialize the text splitter with custom parameters
    custom_text_splitter = RecursiveCharacterTextSplitter(
        # Set custom chunk size
        chunk_size = 300,
        chunk_overlap  = 30,
        # Use length of the text as the size measure
        length_function = len,
        # Use only "\n\n" as the separator
        separators = ['\n']
    )

    custom_texts = custom_text_splitter.create_documents([text])

    pypdf_list = []
    for i in range(len(custom_texts)):
        custom_text_all = custom_texts[i].page_content
        pypdf_list.append(custom_text_all)
    return pypdf_list

# ------------------------------------------------------------------------------------------
# extract text from actual path
def extract_text_from_path(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        text = " ".join(page.extract_text() for page in pdf_reader.pages)
    custom_text_splitter = RecursiveCharacterTextSplitter(
            # Set custom chunk size
            chunk_size = 300,
            chunk_overlap  = 30,
            # Use length of the text as the size measure
            length_function = len,
            # Use only "\n\n" as the separator
            separators = ['\n']
        )

    custom_texts = custom_text_splitter.create_documents([text])

    pypdf_list = []
    for i in range(len(custom_texts)):
        custom_text_all = custom_texts[i].page_content
        pypdf_list.append(custom_text_all)
    return pypdf_list

# ------------------------------------------------------------------------------------------
# extract text from actual path without textsplitter

def extract_text_from_path_no_chunk(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        text = " ".join(page.extract_text() for page in pdf_reader.pages)
    
    return text

# ------------------------------------------------------------------------------------------
# preprocessing text from pdf by P'Kaew's function
def clean_txt(text_list):
    list_clean = []

    # clean data in pypdf_list
    for i in range(len(text_list)):
        list_clean.append(_clean_missing_1(text_list[i]))

    df_clean = pd.DataFrame({"text": list_clean})
    return df_clean

# ------------------------------------------------------------------------------------------
# collect data
def create_table(url_linkk, num_id):
    ct_texts = extract_text_from_path(url_linkk)
    # ct_text_list = extract_text_2(url_linkk)
    df_clean = clean_txt(ct_texts)
    db_name_lst = []
    table_name_lst = []
    issue_date_lst = []
    expiration_date_lst = []
    file_name_lst = []
    document_id_lst = []
    url_lst = []
    domain_lst = []
    source_type_lst = []
    lang_lst = []
    category_1_lst = []
    category_2_lst = []
    title_lst = []
    description_lst = []
    section_lst = []
    par_lst = []
    updated_date_lst = []

    for i in range(len(df_clean)):
        db_name_lst.append('llm_ivx')
        table_name_lst.append('llm_ivx_pdf')
        issue_date_lst.append('null')
        expiration_date_lst.append('null')
        
        url_lst.append(url_linkk) # this

        a = urlparse(url_lst[0])
        file_name_lst.append(os.path.basename(a.path))

        # domain_lst.append('null')
        source_type_lst.append('pdf')
        lang_lst.append('th')
        category_1_lst.append('null')
        category_2_lst.append('null')
        title_lst.append('null')
        description_lst.append('null')
        section_lst.append('null')
        updated_date_lst.append('null')

    df_clean['db_name'] = db_name_lst
    df_clean['table_name'] = table_name_lst
    df_clean['issue_date'] = issue_date_lst
    df_clean['expiration_date'] = expiration_date_lst
    df_clean['file_name'] = file_name_lst
    df_clean['url'] = url_lst
    df_clean['source_type'] = source_type_lst
    df_clean['lang'] = lang_lst
    df_clean['category_1'] = category_1_lst
    df_clean['category_2'] = category_2_lst
    df_clean['title'] = title_lst
    df_clean['description'] = description_lst
    df_clean['section'] = section_lst
    df_clean['updated_date'] = updated_date_lst

    for k in range(len(df_clean)):
        document_id_lst.append(file_name_lst.index(df_clean['file_name'].values[0]) + num_id) # this
    df_clean['document_id'] = document_id_lst

    res = df_clean.reset_index().groupby('document_id').agg(lambda x: x.nunique())
    for j in range(res['index'].values[0]):
        num_str = str(j+1)
        par_num = 'par' + num_str
        par_lst.append(par_num)
    df_clean['paragraph/chunk'] = par_lst

    domain = urlparse(url_lst[0]).netloc
    df_clean['domain'] = domain

    new_cols = ['db_name', 'table_name', 'issue_date', 'expiration_date', 'file_name', 'document_id', 'url','domain', 'source_type', 'lang', 'category_1', 'category_2', 'title', 'description', 'section', 'paragraph/chunk', 'text', 'updated_date']

    df_clean = df_clean[new_cols]
    return df_clean

def PDF2TEXT_DF(path_list):
    warnings.filterwarnings("ignore")
    Initialize_var()
    pdf_input = path_list.copy()

    output_list = []

    
    for i in range(len(pdf_input)):
        try:
            x = create_table(pdf_input[i], i + 1)
            output_list.append(x)
        except PdfReadError as e1:
            print("Error creating table for: %s - %s" %(pdf_input[i], e1))
        except fitz.FileDataError as e2:
            print("Error creating table for: %s - %s" %(pdf_input[i], e2))

    final = pd.concat(output_list)
    return final

def PDF2TEXT_STR(path_list):
    warnings.filterwarnings("ignore")
    Initialize_var()
    pdf_input = path_list.copy()
    
    json_result = []
    
    for idx,path in enumerate(path_list, start=1):
        text = extract_text_from_path_no_chunk(path)
        clean_text = _clean_missing_1(text)
        result = {"document_id" : idx,
                  "pdf_path" : path,
                  "text" : clean_text}
        json_result.append(result)
        
    return json_result