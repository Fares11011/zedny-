import streamlit as st
import base64

def render_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    return html_content

def main():
    st.set_page_config(page_title="Leadership Assessment", layout="wide")
    st.sidebar.title("التقييم القيادي المتقدم")
    page = st.sidebar.radio("اختر الصفحة:", ["الاختبار", "المتطلبات", "النتائج"])

    if page == "الاختبار":
        html_content = render_html_file("Assessment.html")
    elif page == "المتطلبات":
        html_content = render_html_file("req.html")
    elif page == "النتائج":
        html_content = render_html_file("answers.html")

    st.components.v1.html(html_content, scrolling=True, height=800)

if __name__ == "__main__":
    main()
