import streamlit as st
import requests

# ------------------------ Secure Token ------------------------
HF_TOKEN = st.secrets["HF_TOKEN"]  # Loaded from .streamlit/secrets.toml
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# ------------------------ Career Mapping ------------------------
skill_to_career = {
    "python": "Data Scientist",
    "machine learning": "ML Engineer",
    "deep learning": "AI Researcher",
    "web development": "Frontend Developer",
    "react": "Full Stack Developer",
    "java": "Backend Developer",
    "excel": "Data Analyst",
    "communication": "Sales Executive",
    "graphic design": "UI/UX Designer",
    "writing": "Content Writer",
    "teaching": "Educator",
    "sql": "Database Administrator",
    "linux": "System Administrator",
    "cloud": "Cloud Engineer",
    "android": "Mobile App Developer",
    "photography": "Photographer",
    "video editing": "Video Editor"
}

mbti_to_careers = {
    "INTJ": ["Strategic Planner", "Software Architect", "Data Scientist"],
    "INFP": ["Writer", "Counselor", "Artist"],
    "ENFP": ["Creative Director", "Public Relations", "Life Coach"],
    "ISTJ": ["Accountant", "Analyst", "Auditor"],
    "ISFJ": ["Nurse", "Librarian", "Elementary Teacher"],
    "ENTP": ["Entrepreneur", "Marketing Manager", "Product Designer"],
    "ESTJ": ["Project Manager", "Operations Manager", "Military Officer"],
    "ESFP": ["Performer", "Event Planner", "Customer Support"]
}

# ------------------------ MBTI and Career Suggestion ------------------------
def get_mbti(ei, sn, tf, jp):
    return ("E" if ei == "Extroverted" else "I") + \
           ("S" if sn == "Sensing" else "N") + \
           ("T" if tf == "Thinking" else "F") + \
           ("J" if jp == "Judging" else "P")

def suggest_careers(skills_input, mbti_type):
    skills = [s.strip().lower() for s in skills_input.split(",")]
    skill_careers = {skill_to_career[s] for s in skills if s in skill_to_career}
    personality_careers = set(mbti_to_careers.get(mbti_type, []))

    if skill_careers and personality_careers:
        matched = skill_careers & personality_careers
        return list(matched or skill_careers | personality_careers), mbti_type
    return list(skill_careers or personality_careers or ["No suitable career found."]), mbti_type

# ------------------------ Hugging Face Chat Function ------------------------
def query_huggingface(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return [{"generated_text": f"Error: {str(e)}"}]

# ------------------------ Streamlit UI ------------------------
st.set_page_config(page_title="MBTI Career Guide", layout="centered")
tab1, tab2 = st.tabs(["🎯 Career Suggestion", "💬 Chat Assistant"])

# TAB 1: CAREER SUGGESTION
with tab1:
    st.title("🎯 Career Suggestion Based on Skills + MBTI")

    skills = st.text_input("Your Skills (comma-separated)", placeholder="e.g. Python, Communication, SQL")

    st.subheader("MBTI Personality Quiz")
    ei = st.radio("Do you enjoy social gatherings?", ["Extroverted", "Introverted"])
    sn = st.radio("Do you focus more on facts or ideas?", ["Sensing", "Intuitive"])
    tf = st.radio("Are you more logical or empathetic in decisions?", ["Thinking", "Feeling"])
    jp = st.radio("Do you prefer plans or spontaneity?", ["Judging", "Perceiving"])

    if st.button("Suggest Careers"):
        if not skills.strip():
            st.warning("Please enter at least one skill.")
        else:
            mbti = get_mbti(ei, sn, tf, jp)
            suggested, mbti_result = suggest_careers(skills, mbti)
            st.success(f"Your MBTI: {mbti_result}")
            st.write("**Suggested Careers:**")
            for c in suggested:
                st.markdown(f"- {c}")

# TAB 2: CHAT ASSISTANT
with tab2:
    st.subheader("💬 Ask Anything About Careers or MBTI")
    user_query = st.text_input("Type your question below:", key="user_query")

    if st.button("Ask", key="ask_button"):
        if user_query.strip() == "":
            st.warning("Please type something.")
        else:
            with st.spinner("Thinking..."):
                hf_payload = {
                    "inputs": f"<|user|>\n{user_query}\n<|assistant|>\n"
                }
                result = query_huggingface(hf_payload)
                try:
                    response = result[0]["generated_text"].split("<|assistant|>\n")[-1].strip()
                except Exception:
                    response = "Sorry, I couldn't process that. Please try again."

                st.markdown("**You:** " + user_query)
                st.markdown("**Assistant:** " + response)
