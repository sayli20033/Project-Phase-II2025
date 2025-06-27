import re

def guess_language(code_text):
    patterns = {
        "Python": r"(?m)^\s*def\s|\bimport\b|print\(|:\s*$",
        "Java": r"\bpublic\s+class\b|\bSystem\.out\.print",
        "JavaScript": r"\bfunction\b|\bvar\b|\bconst\b|\bconsole\.log"
    }
    for lang, pattern in patterns.items():
        if re.search(pattern, code_text):
            return lang
    return "Unknown"

def build_prompt(language, code_snippet):
    return f"""
### Language: {language}
### Buggy Code:
{code_snippet}

### Task:
You are a code analysis engine trained to find *multiple bugs* in code written in {language}.

- If the code is completely correct, respond exactly with:
  ✅ No bugs found in the code.

- Otherwise, do the following:
  1. List *all bugs*:
     - Line number
     - Error type (e.g., SyntaxError, NameError, LogicalError, RuntimeError)
     - Clear explanation
  2. Then, output the *entire corrected code*.

### Output Format:
✅ No bugs found in the code.

OR

Errors:
1. Line: <line number>
   Error Type: <type>
   Issue: <explanation>

2. Line: <line number>
   Error Type: <type>
   Issue: <explanation>

...

Fixed Code:
<corrected code here>
"""

def detect_and_fix_bugs(code_snippet):
    return f"""
### Language: Python
### Buggy Code:
{code_snippet}

### Task:
You are a Python expert. Carefully examine the code for *multiple types of bugs*.

- If the code is fully correct, respond exactly with:
  ✅ No bugs found in the code.

- Otherwise:
  1. Identify *every bug*, including:
     - Line number
     - Error type (choose from: SyntaxError, NameError, TypeError, IndentationError, ZeroDivisionError, ValueError, AttributeError, LogicalError, RuntimeError)
     - Explanation
  2. Then provide the *complete corrected version* of the code.

### Output Format:
✅ No bugs found in the code.

OR

Errors:
1. Line: <line number>
   Error Type: <type>
   Issue: <explanation>

2. Line: <line number>
   Error Type: <type>
   Issue: <explanation>

...

Fixed Code:
<corrected code here>
"""