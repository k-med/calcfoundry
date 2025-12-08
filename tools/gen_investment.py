import os

# --- CONFIGURATION & PATH SETUP ---
# 1. Get the folder where THIS script is currently running (e.g., .../tools)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level to find the Project Root (e.g., .../my-hugo-site)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 3. Define the output directory based on the project root
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "content", "posts")

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
# ---------------------

def create_calculator(title, category, description, inputs_html, calculation_js, formula_latex, educational_content, variable_definitions):
    """
    Generates a Professional Hugo Calculator for CalcFoundry.
    """
    # Create a safe filename from the title
    safe_title = "".join(c for c in title if c.isalnum() or c == " ").lower().strip().replace(" ", "-")
    filename = os.path.join(OUTPUT_DIR, f"{safe_title}.md")
    
    # Create a unique ID for JS variables to prevent conflicts if multiple calcs are on one page
    tool_id = safe_title.replace("-", "_")
    
    # --- THE MARKDOWN TEMPLATE ---
    content = f"""---
title: "{title}"
date: 2025-12-09
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
            How is this calculated?
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
The tool uses the following mathematical principle:

$$
{formula_latex}
$$

**Where:**

{variable_definitions}
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {filename}")


# === DEFINING THE INVESTMENT CALCULATOR ===

compound_inputs = """
<label>Initial Principal ($)</label>
<input type="number" id="principal" placeholder="e.g. 5000">

<label>Monthly Contribution ($)</label>
<input type="number" id="monthly_contribution" placeholder="e.g. 500">

<label>Annual Interest Rate (%)</label>
<input type="number" id="interest_rate" placeholder="e.g. 7.5">

<label>Time Period (Years)</label>
<input type="number" id="years_grow" placeholder="e.g. 30">
"""

compound_js = """
    let P = parseFloat(document.getElementById('principal').value);
    let PMT = parseFloat(document.getElementById('monthly_contribution').value);
    let r_annual = parseFloat(document.getElementById('interest_rate').value);
    let t = parseFloat(document.getElementById('years_grow').value);

    // Sanitize inputs
    if (isNaN(P)) P = 0;
    if (isNaN(PMT)) PMT = 0;

    if (isNaN(r_annual) || isNaN(t) || t <= 0) {
        var resultText = "Please enter a valid interest rate and time period (years > 0).";
    } else {
        // Calculations
        let n = 12; // Monthly compounding frequency
        let r = r_annual / 100;
        let total_months = t * n;
        
        // Future Value of the Initial Principal
        let fv_principal = P * Math.pow((1 + r/n), total_months);
        
        // Future Value of the Series (Monthly Contributions)
        let fv_series = 0;
        if (PMT > 0 && r > 0) {
            fv_series = PMT * ( (Math.pow((1 + r/n), total_months) - 1) / (r/n) );
        } else if (PMT > 0 && r === 0) {
            fv_series = PMT * total_months;
        }

        let total_fv = fv_principal + fv_series;
        let total_contributed = P + (PMT * total_months);
        let total_interest = total_fv - total_contributed;

        // Formatting currency
        const fmt = (num) => {
            return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(num);
        };

        var resultText = `
            <strong>Final Balance:</strong> <span style="color:#4caf50; font-size:1.2em;">${fmt(total_fv)}</span><br>
            <hr style="border-color:#444; opacity:0.3; margin: 10px 0;">
            <small>Total Contributed: ${fmt(total_contributed)}</small><br>
            <small>Total Interest Earned: ${fmt(total_interest)}</small>
        `;
    }
"""

compound_latex = r"A = P \left(1 + \frac{r}{n}\right)^{nt} + PMT \times \frac{\left(1 + \frac{r}{n}\right)^{nt} - 1}{\frac{r}{n}}"

compound_content = """
### The Eighth Wonder of the World
Compound interest is often jokingly referred to as the "eighth wonder of the world" because of its ability to turn small, consistent efforts into massive results over time. Unlike **Simple Interest** (where you only earn money on your principal), **Compound Interest** means you earn interest on your interest.

### How it Works
1. **The Snowball Effect:** In the beginning, growth looks flat. This is the "accumulation phase."
2. **The Inflection Point:** Once your interest payments exceed your contributions, your wealth begins to grow vertically.
3. **Time is Key:** As you can see from the calculator, doubling your *time* usually does far more than doubling your *rate of return*.
"""

compound_vars = """
* $A$ is the **Future Value** (the final amount).
* $P$ is the **Initial Principal** (starting deposit).
* $PMT$ is the **Monthly Contribution**.
* $r$ is the **Annual Interest Rate** (decimal).
* $n$ is the **Compounding Frequency** (12 for monthly).
* $t$ is the **Time** in years.
"""

# === GENERATE THE FILE ===
create_calculator(
    title="Investment Growth Calculator", 
    category="Finance", 
    description="Visualize the power of compound interest with monthly contributions. See how small savings grow into massive wealth over time.",
    inputs_html=compound_inputs,
    calculation_js=compound_js,
    formula_latex=compound_latex,
    educational_content=compound_content,
    variable_definitions=compound_vars 
)