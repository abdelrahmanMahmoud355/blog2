import streamlit as st
import openai
import requests
import time

# Set your OpenAI API key
openai.api_key = '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'

# Set your Unsplash API key
UNSPLASH_API_KEY = '7BetPp35y0qr6bPgkG-ofcgmkcRFwx2W5AieG0xejFs'
UNSPLASH_API_URL = 'https://api.unsplash.com/photos/random'


def generate_openai_text(prompt, max_tokens, engine="text-davinci-002", temperature=0.7, n=1):
    attempts = 0
    max_attempts = 5
    wait_time = 20  # seconds

    while attempts < max_attempts:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                max_tokens=max_tokens,
                n=n,
                stop=None,
                temperature=temperature,
            )
            return response.choices[0].text.strip()

        except openai.error.RateLimitError:
            st.warning("Please be patient. It may take some time...")
            time.sleep(wait_time)
            attempts += 1

    st.error("Max retry attempts reached. Please try again later.")
    return None


def generate_blog_with_image(topic):
    # Generate text using OpenAI GPT-3 for overview
    overview_prompt = f"Provide an overview of {topic}."
    overview_text = generate_openai_text(
        prompt=overview_prompt,
        max_tokens=150
    )

    # Generate the introduction paragraph using OpenAI GPT-3
    intro_prompt = f"Write an introduction about {topic}."
    intro_text = generate_openai_text(
        prompt=intro_prompt,
        max_tokens=100
    )

    # Generate the challenges and controversies paragraph using OpenAI GPT-3
    challenges_prompt = f"Discuss the challenges and controversies related to {topic}."
    challenges_text = generate_openai_text(
        prompt=challenges_prompt,
        max_tokens=200
    )

    # Generate the news and updates paragraph using OpenAI GPT-3
    news_prompt = f"Provide news and updates about {topic}."
    news_text = generate_openai_text(
        prompt=news_prompt,
        max_tokens=400
    )

    # Generate the rest of the blog using OpenAI GPT-3
    blog_prompt = f"Write a blog post about {topic}. Include an image related to the topic."
    generated_text = generate_openai_text(
        prompt=blog_prompt,
        max_tokens=400
    )

    # Generate the conclusion paragraph using OpenAI GPT-3
    conclusion_prompt = f"Write a conclusion about {topic}."
    conclusion_text = generate_openai_text(
        prompt=conclusion_prompt,
        max_tokens=150
    )

    return overview_text, intro_text, challenges_text, news_text, generated_text, conclusion_text


def generate_unsplash_image(query):
    image_params = {
        'query': query,
        'client_id': UNSPLASH_API_KEY,
        'orientation': 'landscape',
        'per_page': 1,
    }
    try:
        image_response = requests.get(UNSPLASH_API_URL, params=image_params)
        image_data = image_response.json()
        if 'urls' in image_data:
            image_url = image_data['urls']['regular']
            return image_url
    except Exception as e:
        st.warning(f"Error fetching Unsplash image: {str(e)}")
    return None


def main():
    st.title("Blog Generator ")

    # Get user input for the topic
    topic = st.text_input("Enter the topic:")

    # Generate blog and image on button click
    if st.button("Generate Blog"):
        if topic:
            # Generate blog and fetch images
            overview_text, intro_text, challenges_text, news_text, blog_text, conclusion_text = generate_blog_with_image(
                topic)

            # Display the generated text
            st.header(f"Blog about {topic}:")

            st.subheader("Table of Contents:")
            st.write("1. Overview")
            st.write("2. Introduction")
            st.write("3. Challenges and Controversies")
            st.write("4. News and Updates")
            st.write("5. General")
            st.write("6. Conclusion")

            # Display the overview
            st.markdown(
                f'<div style="background-color:#f0f0f0; padding: 10px; border-radius: 10px; margin-bottom: 15px;">{overview_text}</div>',
                unsafe_allow_html=True
            )

            # Display the generated image after the overview
            overview_image_url = generate_unsplash_image(topic)
            if overview_image_url:
                st.image(
                    overview_image_url, caption=f"Image related to {topic}", clamp=True, width=None)

            # Display the introduction in two columns
            col1, col2 = st.columns([2, 1])

            col1.write("***Introduction***")
            col1.write(intro_text)

            # Display the related image for the introduction on the right
            intro_image_url = generate_unsplash_image(topic)
            if intro_image_url:
                col2.image(
                    intro_image_url, clamp=True, width=None)

            # Display the challenges and controversies section
            st.markdown(
                f'<div style="background-color:#f0f0f0; padding: 10px; border-radius: 10px; margin-bottom: 15px;">'
                f'<h6>Challenges and Controversies</h6>{challenges_text}'
                '</div>',
                unsafe_allow_html=True
            )

            # Display the news and updates section
            st.write("***News and Updates***")
            # Display the news image and text in two columns
            col1, col2 = st.columns([1, 2])
            news_image_url = generate_unsplash_image(topic)
            if news_image_url:
                col1.image(
                    news_image_url, clamp=True, width=None)
            col2.write(news_text)

            # Display the remaining paragraphs
            st.markdown(
                f'<div style="background-color:#f0f0f0; padding: 10px; border-radius: 10px; margin-bottom: 15px;">'
                f'<h5>General</h5>{blog_text}'
                '</div>',
                unsafe_allow_html=True
            )

            # Display the conclusion
            st.write("***Conclusion***")
            st.write(conclusion_text)

        else:
            st.warning("Please enter a topic.")


if __name__ == "__main__":
    main()
