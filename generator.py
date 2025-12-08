import os
import textwrap

# --- CONFIGURATION ---
TOOLS_DIR = "content/posts"
# ---------------------

def create_calculator(title, category, description, html_logic, formula_latex):
    """
    Generates a Hugo Markdown file for a new calculator.
    """
    # Create filename from title (e.g., "Mortgage Calculator" -> "mortgage-calculator.md")
    safe_title = "".join(c for c in title if c.isalnum() or c == " ").lower().strip().replace(" ", "-")
    filename = f"{TOOLS_DIR}/{safe_title}.md"
    
    # Ensure directory exists
    os.makedirs(TOOLS_DIR, exist_ok=True)
    
    # The Markdown Content
    content = f"""---
title: "{title}"
date: 2025-12-08
categories: ["{category}"]
summary: "{description}"
---

{description}

{{{{< calculator >}}}}

{html_logic}

{{{{< /calculator >}}}}

### How it Works
This tool uses the following mathematical principle:
$$
{formula_latex}
$$
"""
    
    # Write to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Success: Created {filename}")

# --- EXAMPLE USAGE (You will replace this with AI loop later) ---

# Example 1: ROI Calculator
roi_html = """
<label>Total Investment ($)</label>
<input type="number" id="inv" value="5000">
<label>Returned Amount ($)</label>
<input type="number" id="ret" value="6500">
<button onclick="calcROI()">Calculate ROI</button>
<div id="roi_res" class="result-box">Result...</div>

<script>
function calcROI() {
    let i = parseFloat(document.getElementById('inv').value);
    let r = parseFloat(document.getElementById('ret').value);
    let res = ((r - i) / i) * 100;
    document.getElementById('roi_res').innerHTML = `<strong>ROI:</strong> ${res.toFixed(2)}%`;
}
</script>
"""

create_calculator(
    title="Return on Investment Calculator", 
    category="Business", 
    description="Instantly calculate the percentage return on any investment.",
    html_logic=roi_html,
    formula_latex="ROI = \\frac{Current Value - Cost of Investment}{Cost of Investment} \\times 100"
)

# Example 2: BMI Calculator
bmi_html = """
<label>Weight (kg)</label>
<input type="number" id="w" value="70">
<label>Height (cm)</label>
<input type="number" id="h" value="175">
<button onclick="calcBMI()">Check BMI</button>
<div id="bmi_res" class="result-box">Result...</div>

<script>
function calcBMI() {
    let w = parseFloat(document.getElementById('w').value);
    let h = parseFloat(document.getElementById('h').value) / 100; // convert to m
    let bmi = w / (h * h);
    document.getElementById('bmi_res').innerHTML = `<strong>Your BMI:</strong> ${bmi.toFixed(1)}`;
}
</script>
"""

create_calculator(
    title="BMI Body Mass Index", 
    category="Health", 
    description="Check if you are in a healthy weight range based on height and weight.",
    html_logic=bmi_html,
    formula_latex="BMI = \\frac{kg}{m^2}"
)