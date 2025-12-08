import os
from datetime import datetime

# --- CONFIGURATION & PATH SETUP ---
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
    <button onclick="calculate_{tool_id}()">Calculate True Inflation</button>
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
    <h4>Recent Checks</h4>
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
        addToHistory_{tool_id}(historyText);
    }}

    function addToHistory_{tool_id}(item) {{
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_{tool_id})) || [];
        history.unshift(item);
        if (history.length > 5) history.pop();
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
  .input-row {{ display: flex; gap: 10px; }}
  .input-row div {{ flex: 1; }}
</style>

{{{{< /calculator >}}}}

## How to Use
{educational_content}

## The Math Behind It
This calculator uses the Compound Annual Growth Rate (CAGR) formula to find the implicit inflation rate required to get from your starting price to your ending price:

$$
{formula_latex}
$$

**Where:**

{variable_definitions}
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {filename}")


# === DEFINING THE SHADOW INFLATION CALCULATOR ===

shadow_inputs = """
<div class="input-row">
    <div>
        <label>Start Year</label>
        <input type="number" id="start_year" placeholder="e.g. 1940" value="1940">
    </div>
    <div>
        <label>Start Price ($)</label>
        <input type="number" id="start_price" placeholder="e.g. 50" value="50">
    </div>
</div>

<div class="input-row">
    <div>
        <label>End Year</label>
        <input type="number" id="end_year" placeholder="e.g. 2025" value="2025">
    </div>
    <div>
        <label>End Price ($)</label>
        <input type="number" id="end_price" placeholder="e.g. 700" value="700">
    </div>
</div>

<small style="color:#aaa; display:block; margin-top:10px;">
    <em>Tip: Enter what an item cost back then vs. what it costs <strong>you</strong> today to see your personal inflation rate.</em>
</small>
"""

shadow_js = """
    let y1 = parseFloat(document.getElementById('start_year').value);
    let p1 = parseFloat(document.getElementById('start_price').value);
    let y2 = parseFloat(document.getElementById('end_year').value);
    let p2 = parseFloat(document.getElementById('end_price').value);
    
    let resultText = "";
    let historyText = "";

    if (isNaN(y1) || isNaN(p1) || isNaN(y2) || isNaN(p2)) {
        resultText = "Please enter valid years and prices.";
        historyText = "Error";
    } else if (y2 <= y1) {
        resultText = "End Year must be after Start Year.";
        historyText = "Error";
    } else if (p1 <= 0 || p2 <= 0) {
        resultText = "Prices must be greater than zero.";
        historyText = "Error";
    } else {
        // Calculate Time Span
        let n = y2 - y1;
        
        // Calculate Total Change
        let total_growth = ((p2 - p1) / p1) * 100;
        
        // Calculate CAGR (Implicit Annual Inflation)
        // Formula: (End/Start)^(1/n) - 1
        let ratio = p2 / p1;
        let cagr = (Math.pow(ratio, (1/n)) - 1) * 100;
        
        // Determine Color based on severity (Official target is usually ~2-3%)
        let color = "#4caf50"; // Green (Low)
        if (cagr > 3) color = "#ff9800"; // Orange (Moderate)
        if (cagr > 6) color = "#f44336"; // Red (High/Shadow Levels)

        resultText = `
            <strong>Average Annual Inflation:</strong> <span style="color:${color}; font-size:1.6em;">${cagr.toFixed(2)}%</span><br>
            <hr style="border-color:#444; opacity:0.3; margin: 10px 0;">
            <small>Total Price Increase: ${total_growth.toLocaleString(undefined, {maximumFractionDigits: 0})}%</small><br>
            <small>Time Span: ${n} Years</small>
        `;
        
        historyText = `${y1} ($${p1}) \u2192 ${y2} ($${p2}) = ${cagr.toFixed(2)}%`;
    }
"""

shadow_latex = r"i = \left( \frac{P_{end}}{P_{start}} \right)^{\frac{1}{n}} - 1"

shadow_content = """
### Why Your "Personal Inflation" May Feel Higher
You might notice that the official Consumer Price Index (CPI) reports inflation at 3%, but your grocery bill feels like it went up 10%. This discrepancy often comes down to methodology. 

### The "Shadow" Perspective
Economists like those at **ShadowStats** argue that changes to how inflation is calculated (starting in the 1980s and 1990s) have artificially lowered the official numbers. Two major changes are often cited:

1.  **Substitution Bias:** Old models used a "Fixed Basket" (if you bought steak in 1980, they tracked the price of steak in 1990). Modern models assume if steak gets expensive, you switch to chicken. This lowers the reported "cost of living" but ignores the drop in your standard of living.
2.  **Hedonics:** If a new car costs more but has better features (airbags, GPS), the government might say the "price" didn't actually rise because you are getting "more car." However, to your bank account, the cash leaving is still higher.

### How to use this tool
Use this calculator to bypass official statistics and check the **actual** inflation rate of goods you buy. 
* **Example:** If a house cost \$10,000 in 1960 and costs \$500,000 today, input those numbers to find the *true* annual inflation rate for housing, regardless of what the CPI says.
"""

shadow_vars = """
* $i$ is the **Average Annual Inflation Rate**.
* $P_{end}$ is the **Price in the Future Year**.
* $P_{start}$ is the **Price in the Past Year**.
* $n$ is the **Number of Years** between the two dates.
"""

# === GENERATE THE FILE ===
create_calculator(
    title="True Inflation Calculator", 
    category="Economics", 
    description="Calculate the real inflation rate based on actual price changes. Compare official CPI numbers against the reality of your wallet.",
    inputs_html=shadow_inputs,
    calculation_js=shadow_js,
    formula_latex=shadow_latex,
    educational_content=shadow_content,
    variable_definitions=shadow_vars 
)