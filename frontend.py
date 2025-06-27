import gradio as gr
import requests
from utils import guess_language

BACKEND_URL = "http://localhost:8000/analyze"

def process_uploaded_file(file_obj):
    try:
        content = file_obj.read().decode("utf-8")
        detected_lang = guess_language(content)
        return content, detected_lang if detected_lang in ["Python", "Java", "JavaScript"] else "Python"
    except Exception as e:
        return f"❌ Error reading file: {str(e)}", "Python"

def analyze_code_frontend(code_snippet, language):
    if not code_snippet.strip():
        return "❌ Please enter some code."

    try:
        response = requests.post(BACKEND_URL, json={
            "code_snippet": code_snippet,
            "language": language
        })
        if response.status_code == 200:
            return response.json().get("analysis", "✅ Code analyzed, but no output returned.")
        return f"❌ Backend error: {response.text}"
    except Exception as e:
        return f"❌ Could not connect to backend: {str(e)}"

with gr.Blocks(title="Bug Detection and Fixing") as demo:
    gr.Markdown("<h1 style='text-align:center;'>🔍 Bug Detection & Fixing</h1>")
    gr.Markdown("Paste your code, upload a file, and select a language to detect and fix bugs.")

    with gr.Row():
        lang_dropdown = gr.Dropdown(["Python", "Java", "JavaScript"], label="🧠 Select Language", value="Python")

    with gr.Row():
        file_upload = gr.File(label="📂 Upload Code File", file_types=[".py", ".java", ".js"])
        code_input = gr.Textbox(lines=15, label="📝 Code Snippet", placeholder="Paste your buggy code here...")

    file_upload.change(fn=process_uploaded_file, inputs=file_upload, outputs=[code_input, lang_dropdown])

    analyze_button = gr.Button("🚀 Analyze Code")
    result_output = gr.Code(label="🛠 Analysis & Fix", language="python")

    analyze_button.click(fn=analyze_code_frontend, inputs=[code_input, lang_dropdown], outputs=result_output)

    gr.Markdown("---")
    gr.Markdown("🧠 Powered by CodeLlama + FastAPI + Gradio")

    demo.launch()
frontend.py