import streamlit as st
import pandas as pd
import os
from PIL import Image
from datetime import datetime

class ImageRater:
    def __init__(self):
        self.setup_session_state()
        
    @staticmethod
    def setup_session_state():
        if 'current_image_index' not in st.session_state:
            st.session_state.current_image_index = 0
        if 'ratings' not in st.session_state:
            st.session_state.ratings = []
        if 'rater_name' not in st.session_state:
            st.session_state.rater_name = ''
            
    def save_ratings(self):
        """Create downloadable CSV of ratings"""
        if st.session_state.ratings:
            df = pd.DataFrame(st.session_state.ratings)
            csv = df.to_csv(index=False)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'ratings_{st.session_state.rater_name}_{timestamp}.csv'
            
            st.download_button(
                label="📥 Download Ratings CSV",
                data=csv,
                file_name=filename,
                mime='text/csv'
            )
            return filename
        return None

    def load_images(self):
        """Load all images from the images folder"""
        image_dir = "images"  # Changed to use relative path
        if not os.path.exists(image_dir):
            st.error("Images directory not found!")
            return []
        return sorted([f for f in os.listdir(image_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

    def run(self):
        st.title("Bottle Aesthetic Rating Study")
        
        if not st.session_state.rater_name:
            self.get_rater_name()
            return

        images = self.load_images()
        if not images:
            st.error("No images found in the directory!")
            return

        self.display_rating_interface(images)

    def get_rater_name(self):
        st.write("### Welcome to the Bottle Rating Study!")
        st.write("""
        Please enter your name to begin rating the bottles.
        You will be rating each bottle on four different aesthetic aspects using a 1-7 scale.
        """)
        
        rater_name = st.text_input("Enter your name:", key="name_input")
        if rater_name:
            st.session_state.rater_name = rater_name
            st.rerun()

    def display_rating_interface(self, images):
        # Display progress
        progress = st.session_state.current_image_index / len(images)
        st.progress(progress)
        st.write(f"Image {st.session_state.current_image_index + 1} of {len(images)}")

        # Display current image
        if st.session_state.current_image_index < len(images):
            current_image = images[st.session_state.current_image_index]
            img_path = os.path.join("images", current_image)
            
            try:
                img = Image.open(img_path)
                st.image(img, width=400)
            except Exception as e:
                st.error(f"Error loading image: {str(e)}")
                return

            # Rating inputs with descriptions
            st.write("### Please rate the following aspects:")
            
            st.write("1. Overall Image Aesthetics")
            st.write("*(1 = least aesthetically pleasing, 7 = most aesthetically pleasing)*")
            overall_rating = st.select_slider(
                "Overall Rating",
                options=range(1, 8),
                value=4
            )
            
            st.write("\n2. Shape Aesthetics")
            st.write("*(1 = least aesthetically pleasing, 7 = most aesthetically pleasing)*")
            shape_rating = st.select_slider(
                "Shape Rating",
                options=range(1, 8),
                value=4
            )
            
            st.write("\n3. Color Aesthetics")
            st.write("*(1 = least aesthetically pleasing, 7 = most aesthetically pleasing)*")
            color_rating = st.select_slider(
                "Color Rating",
                options=range(1, 8),
                value=4
            )
            
            st.write("\n4. Label Aesthetics")
            st.write("*(1 = least aesthetically pleasing, 7 = most aesthetically pleasing)*")
            label_rating = st.select_slider(
                "Label Rating",
                options=range(1, 8),
                value=4
            )

            # Navigation buttons
            st.write("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ Previous", key="prev"):
                    if st.session_state.current_image_index > 0:
                        st.session_state.current_image_index -= 1
                        st.rerun()

            with col2:
                if st.button("Next ➡️", key="next"):
                    # Save ratings
                    st.session_state.ratings.append({
                        'Rater': st.session_state.rater_name,
                        'Image': current_image,
                        'Overall_Rating': overall_rating,
                        'Shape_Rating': shape_rating,
                        'Color_Rating': color_rating,
                        'Label_Rating': label_rating,
                        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    # Move to next image
                    if st.session_state.current_image_index < len(images) - 1:
                        st.session_state.current_image_index += 1
                        st.rerun()
                    else:
                        self.save_ratings()
                        st.success("🎉 All ratings completed! Thank you for your participation.")
                        st.write("Please download your ratings using the button above.")

            # Save progress button
            if st.button("💾 Save Progress", key="save"):
                self.save_ratings()
                st.success("Progress saved! Click the download button above to save your ratings.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Bottle Rating Study",
        page_icon="🏺",
        layout="centered"
    )

    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
        }
        .stProgress .st-bo {
            background-color: #2ecc71;
        }
        </style>
    """, unsafe_allow_html=True)

    rater = ImageRater()
    rater.run()