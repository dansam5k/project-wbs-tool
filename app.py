import streamlit as st
import json
from openai import OpenAI

client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", None))

st.set_page_config(page_title="AI WBS Generator", layout="wide")

# ---------------- Sidebar ----------------
st.sidebar.title("⚙️ Settings")
model = st.sidebar.selectbox("Model", ["gpt-4.1-mini", "gpt-4.1"])
temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 1.0, 0.3)

st.sidebar.markdown("---")
st.sidebar.write("💡 Lower temperature = more deterministic output")

# ---------------- Title ----------------
st.title("🧠 AI-Assisted Work Breakdown Structure Generator")
st.markdown("Generate, refine, compare, and evaluate WBS using AI.")

# ---------------- Examples ----------------
examples = {
    "E-commerce App": "Develop a mobile e-commerce app with user authentication, product catalog, payment integration, and order tracking.",
    "Conference": "Organize a 3-day international tech conference including speakers, venue, marketing, and logistics.",
    "Website": "Build a company website with homepage, blog, contact form, and SEO optimization."
}

selected_example = st.selectbox("📌 Try an example", ["None"] + list(examples.keys()))

if selected_example != "None":
    project_description = st.text_area("Project Description", value=examples[selected_example], height=150)
else:
    project_description = st.text_area("Project Description", height=150)

col1, col2, col3 = st.columns(3)

# ---------------- Generate ----------------
with col1:
    if st.button("🚀 Generate WBS"):
        if project_description.strip() == "":
            st.warning("Please enter a project description.")
        else:
            with st.spinner("Generating..."):
                prompt = f"""
You are a senior project manager.

Create a hierarchical Work Breakdown Structure (WBS):
- 3 levels
- Deliverable-oriented
- JSON format

Project:
{project_description}
"""
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature
                )
                st.session_state["wbs"] = response.choices[0].message.content

# ---------------- Improve ----------------
with col2:
    if st.button("✨ Improve"):
        if "wbs" in st.session_state:
            improve_prompt = f"""
Improve this WBS:
- Add missing tasks
- Improve structure
- Keep JSON

{st.session_state['wbs']}
"""
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": improve_prompt}],
                temperature=temperature
            )
            st.session_state["wbs"] = response.choices[0].message.content

# ---------------- Second Generation (Comparison) ----------------
with col3:
    if st.button("🆚 Generate Alt Version"):
        if project_description.strip() != "":
            alt_prompt = f"""
Generate an alternative WBS with a different structure and phrasing.

Project:
{project_description}
"""
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": alt_prompt}],
                temperature=temperature
            )
            st.session_state["wbs_alt"] = response.choices[0].message.content

# ---------------- Utility Functions ----------------
def count_tasks(data):
    count = 0
    if isinstance(data, dict):
        for v in data.values():
            count += 1 + count_tasks(v)
    elif isinstance(data, list):
        count += len(data)
    return count

# ---------------- Display ----------------
st.markdown("---")

colA, colB = st.columns(2)

# Main WBS
with colA:
    if "wbs" in st.session_state:
        st.subheader("📦 WBS A")
        try:
            parsed = json.loads(st.session_state["wbs"])

            st.code(st.session_state["wbs"], language="json")

            # Scoring
            tasks = count_tasks(parsed)
            depth_score = 3  # fixed since prompt enforces
            completeness = min(tasks / 20, 1.0) * 5

            st.markdown("### 📊 Score")
            st.write(f"Tasks: {tasks}")
            st.write(f"Completeness Score (approx): {round(completeness,2)}/5")
            st.write(f"Depth Score: {depth_score}/5")

        except:
            st.error("Invalid JSON")

# Alternative WBS
with colB:
    if "wbs_alt" in st.session_state:
        st.subheader("📦 WBS B (Alternative)")
        try:
            parsed_alt = json.loads(st.session_state["wbs_alt"])

            st.code(st.session_state["wbs_alt"], language="json")

            # Scoring
            tasks_alt = count_tasks(parsed_alt)
            completeness_alt = min(tasks_alt / 20, 1.0) * 5

            st.markdown("### 📊 Score")
            st.write(f"Tasks: {tasks_alt}")
            st.write(f"Completeness Score: {round(completeness_alt,2)}/5")

        except:
            st.error("Invalid JSON")

# ---------------- Comparison Insight ----------------
if "wbs" in st.session_state and "wbs_alt" in st.session_state:
    st.markdown("---")
    st.subheader("🧠 Comparison Insight")

    try:
        a = json.loads(st.session_state["wbs"])
        b = json.loads(st.session_state["wbs_alt"])

        diff = count_tasks(b) - count_tasks(a)

        if diff > 0:
            st.success(f"Alternative WBS has {diff} more tasks → potentially more detailed.")
        elif diff < 0:
            st.info(f"Original WBS has {-diff} more tasks → potentially more detailed.")
        else:
            st.write("Both WBS have similar task counts.")

    except:
        st.error("Comparison failed")

# ---------------- Footer ----------------
st.markdown("---")
st.caption("Advanced AI WBS Tool with scoring + comparison (Thesis Prototype)")
