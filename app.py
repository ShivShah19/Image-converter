import os
import zipfile
import streamlit as st
from PIL import Image

# custom CSS from the style.css file
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Streamlit web app title and subtitle
st.markdown('<p class="title">Image Converter - PNG/JPG to WebP</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload PNG or JPG images to convert them to WebP format.</p>', unsafe_allow_html=True)

output_folder = 'output_images'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to convert image to WebP format
def convert_to_webp(input_image, output_filename):
    try:
        img = Image.open(input_image)
        output_path = os.path.join(output_folder, output_filename)
        
        img.save(output_path, 'WebP')

        return output_path
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to create a ZIP file of all converted WebP images
def create_zip(output_paths, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in output_paths:
            zipf.write(file_path, os.path.basename(file_path))
    return zip_filename

# multiple image upload functionality
uploaded_files = st.file_uploader("Choose images (PNG/JPG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if 'image_offset' not in st.session_state:
    st.session_state['image_offset'] = 0


if uploaded_files:
    # store the converted images (list)
    output_paths = []

    for uploaded_file in uploaded_files:
        output_filename = os.path.splitext(uploaded_file.name)[0] + '.webp'

        # Convert the image to WebP format
        output_path = convert_to_webp(uploaded_file, output_filename)
        
        if output_path:
            output_paths.append(output_path)

    # All buttons 
    if output_paths:
        st.markdown('<p class="section-header">Download the converted WebP images:</p>', unsafe_allow_html=True)

        # create individual download buttons
        for output_path in output_paths:
            with open(output_path, "rb") as f:
                st.download_button(
                    label=f"Download {os.path.basename(output_path)}",
                    data=f,
                    file_name=os.path.basename(output_path),
                    mime="image/webp"
                )

        # Create "Download All" button
        zip_filename = "converted_images.zip"
        zip_file = create_zip(output_paths, zip_filename)

        with open(zip_file, "rb") as f:
            st.download_button(
                label="Download All as ZIP",
                data=f,
                file_name=zip_filename,
                mime="application/zip"
            )
    else:
        st.write("No valid images were converted.")
