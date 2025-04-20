import os
import subprocess
from jinja2 import Template

TEMPLATES = {
    "文章 (Article)": "templates/article_template.tex",
    "簡報 (Beamer)": "templates/beamer_template.tex"
}

def markdown_to_latex(md_content: str) -> str:
    result = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "latex"],
        input=md_content,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        print("❌ Pandoc 錯誤訊息：", result.stderr)
        raise RuntimeError("Pandoc 轉換 Markdown → LaTeX 失敗")
    return result.stdout

def generate_pdf(markdown_text: str, mode: str, filename: str = "output"):
    os.makedirs("output", exist_ok=True)

    with open(TEMPLATES[mode], "r", encoding="utf-8") as f:
        template = Template(f.read())

    latex_content = markdown_to_latex(markdown_text)

    rendered = template.render(
        title="MarkTex 自動產出",
        author="Anonymous",
        date="\today",
        content=latex_content
    )

    tex_path = f"output/{filename}.tex"
    pdf_path = f"output/{filename}.pdf"

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    result = subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "-output-directory=output", tex_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print("❌ XeLaTeX 編譯錯誤：")
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("LaTeX 編譯失敗，請檢查模板與內容")

    return pdf_path, tex_path
