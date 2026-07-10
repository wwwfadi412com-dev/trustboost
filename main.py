import streamlit as st

from core.pipeline import TrustBoostPipeline
from db.crud import create_user_if_not_exists, deduct_credit, get_user_credits
from db.database import init_db


st.set_page_config(page_title="TrustBoost - E-E-A-T Injector", layout="wide")
init_db()

if "email" not in st.session_state:
    st.session_state.email = None

with st.sidebar:
    st.title("🔐 Login")
    email = st.text_input("Enter your email to continue:")
    if st.button("Login"):
        normalized_email = email.strip().lower()
        if normalized_email:
            st.session_state.email = normalized_email
            create_user_if_not_exists(normalized_email)
            st.rerun()

    if st.session_state.email:
        credits = get_user_credits(st.session_state.email)
        st.success(f"Logged in: {st.session_state.email}")
        st.info(f"Credits remaining: {credits}")

st.title("🚀 TrustBoost: E-E-A-T Citation Injector")
st.markdown(
    "Transform your AI-generated content into highly trusted, E-E-A-T compliant "
    "articles by automatically injecting real statistics and sources."
)

if not st.session_state.email:
    st.warning("Please login from the sidebar to use the tool.")
else:
    credits = get_user_credits(st.session_state.email)
    if credits <= 0:
        st.error("❌ You have no credits left. Please upgrade your plan to continue!")
    else:
        input_article = st.text_area(
            "📄 Paste Your Article Here:",
            height=300,
            placeholder="Write or paste your article...",
        )

        if st.button("✨ Boost E-E-A-T & Add Citations", type="primary"):
            if not input_article.strip():
                st.error("Please paste an article first.")
            else:
                with st.spinner(
                    "🧠 Analyzing claims, searching the web, and injecting facts..."
                ):
                    try:
                        pipeline = TrustBoostPipeline()
                        result = pipeline.process_article(input_article)

                        if result["success"]:
                            deduct_credit(st.session_state.email)
                            st.success(
                                f"✅ Done! Added {result['citations_added']} credible citations."
                            )

                            st.subheader("📝 Optimized Article")
                            st.markdown(result["final_article"])

                            with st.expander("🔍 View Citation Details"):
                                for item in result["details"]:
                                    st.markdown(f"**Original:** {item['original']}")
                                    st.markdown(f"**Modified:** {item['modified']}")
                                    st.markdown(f"**Source:** [Link]({item['source']})")
                                    st.divider()
                        else:
                            st.warning(result["message"])
                    except Exception as exc:
                        st.error(f"An error occurred: {exc}")
