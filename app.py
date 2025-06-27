import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from utils import guess_language, build_prompt, detect_and_fix_bugs

MODEL_PATH = r"saved_codellema"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, local_files_only=True)
model.to(device)

def analyze_code(code_snippet):
    language = guess_language(code_snippet)

    # Select proper prompt
    prompt = detect_and_fix_bugs(code_snippet) if language == "Python" else build_prompt(language, code_snippet)

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(device)
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=1024,
            temperature=0.2,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True).strip()

    # Normalize output for detection
    normalized_output = decoded_output.lower().strip()

    # 1. True "no error" check
    if "✅ no bugs found in the code." in normalized_output:
        if "errors:" not in normalized_output and "fixed code:" not in normalized_output:
            return "✅ No bugs found in the code."

    # 2. Check if model failed to follow format
    if "errors:" not in normalized_output or "fixed code:" not in normalized_output:
        return f"⚠ Format issue: Output from model incomplete.\n\nRaw Output:\n{decoded_output}"

    # 3. Return full structured response
    return decoded_output