import streamlit as st
from PIL import Image
from api_calling import note_generator, audio_transcription, quiz_generator
from prepare_txt_clean_audio import prepare_text_for_audio

st.title("Note Summary and Quiz Generator")
st.markdown("Upload upto 3 images to generate Note summary and Quizzes")
st.divider()

with st.sidebar:
    
    st.header("Controls")
    images=st.file_uploader(
        "Upload the photos of your note",
        type=['jpg', 'jpeg','png'],
        accept_multiple_files=True
    )

    pill_images = []

    for img in images:
        pill_img = Image.open(img)
        pill_images.append(pill_img)

    if images:
        if len(images)>3:
            st.error("Upload at max 3 images")
        else:
            col = st.columns(len(images))

            st.subheader("Uploaded images", anchor=False)

            for i,img in enumerate(images):
                with col[i]:
                    st.image(img)

    #difficulty
    selected_option=st.selectbox(
        "Enter the difficulty of your quiz",
        ("Easy","Medium","Hard"),
        index=None
    )


    if selected_option:
        st.markdown(f"You selected **{selected_option}** as difficulty of your quiz")

    pressed =st.button("Click the button to initiate AI", type="primary")


if pressed:
    if not images:
        st.error("You must upload atleast 1 image")
    if not selected_option:
        st.error("You must select a difficulty")

    if images and selected_option:


        # Note
        with st.container(border=True):
            st.subheader("Your note", anchor=False)

            with st.spinner("Ai is generating the notes"):
                generated_notes = note_generator(pill_images)
                st.markdown(generated_notes)


        # Audio Transcription
        with st.container(border=True):
            st.subheader("Audio Transcription", anchor=False)

            with st.spinner("Ai is generating the audio-notes"):
                st.audio(audio_transcription(prepare_text_for_audio(generated_notes)))


        # Quiz
        with st.container(border=True):
            st.subheader(f"Quiz {selected_option} Difficulty", anchor=False)

            with st.spinner("Ai is generating the quizzes"):
                quiz = quiz_generator(pill_images, selected_option)
                st.markdown(quiz)
