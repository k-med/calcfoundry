import os
from datetime import datetime

# --- CONFIGURATION & PATH SETUP ---
# Replicating the setup from your provided gen_investment.py
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "content", "posts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_calculator(title, category, description, inputs_html, calculation_js, formula_latex, educational_content, variable_definitions):
    # 1. Create a safe filename
    safe_title = "".join(c for c in title if c.isalnum() or c == " ").lower().strip().replace(" ", "-")
    filename = os.path.join(OUTPUT_DIR, f"{safe_title}.md")
    
    # Create unique ID for JS
    tool_id = safe_title.replace("-", "_")
    
    # 2. Date string
    date_str = datetime.now().strftime("%Y-%m-%d")

    # 3. Markdown Content Construction
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
    <button onclick="calculate_{tool_id}()">Calculate Sample Size</button>
    <div id="result_box" class="result-box" style="display:none;">
        <span id="result_val"></span>
    </div>
    
    <div style="margin-top: 15px; text-align: center; font-size: 0.85em;">
        <a href="#the-math-behind-it" style="color: #888; text-decoration: underline; cursor: pointer;">
            See the Formula
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

    window.onload = function() {{ renderHistory_{tool_id}(); }};

    function calculate_{tool_id}() {{
        {calculation_js}
        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        resBox.style.display = 'block';
        addToHistory_{tool_id}(resultText);
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

## How to Use This Calculator
{educational_content}

## The Math Behind It
The tool uses Cochran's Sample Size Formula with a Finite Population Correction:

$$
{formula_latex}
$$

**Where:**

{variable_definitions}
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {filename}")


# === DEFINING THE SAMPLE SIZE CALCULATOR ===

sample_inputs = """
<label>Confidence Level</label>
<select id="confidence_level">
    <option value="1.645">90% (Low Risk)</option>
    <option value="1.96" selected>95% (Standard)</option>
    <option value="2.576">99% (High Precision)</option>
</select>

<label>Margin of Error (%)</label>
<input type="number" id="margin_error" placeholder="e.g. 5" value="5">

<label>Population Size (Optional)</label>
<input type="number" id="population_size" placeholder="Leave blank for infinite">

<label>Estimated Proportion (%)</label>
<input type="number" id="proportion" placeholder="e.g. 50" value="50">
<small style="color:#888;">Use 50% if unsure (this gives the maximum sample size).</small>
"""

sample_js = """
    // Inputs
    let Z = parseFloat(document.getElementById('confidence_level').value);
    let e_percent = parseFloat(document.getElementById('margin_error').value);
    let pop = parseFloat(document.getElementById('population_size').value);
    let p_percent = parseFloat(document.getElementById('proportion').value);

    // Sanitize
    if (isNaN(e_percent) || e_percent <= 0) e_percent = 5; 
    if (isNaN(p_percent)) p_percent = 50;
    
    let e = e_percent / 100;
    let p = p_percent / 100;

    // 1. Calculate Standard Sample Size (Infinite Population)
    // Formula: (Z^2 * p * (1-p)) / e^2
    let numerator = Math.pow(Z, 2) * p * (1 - p);
    let denominator = Math.pow(e, 2);
    let n = numerator / denominator;

    // 2. Apply Finite Population Correction (if population is provided)
    // Formula: n_adj = n / (1 + ((n - 1) / Population))
    let isFinite = false;
    if (!isNaN(pop) && pop > 0) {
        n = n / (1 + ((n - 1) / pop));
        isFinite = true;
    }

    // Always round up for people
    let final_n = Math.ceil(n);

    // Output Generation
    let popText = isFinite ? `Population: ${pop.toLocaleString()}` : "Infinite Population";
    
    var resultText = `
        <strong>Required Sample Size:</strong> <span style="color:#4caf50; font-size:1.4em;">${final_n}</span><br>
        <hr style="border-color:#444; opacity:0.3; margin: 10px 0;">
        <small>${popText} @ ${document.getElementById('confidence_level').options[document.getElementById('confidence_level').selectedIndex].text}</small><br>
        <small>Margin of Error: ±${e_percent}%</small>
    `;
"""

sample_latex = r"n = \frac{\frac{Z^2 \cdot p(1-p)}{e^2}}{1 + \frac{\frac{Z^2 \cdot p(1-p)}{e^2} - 1}{N}}"

sample_content = """
### Understanding the Results
In statistics, the "Sample Size" is the number of individual responses you need to collect to ensure that your survey results accurately represent the overall population within your chosen margin of error.


### Key Concepts:
* **Confidence Level:** How sure you want to be that the actual data falls within your margin of error. 95% is the industry standard.
* **Margin of Error:** The wiggle room you allow. If your survey says 60% of people like pizza with a 5% margin of error, the "true" number is between 55% and 65%.
* **Population:** If you are surveying a specific small group (e.g., "Employees at my company of 500 people"), input that number. If you are surveying "US Consumers," leave it blank (infinite).
"""

sample_vars = """
* $n$ is the **Sample Size** needed.
* $N$ is the **Population Size**.
* $Z$ is the **Z-score** (1.96 for 95% confidence).
* $p$ is the **Estimated Proportion** (0.5 yields the most conservative sample).
* $e$ is the **Margin of Error** (decimal format).
"""

# === GENERATE THE FILE ===
create_calculator(
    title="Survey Sample Size Calculator", 
    category="Statistics", 
    description="Calculate exactly how many survey responses you need for statistically significant results. Supports finite population correction.",
    inputs_html=sample_inputs,
    calculation_js=sample_js,
    formula_latex=sample_latex,
    educational_content=sample_content,
    variable_definitions=sample_vars 
)