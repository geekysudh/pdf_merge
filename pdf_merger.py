import streamlit as st
from pypdf import PdfReader, PdfWriter
from io import BytesIO
from streamlit_pdf_viewer import pdf_viewer
import base64
def create_title_page(title_text):
    """
    Creates a title page PDF with the given text.
    
    Parameters:
        title_text (str): The text to be displayed on the title page.
    
    Returns:
        BytesIO: The generated title page as a PDF file in memory.
    """
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=24)
    text_width = pdf.get_string_width(title_text)
    page_width = pdf.w
    page_height = pdf.h
    x = (page_width - text_width) / 2
    y = page_height / 2
    pdf.set_xy(x, y)
    pdf.cell(text_width, 10, title_text, ln=True, align='C')
    
    
    
    byte_string = pdf.output(dest='S')  # Probably what you want
    output = BytesIO(byte_string.encode("latin1"))  # If you really need a BytesIO
    output.seek(0)
    return output

def merge_pdfs(pdf_files, title_text, title_dict, add_title_per_pdf=False):
    """
    Merges multiple PDF files into a single PDF, adding a title page for each PDF.
    
    Parameters:
        pdf_files (list): A list of uploaded PDF files.
        title_text (str): The title text for the optional title page at the beginning.
        title_dict (dict): Dictionary mapping filenames to user-defined titles.
        add_title_per_pdf (bool): Whether to add a title page for each PDF.
    
    Returns:
        BytesIO: The merged PDF file in memory.
    """
    writer = PdfWriter()
    
    if title_text:
        title_pdf = create_title_page(title_text)
        reader = PdfReader(title_pdf)
        writer.add_page(reader.pages[0])
    
    for pdf in pdf_files:
        if add_title_per_pdf:
            pdf_name = pdf.name if hasattr(pdf, 'name') else 'Untitled Document'
            custom_title = title_dict.get(pdf.name, pdf_name)
            print(custom_title)
            title_page = create_title_page(custom_title)
            reader = PdfReader(title_page)
            writer.add_page(reader.pages[0])
        
        reader = PdfReader(pdf)
        for page in reader.pages:
            writer.add_page(page)
    
    output_pdf = BytesIO()
    writer.write(output_pdf)
    writer.close()
    output_pdf.seek(0)
    return output_pdf
   



def main():
    st.set_page_config(layout="wide")
    """
    Streamlit app main function that provides the user interface for uploading, merging,
    and downloading PDF files.
    """
    st.title("📄 PDF Merger App")

    
    col1, col2 = st.columns([1, 2])
    title_dict = {}
    st.session_state.title_dict = title_dict
    with col1:
        st.write("Upload multiple PDF files and merge them into one.")
        uploaded_files = st.file_uploader("Upload PDFs", accept_multiple_files=True, type=["pdf"])
        st.session_state.title_text = st.text_input("Enter Title Page Text (Optional)")
    
        add_title_per_pdf = st.checkbox("Add a title page for each PDF")
        if uploaded_files:
            st.write(f"Uploaded {len(uploaded_files)} PDF files.")
            
            if add_title_per_pdf:
                for pdf in uploaded_files:
                    title_dict[pdf.name] = st.text_input(f"Enter title for {pdf.name}", pdf.name)
            if st.button("Merge PDFs"):
                merged_pdf = merge_pdfs(uploaded_files, title_text, title_dict, add_title_per_pdf)
                st.success("PDFs merged successfully!")
            
                st.download_button(
                    label="📥 Download Merged PDF",
                    data=merged_pdf,
                    file_name="merged_document.pdf",
                    mime="application/pdf"
                )

    with col2:
        if uploaded_files and st.button("Preview Merge PDFs"):
            st.write("Preview Merged PDF")
            merged_pdf = merge_pdfs(uploaded_files, st.session_state.title_text, st.session_state.title_dict, add_title_per_pdf)
            #display_pdf(merged_pdf)
            pdf_viewer(merged_pdf.read(),  height=600, key="merged_pdf",  )

if __name__ == "__main__":
    main()


