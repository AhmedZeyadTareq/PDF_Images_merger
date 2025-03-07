import fitz  # PyMuPDF
import streamlit as st
import os
from PIL import Image  # For image processing

# Path to your logo
logo_link = r"images\formal image.jpg"


def convert_image_to_pdf(image_path):
    """Convert an image to a PDF file"""
    image = Image.open(image_path)
    pdf_path = f"{image_path}.pdf"
    image.save(pdf_path, "PDF", resolution=100.0)
    return pdf_path


def merge_files(file_paths, output_path):
    """Merge PDF and image files into a single PDF"""
    merged_pdf = fitz.open()

    for file in file_paths:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            # If the file is an image, convert it to PDF first
            pdf_path = convert_image_to_pdf(file)
            with fitz.open(pdf_path) as doc:
                merged_pdf.insert_pdf(doc)
            os.remove(pdf_path)  # Delete the temporary file after merging
        elif file.lower().endswith('.pdf'):
            # If the file is a PDF, add it directly
            with fitz.open(file) as doc:
                merged_pdf.insert_pdf(doc)
        else:
            st.warning(f"Unsupported file type: {file}")

    merged_pdf.save(output_path)
    merged_pdf.close()


def main():
    # Sidebar with logo and description
    with st.sidebar:
        if os.path.exists(logo_link):
            logo_image = Image.open(logo_link)
            st.image(logo_image, width=150)  # Adjust width as needed
        else:
            st.warning("Logo not found. Please check the logo path.")

        st.write("### This service is implemented by:")
        st.write("**Eng.Ahmed Zeyad Tareq**")
        st.write("📌 Data Scientist")
        st.write("🎓 Master of AI Engineering")
        st.write("📷 Instagram: [@adlm7](https://www.instagram.com/adlm7)")
        st.write("🔗 LinkedIn: [Ahmed Zeyad Tareq](https://www.linkedin.com/in/ahmed-zeyad-tareq)")

    # Main application
    st.title("PDF and Image Merger")
    st.write("Select PDF files or images (PNG, JPG, JPEG) to merge them into a single PDF.")

    # File uploader
    uploaded_files = st.file_uploader("Choose PDF or image files", type=["pdf", "png", "jpg", "jpeg"],
                                      accept_multiple_files=True)

    # Output file name
    output_filename = st.text_input("Output file name (without .pdf)", value="merged_file")
    output_path = f"{output_filename}.pdf"

    # Merge button
    if st.button("Merge Files"):
        if uploaded_files:
            file_paths = []
            for uploaded_file in uploaded_files:
                # Save uploaded files temporarily
                temp_file_path = uploaded_file.name
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                file_paths.append(temp_file_path)

            # Merge files
            merge_files(file_paths, output_path)

            # Download the merged file
            with open(output_path, "rb") as f:
                st.download_button(
                    label="Download Merged File",
                    data=f,
                    file_name=output_path,
                    mime="application/pdf"
                )

            # Delete temporary files
            for file in file_paths:
                if os.path.exists(file):
                    os.remove(file)
                else:
                    st.warning(f"File not found: {file}")

            # Delete the merged file
            if os.path.exists(output_path):
                os.remove(output_path)
            else:
                st.warning(f"File not found: {output_path}")
        else:
            st.error("Please select files to merge.")


if __name__ == "__main__":
    main()
