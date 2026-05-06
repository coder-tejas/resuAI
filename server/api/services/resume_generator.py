import os
import subprocess
import tempfile
import shutil
from jinja2 import Template

LATEX_TEMPLATE = r"""
\documentclass[a4,11pt]{article}
\usepackage[left=0.75in, right=0.75in, top=0.75in, bottom=0.75in]{geometry}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{fontenc}
\usepackage{iftex}

\ifLuaTeX
  \usepackage{fontspec}
\else
  \usepackage[utf8]{inputenc}
\fi

\pagestyle{empty}
\titlespacing\section}{0pt}{6pt}{4pt}
\titleformat{\section}{\bfseries\uppercase}{}{0pt}{}

\newenvironment{tightitemize}{\begin{itemize}[noitemsep, leftmargin=0pt]}{\end{itemize}}

\begin{document}

\begin{center}
{\LARGE \textbf{{ name }}}\\[4pt]
{\small email: {{ email }} \textbullet{} phone: {{ phone }} 
\textbullet{} GitHub: {{ github }} \textbullet{} LinkedIn: {{ linkedin }}}
\end{center}

\section*{Education}
\begin{itemize}
  {% for edu in education %}
  \item \textbf{{ edu.degree }}, {{ edu.school }} -- {{ edu.year }}
  {% endfor %}
\end{itemize}

\section*{Projects}
\begin{enumerate}
  {% for project in projects %}
  \item \textbf{{ project.name }} ({{ project.tech }})
  \begin{tightitemize}
    {% for bullet in project.bullets %}
    \item {{ bullet }}
    {% endfor %}
  \end{tightitemize}
  {% endfor %}
\end{enumerate}

\section*{Skills}
\begin{itemize}
  {% for category, skill_list in skills.items() %}
  \item \textbf{{ category }}: {{ skill_list|join(', ') }}
  {% endfor %}
\end{itemize}

\end{document}
"""

def generate_resume(personal_info: dict, education: list, projects: list, skills: dict, jd_info: dict) -> str:
    template = Template(LATEX_TEMPLATE)
    
    structured_skills = {}
    for category, skill_list in skills.items():
        structured_skills[category] = skill_list if isinstance(skill_list, list) else skill_list.split(',')
    
    latex_content = template.render(
        name=personal_info.get("name", "Your Name"),
        email=personal_info.get("email", "email@example.com"),
        phone=personal_info.get("phone", ""),
        github=personal_info.get("github", ""),
        linkedin=personal_info.get("linkedin", ""),
        education=education,
        projects=projects,
        skills=structured_skills
    )
    
    output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(output_dir, exist_ok=True)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as f:
        f.write(latex_content)
        tex_path = f.name
    
    pdf_filename = f"resume_{personal_info.get('name', 'output').replace(' ', '_')}.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)
    
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", output_dir, tex_path],
            capture_output=True,
            timeout=30
        )
        
        if result.returncode != 0:
            raise Exception(f"LaTeX error: {result.stderr.decode()}")
        
        os.rename(os.path.join(output_dir, os.path.basename(tex_path).replace('.tex', '.pdf')), pdf_path)
        
    finally:
        for ext in ['.tex', '.aux', '.log', '.out']:
            try:
                os.remove(tex_path.replace('.tex', ext))
            except:
                pass
    
    return pdf_path