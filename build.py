import PyInstaller.__main__
import os
import sys


PyInstaller.__main__.run([
    '--name=RAG-QA-System',
    '--onefile',
    '--windowed',
    '--add-data=docs;docs',
    '--hidden-import=streamlit',
    '--hidden-import=langchain',
    '--hidden-import=langchain_community',
    '--hidden-import=chromadb',
    '--hidden-import=PyPDF2',
    '--hidden-import=docx',
    'app.py',
])