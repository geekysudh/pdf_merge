# Software Requirements Specification (SRS)

## 1. Introduction
### 1.1 Purpose
The **Streamlit PDF Merger App** is a web-based tool that allows users to upload multiple PDF files, merge them into a single document, and optionally insert a custom title page. The app provides a seamless user experience with an interactive interface and a downloadable merged file.

### 1.2 Scope
- Users can upload multiple PDFs and merge them.
- An optional title page can be inserted at the beginning of the merged document.
- The final merged PDF is available for direct download.
- The app runs locally using **Streamlit** and processes PDFs in memory.

### 1.3 Definitions, Acronyms, and Abbreviations
- **PDF**: Portable Document Format
- **UI**: User Interface
- **Streamlit**: A Python framework for building interactive web applications
- **pypdf**: A Python library for PDF manipulation

### 1.4 References
- Streamlit Documentation: [https://docs.streamlit.io](https://docs.streamlit.io)
- pypdf Documentation: [https://pypdf.readthedocs.io](https://pypdf.readthedocs.io)

---
## 2. Functional Requirements
### 2.1 User Interface
- The app should provide an intuitive UI with:
  - A file uploader for PDF selection
  - A text input for title page entry
  - A "Merge PDFs" button to process the files
  - A "Download Merged PDF" button

### 2.2 PDF Merging
- The app should allow users to upload **multiple PDF files**.
- The system should **merge PDFs in the order of selection**.
- If the user provides a **title page**, it should be **inserted as the first page**.
- The merged PDF should be **available for download immediately**.

### 2.3 Title Page Generation
- The app should generate a **title page dynamically**.
- The title page should have:
  - A **centered title** in **large font size**.
  - A simple layout using `fpdf`.

### 2.4 File Handling
- PDFs should be processed **in memory** using `BytesIO`.
- No files should be stored on disk for security and efficiency.

---
## 3. Non-Functional Requirements
### 3.1 Performance
- The system should merge PDFs **within a few seconds**.
- It should handle at least **10 PDFs of 5MB each** efficiently.

### 3.2 Scalability
- The app should support **local execution**.
- Future versions may include **cloud storage integration** (e.g., AWS S3, Google Drive).

### 3.3 Usability
- The UI should be **simple and intuitive**, requiring no technical knowledge.
- Users should get **instant feedback** after uploading and merging files.

### 3.4 Security
- The app should not store any uploaded files.
- PDFs should be processed **locally in memory**.

---
## 4. System Setup & Installation
### 4.1 Environment Setup
1. Create a virtual environment:
   ```sh
   python -m venv venv
   ```
2. Activate the virtual environment:
   - **Windows**:
     ```sh
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```sh
     source venv/bin/activate
     ```
3. Install dependencies:
   ```sh
   pip install streamlit pypdf fpdf
   ```
4. Run the application:
   ```sh
   streamlit run pdf_merger.py
   ```

---
## 5. Future Enhancements
- **Cloud Storage Support** (Upload/download from AWS S3, Google Drive)
- **Customizable Title Page** (Fonts, colors, additional text)
- **Password Protection for PDFs** (Encrypt merged output)
- **Mobile-friendly UI** for easy access on different devices

