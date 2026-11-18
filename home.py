import streamlit as st

st.set_page_config(page_title="Giuseppe Sanfilippo — Streamlit projects", page_icon="🏠", layout="centered")

st.title("🏠 Giuseppe Sanfilippo")
st.subheader("Streamlit projects")
st.write("A collection of interactive applications for probability, statistics and mathematics.")

st.divider()

with st.container(border=True):
    st.subheader("Mixtures of Pólya Urns")
    st.write("Interactive exploration of two Pólya urns, conditional probabilities, elementary constituents and the distribution of X.")
    st.link_button("Open online app", "https://polyags.streamlit.app")

projects = [
    ("Unconditional Coherence Teaching", "Interactive teaching project on unconditional coherence.", "https://unconditional-coherence-teaching.streamlit.app/"),
    ("Conditional Coherence Checker", "Tool for checking conditional coherence.", "https://conditional-coherence-checker-olkedbzeec8whjgfhvchzj.streamlit.app/"),
    ("Mimic GUI", "Interactive project.", "https://eeapprc2tfzcpn7spmd27q.streamlit.app/"),
    ("Birthday Paradox", "Explore the birthday paradox interactively.", "https://birthdayparadox.streamlit.app/"),
    ("Operations Between Two Conditional Events", "Explore operations between two conditional events.", "https://vsafswmanv9gjmxasrskbc.streamlit.app/"),
]

for title, description, url in projects:
    with st.container(border=True):
        st.subheader(title)
        st.write(description)
        st.link_button("Open online app", url)

st.divider()
st.caption("Author: Giuseppe Sanfilippo")
