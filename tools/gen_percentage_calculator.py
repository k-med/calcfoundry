import os
from datetime import datetime

# --- CONFIGURATION & PATH SETUP ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "content", "posts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_calculator(title, category, description, inputs_html, calculation_js, formula_latex, educational_content, variable_definitions):
    safe_title = "".join(c for c in title if c.isalnum() or c == " ").lower().strip().replace(" ", "-")
    filename = os.path.join(OUTPUT_DIR, f"{safe_title}.md")
    
    tool_id = safe_title.replace("-", "_")
    date_str = datetime.now().strftime("%Y-%m-%d")

    content = f"""---
title: "{title}"
date: {date_str}
categories: ["{category}"]
summary: "{description}"
math: true
disableSpecial1stPost: true
---

{description}

{{{{< calculator >}}}}

<div class="calc-grid">
  <div class="calc-main">
    {inputs_html}
    <button onclick="calculate_{tool_id}()">Calculate</button>
    <div id="result_box" class="result-box" style="display:none;">
        <span id="result_val"></span>
    </div>
    
    <div style="margin-top: 15px; text-align: center; font-size: 0.85em;">
        <a href="#the-math-behind-it" style="color: #888; text-decoration: underline; cursor: pointer;">
            How does this work?
        </a>
    </div>
  </div>

  <div class="calc-history">
    <h4>History</h4>
    <ul id="history_list_{tool_id}"></ul>
    <button onclick="clearHistory_{tool_id}()" class="btn-small">Clear History</button>
  </div>
</div>

<script>
    const STORAGE_KEY_{tool_id} = "calcfoundry_history_{tool_id}"; 

    window.onload = function() {{ 
        renderHistory_{tool_id}();
        updateLabels_{tool_id}(); 
    }};

    function updateLabels_{tool_id}() {{
        const mode = document.getElementById('calc_mode').value;
        const lblA = document.getElementById('label_a');
        const lblB = document.getElementById('label_b');
        
        if (mode === 'percent_of') {{
            lblA.innerText = "Percentage (%)";
            lblB.innerText = "Total Value";
        }} else if (mode === 'what_percent') {{
            lblA.innerText = "Part Value";
            lblB.innerText = "Total Value";
        }} else if (mode === 'percent_change') {{
            lblA.innerText = "Old Value";
            lblB.innerText = "New Value";
        }}
    }}

    function calculate_{tool_id}() {{
        {calculation_js}
        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        resBox.style.display = 'block';
        addToHistory_{tool_id}(historyText);
    }}

    function addToHistory_{tool_id}(item) {{
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_{tool_id})) || [];
        history.unshift(item);
        if (history.length > 10) history.pop();
        localStorage.setItem(STORAGE_KEY_{tool_id}, JSON.stringify(history));
        renderHistory_{tool_id}();
    }}

    function renderHistory_{tool_id}() {{
        const list = document.getElementById('history_list_{tool_id}');
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_{tool_id})) || [];
        list.innerHTML = history.map(item => `<li>${{item}}</li>`).join('');
    }}

    function clearHistory_{tool_id}() {{
        localStorage.removeItem(STORAGE_KEY_{tool_id});
        renderHistory_{tool_id}();
    }}
</script>

<style>
  .calc-grid {{ display: grid; gap: 20px; grid-template-columns: 1fr; }}
  @media (min-width: 768px) {{ .calc-grid {{ grid-template-columns: 2fr 1fr; }} }}
  .calc-history {{ background: #252526; padding: 15px; border-radius: 8px; font-size: 0.9em; }}
  .calc-history h4 {{ margin-top: 0; border-bottom: 1px solid #444; padding-bottom: 5px; }}
  .calc-history ul {{ padding-left: 20px; color: #bbb; }}
  .btn-small {{ background: #444; font-size: 0.8em; padding: 5px 10px; margin-top: 10px; }}
  .calc-main label {{ display: block; margin-top: 10px; font-weight: bold; }}
  .calc-main input, .calc-main select {{ width: 100%; padding: 8px; margin-top: 5px; background: #333; border: 1px solid #555; color: white; }}
  .calc-main button {{ margin-top: 20px; width: 100%; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }}
  .calc-main button:hover {{ background: #0056b3; }}
  .result-box {{ margin-top: 20px; padding: 15px; background: #2d2d2d; border-left: 4px solid #007bff; }}
</style>

{{{{< /calculator >}}}}

## How to Use
{educational_content}

## The Math Behind It
Depending on the mode you selected, the tool uses one of these three formulas:

$$
{formula_latex}
$$

**Where:**

{variable_definitions}
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {filename}")


# === DEFINING THE PERCENTAGE CALCULATOR ===

pct_inputs = """
<label>What do you want to calculate?</label>
<select id="calc_mode" onchange="updateLabels_universal_percentage_calculator()">
    <option value="percent_of">Percentage of a Number (e.g., 20% of 150)</option>
    <option value="what_percent">What % is X of Y? (e.g., 5 is what % of 20?)</option>
    <option value="percent_change">Percentage Increase/Decrease</option>
</select>

<label id="label_a">Percentage (%)</label>
<input type="number" id="input_a" placeholder="Enter first value">

<label id="label_b">Total Value</label>
<input type="number" id="input_b" placeholder="Enter second value">
"""

pct_js = """
    const mode = document.getElementById('calc_mode').value;
    const valA = parseFloat(document.getElementById('input_a').value);
    const valB = parseFloat(document.getElementById('input_b').value);

    let result = 0;
    let resultText = "";
    let historyText = "";

    if (isNaN(valA) || isNaN(valB)) {
        resultText = "Please enter valid numbers in both fields.";
        historyText = "Invalid Input";
    } else {
        if (mode === 'percent_of') {
            result = (valA / 100) * valB;
            resultText = `
                <strong>Result:</strong> <span style="color:#4caf50; font-size:1.4em;">${result.toLocaleString()}</span><br>
                <small>${valA}% of ${valB} is ${result}</small>
            `;
            historyText = `${valA}% of ${valB} = ${result}`;
        } 
        else if (mode === 'what_percent') {
            if (valB === 0) {
                resultText = "Cannot divide by zero.";
                historyText = "Error";
            } else {
                result = (valA / valB) * 100;
                resultText = `
                    <strong>Result:</strong> <span style="color:#4caf50; font-size:1.4em;">${result.toFixed(2)}%</span><br>
                    <small>${valA} is ${result.toFixed(2)}% of ${valB}</small>
                `;
                historyText = `${valA} is ${result.toFixed(2)}% of ${valB}`;
            }
        } 
        else if (mode === 'percent_change') {
            if (valA === 0) {
                resultText = "Starting value cannot be zero for change calculation.";
                historyText = "Error";
            } else {
                result = ((valB - valA) / valA) * 100;
                let direction = result > 0 ? "Increase" : "Decrease";
                let color = result > 0 ? "#4caf50" : "#ff5252"; 
                
                resultText = `
                    <strong>${direction}:</strong> <span style="color:${color}; font-size:1.4em;">${Math.abs(result).toFixed(2)}%</span><br>
                    <small>From ${valA} to ${valB}</small>
                `;
                historyText = `${valA} -> ${valB}: ${result.toFixed(2)}%`;
            }
        }
    }
"""

# FIX: Using FOUR backslashes to force a proper newline in Markdown/LaTeX
pct_latex = r"""
\begin{aligned}
\text{1. Percentage of:} & \quad P = \frac{\text{Percent}}{100} \times \text{Total} \\\\
\text{2. What \% is X of Y:} & \quad \% = \frac{\text{Part}}{\text{Total}} \times 100 \\\\
\text{3. Percent Change:} & \quad \Delta\% = \frac{\text{New} - \text{Old}}{\text{Old}} \times 100
\end{aligned}
"""

# FIX: Escaping the '$' signs so Hugo doesn't treat them as math delimiters
pct_content = """
### Why this matters
Percentages are the universal language of comparison. Whether you are calculating a discount at a store, analyzing stock market returns, or grading a test, understanding how to manipulate these numbers is essential.

### The Three Modes explained
1. **Percentage of a Number:** Use this to find a portion. *Example: "What is 20% of my \$50 bill?"*
2. **What % is X of Y:** Use this to find the rate. *Example: "I got 45 questions right out of 50. What is my grade?"*
3. **Percentage Change:** Use this to compare growth or loss. *Example: "My rent went from \$1,000 to \$1,100. How much did it go up?"*
"""

pct_vars = """
* $P$ is the **Part** (the result).
* $\Delta\%$ is the **Change** in percentage.
* Values are standard decimal or integer inputs.
"""

# === GENERATE THE FILE ===
create_calculator(
    title="Universal Percentage Calculator", 
    category="Math", 
    description="The only percentage tool you need. Calculate percentage increases, find parts of a whole, and solve 'X is what percent of Y' problems instantly.",
    inputs_html=pct_inputs,
    calculation_js=pct_js,
    formula_latex=pct_latex,
    educational_content=pct_content,
    variable_definitions=pct_vars 
)