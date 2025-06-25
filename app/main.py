# app/main.py

import streamlit as st

try:
    from backend.llm_query import parse_query_with_mistral
    from backend.recommender import personalized_search, rerank_results

    st.set_page_config(page_title="Smart Recommender System", layout="centered")
    st.title("🎯 Smart Recommender System")

    with st.sidebar:
        # Content type selection
        content_type = st.selectbox("🎬 Choose content type:", ["book", "movie", "song"])

        # Optional: user interest or profile
        user_profile = st.text_input("💡 (Optional) Describe your interests")

    # Input: user query
    user_query = st.text_input("🔍 What are you looking for (books, movies, songs)?")

    if user_query:
        # Step 1: Refine query
        with st.spinner("Refining your query with Mistral..."):
            refined_query = parse_query_with_mistral(user_query)
            st.success("✅ Query refined")
            st.write(f"Refined Query: {refined_query}")

        # Step 2: Personalized search
        with st.spinner("Searching..."):
            results = personalized_search(refined_query, user_input_profile=user_profile, content_type=content_type)

        # Step 3: Rerank results
        with st.spinner("Reranking results..."):
            ranked_titles = list(rerank_results(refined_query, results))

        # Step 4: Display results
        st.subheader(f"📌 Recommended {content_type.capitalize()}s")

        ranked_items = sorted(
            results,
            key=lambda x: ranked_titles.index(x['metadata']['title'])
            if x['metadata']['title'] in ranked_titles else 999
        )

        for item in ranked_items:
            st.markdown(f"### {item['metadata']['title']} by {item['metadata']['author']}")
            st.write(item['metadata']['description'])

except Exception as e:
    st.error(f"⚠ An error occurred:\n\n{e}")