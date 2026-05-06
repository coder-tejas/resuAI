import streamlit as st
import os
import sys
import json
import markdown2
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from api.services.jd_parser import parse_jd
from api.services.company_enrichment import enrich_company
from api.services.project_selector import select_projects
from api.services.bullet_optimizer import optimize_bullets
from api.services.skills_optimizer import optimize_skills
from api.services.resume_generator import generate_resume

st.set_page_config(page_title="resoAI", page_icon="📄", layout="wide")

st.title("resoAI")
st.markdown("Generate ATS-optimized, tailored resumes for each job application.")

if "OPENROUTER_API_KEY" not in os.environ:
    api_key = st.sidebar.text_input("OpenRouter API Key", type="password")
    if api_key:
        os.environ["OPENROUTER_API_KEY"] = api_key
        st.sidebar.success("API key set!")

with st.expander("Step 1: Job Description", expanded=True):
    jd_text = st.text_area("Paste Job Description", height=150, placeholder="Paste the full job description...")
    col1, col2 = st.columns(2)
    with col1:
        company = st.text_input("Company Name", placeholder="e.g., Stripe")
    with col2:
        role = st.text_input("Role Title", placeholder="e.g., Backend Engineer")

with st.expander("Step 2: Projects", expanded=True):
    uploaded_files = st.file_uploader("Upload project .md files", type="md", accept_multiple_files=True)
    
    projects = []
    if uploaded_files:
        for f in uploaded_files:
            content = f.read().decode()
            lines = content.split('\n---\n')
            name = f.name.replace('.md', '')
            tech = ''
            description = content
            
            if len(lines) > 1:
                frontmatter = lines[0]
                desc = '\n---\n'.join(lines[1:])
                
                for line in frontmatter.split('\n'):
                    if line.startswith('name:'):
                        name = line.replace('name:', '').strip()
                    elif line.startswith('tech:'):
                        tech = line.replace('tech:', '').strip()
                description = desc.strip()
            
            projects.append({"name": name, "tech": tech, "description": description})
        
        st.success(f"Loaded {len(projects)} project(s)")
        for p in projects:
            st.caption(f"**{p['name']}** ({p['tech']})")

with st.expander("Step 3: Personal Info", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="Your Name")
        email = st.text_input("Email", placeholder="email@example.com")
    with col2:
        phone = st.text_input("Phone", placeholder="+1 (555) 123-4567")
        github = st.text_input("GitHub", placeholder="github.com/username")

with st.expander("Step 4: Skills", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        languages = st.text_input("Languages", placeholder="Python, JavaScript, Go")
        frameworks = st.text_input("Frameworks", placeholder="React, FastAPI, Django")
    with col2:
        tools = st.text_input("Tools", placeholder="Docker, Git, AWS")
        libraries = st.text_input("Libraries / Databases", placeholder="PostgreSQL, Redis")

with st.expander("Step 5: Education", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        school = st.text_input("School", placeholder="University Name")
    with col2:
        degree = st.text_input("Degree", placeholder="B.S. Computer Science")
    grad_year = st.text_input("Graduation Year", placeholder="2024")

run_pipeline = st.button("Generate Resume", type="primary", disabled=not jd_text or not projects)

if run_pipeline:
    if not jd_text:
        st.error("Please provide a job description")
    elif not projects:
        st.error("Please upload at least one project file")
    else:
        with st.spinner("Running pipeline..."):
            progress = st.progress(0)
            status_text = st.empty()
            
            try:
                status_text.text("Parsing JD...")
                progress.progress(15)
                jd_info = None
                
                import asyncio
                jd_info = asyncio.run(parse_jd(jd_text, company))
                st.session_state["jd_info"] = jd_info
                
                status_text.text("Enriching company info...")
                progress.progress(30)
                company_info = None
                if company:
                    company_info = asyncio.run(enrich_company(company))
                
                status_text.text("Selecting projects...")
                progress.progress(50)
                selected = asyncio.run(select_projects(projects, jd_info, company_info))
                selected_projects = selected["selected_projects"]
                st.session_state["selected_projects"] = selected_projects
                
                status_text.text("Optimizing bullets...")
                progress.progress(70)
                optimized = asyncio.run(optimize_bullets(selected_projects, jd_info))
                optimized_projects = optimized["optimized_projects"]
                st.session_state["optimized_projects"] = optimized_projects
                
                status_text.text("Optimizing skills...")
                progress.progress(85)
                skills_input = {
                    "Languages": languages,
                    "Frameworks": frameworks,
                    "Tools": tools,
                    "Libraries": libraries
                }
                skills_result = asyncio.run(optimize_skills(skills_input, jd_info))
                optimized_skills = skills_result["optimized_skills"]
                st.session_state["optimized_skills"] = optimized_skills
                
                status_text.text("Generating PDF...")
                progress.progress(95)
                
                pdf_path = generate_resume(
                    {"name": name, "email": email, "phone": phone, "github": github, "linkedin": ""},
                    [{"school": school, "degree": degree, "year": grad_year}],
                    optimized_projects,
                    optimized_skills,
                    jd_info
                )
                
                progress.progress(100)
                st.session_state["pdf_path"] = pdf_path
                
                st.success("Resume generated!")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

if "pdf_path" in st.session_state:
    st.divider()
    st.subheader("Generated Resume")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        with open(st.session_state["pdf_path"], "rb") as f:
            st.download_button("Download PDF", f, file_name="resume.pdf", mime="application/pdf")
    
    with col2:
        st.subheader("Selected Projects")
        for p in st.session_state.get("optimized_projects", []):
            with st.container():
                st.markdown(f"**{p['name']}** ({p['tech']})")
                for bullet in p.get("bullets", []):
                    st.markdown(f"- {bullet}")
                st.markdown("")
    
    st.subheader("Optimized Skills")
    for category, skills in st.session_state.get("optimized_skills", {}).items():
        st.markdown(f"**{category}:** {', '.join(skills) if isinstance(skills, list) else skills}")