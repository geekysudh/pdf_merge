from numpy import sort, tile
import streamlit as st
from pypdf import PdfReader, PdfWriter
from io import BytesIO
from streamlit_pdf_viewer import pdf_viewer
import base64

class PDFFile:
    title = ""
    uploadedFile = None
    def __init__(self, uploadedFile, title:str):
        self.uploadedFile = uploadedFile
        self.title = title
    def __str__(self):
        return self.title 

class PDFFiles:
    files = []
    title_text = ""
    def __init__(self):
        self.files = []
    
    def add_file(self, pdf):
        self.files.append(PDFFile(pdf, pdf.name))
    
    def get_files(self):
        return self.files
    
    def contains(self, pdf):
        return any(file.uploadedFile == pdf for file in self.files)

    def move_up(self, pdf_file):
        try:
            print("Move up")
            index_of_file = self.files.index(pdf_file)
            print("Before " + str(self))
            if(index_of_file > 0):
                current_item = self.files[index_of_file]
                self.files[index_of_file] = self.files[index_of_file - 1]
                self.files[index_of_file - 1] = current_item    
                print("MOved")
            print("After "+str(self)) 
        except:
            print("Error")
       
    def move_down(self, pdf_file):
        try:
            index_of_file = self.files.index(pdf_file)
            if(index_of_file < len(self.files) - 1):
                current_tem = self.files[index_of_file]
                self.files[index_of_file] = self.files[index_of_file + 1]
                self.files[index_of_file + 1] = current_tem
        except:
            print("Error")
    def __str__(self):
        return str(self.files)       

def create_title_page(title_text:str):
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
    output = BytesIO(byte_string.encode("latin1"))  # type: ignore # If you really need a BytesIO
    output.seek(0)
    return output

def merge_pdfs(pdf_files, add_title_per_pdf=False):
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
    
    if pdf_files.title_text:
        title_pdf = create_title_page(pdf_files.title_text)
        reader = PdfReader(title_pdf)
        writer.add_page(reader.pages[0])
    
    for pdf in pdf_files.get_files():
        if add_title_per_pdf:
            pdf_name = pdf.name if hasattr(pdf, 'name') else 'Untitled Document'
            custom_title = pdf.title
            print(custom_title)
            title_page = create_title_page(custom_title)
            reader = PdfReader(title_page)
            writer.add_page(reader.pages[0])
        
        reader = PdfReader(pdf.uploadedFile)
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
    
    col1, col2 = st.columns([3, 1])
    title_dict = {}
    st.session_state.title_dict = title_dict
    with col1:
        st.write("Upload multiple PDF files and merge them into one.")
        uploaded_files = st.file_uploader("Upload PDFs", accept_multiple_files=True, type=["pdf"],)
        if "pdf_files" not in st.session_state:
            st.session_state.pdf_files = PDFFiles()
        if uploaded_files:
            for pdf in uploaded_files:
                if st.session_state.pdf_files.contains(pdf) == False:
                    st.session_state.pdf_files.add_file(pdf)
        st.session_state.pdf_files.title_text = st.text_input("Enter Title Page Text (Optional)")
        add_title_per_pdf = st.checkbox("Add a title page for each PDF")
        if st.session_state.pdf_files:
            st.write(f"Uploaded {len(st.session_state.pdf_files.get_files())} PDF files.")
            
            if add_title_per_pdf:
                for i, pdf in enumerate(st.session_state.pdf_files.get_files()):
                    print(str(i) + pdf.title)
                    cola, colb,colc = st.columns([12, 1,1])
                    with cola:
                        pdf.title = st.text_input(f"Enter title for {pdf.title} ", pdf.title)
                    with colb:
                        if st.button(f"⬆️ Up", key=pdf.uploadedFile.name+'up'):   
                            st.session_state.pdf_files.move_up(pdf)
                            st.rerun()
                    with colc:
                        if st.button(f"⬇️ Down" ,key=pdf.uploadedFile.name+'down'):
                            st.session_state.pdf_files.move_down(pdf)
                            st.rerun()
                   
            

    with col2:
        if uploaded_files and st.button("Preview"):
            merged_pdf = merge_pdfs(st.session_state.pdf_files, add_title_per_pdf)
            #display_pdf(merged_pdf)
            pdf_viewer(merged_pdf.read(),  height=600, key="merged_pdf",  )
        
        if st.button("Merge PDFs"):
            merged_pdf = merge_pdfs(st.session_state.pdf_files,  add_title_per_pdf)
            st.success("PDFs merged successfully!")
            file_name = st.session_state.pdf_files.title_text+".pdf" if st.session_state.pdf_files.title_text else "untitled document.pdf"
            st.download_button(
                label="📥 Download Merged PDF",
                data=merged_pdf,
                file_name= file_name,
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()


