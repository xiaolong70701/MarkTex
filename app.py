import streamlit as st
from utils.converter import generate_pdf

st.set_page_config(page_title="MarkTex", layout="centered")
st.title("📝 MarkTex: Markdown to LaTeX PDF")

md_input = st.text_area("請輸入 Markdown 內容", height=300)
mode = st.selectbox("輸出格式", ["文章 (Article)", "簡報 (Beamer)"])
filename = st.text_input("PDF 檔案名稱（不含副檔名）", value="output")

if st.button("📄 產出 PDF"):
    if not md_input.strip():
        st.warning("請先輸入內容")
    else:
        try:
            pdf_path, tex_path = generate_pdf(md_input, mode, filename=filename)
            with open(pdf_path, "rb") as f:
                st.download_button("📥 下載 PDF", f, file_name=f"{filename}.pdf", mime="application/pdf")
            with open(tex_path, "rb") as f:
                st.download_button("📄 下載 LaTeX", f, file_name=f"{filename}.tex", mime="application/x-tex")
        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
