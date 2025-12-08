import os

# --- CONFIGURATION ---
TOOLS_DIR = "content/posts"
# ---------------------

import os

# --- CONFIGURATION ---
TOOLS_DIR = "content/posts"
# ---------------------

def create_calculator(title, category, description, inputs_html, calculation_js, formula_latex, educational_content=""):
    safe_title = "".join(c for c in title if c.isalnum() or c == " ").lower().strip().replace(" ", "-")
    filename = f"{TOOLS_DIR}/{safe_title}.md"
    os.makedirs(TOOLS_DIR, exist_ok=True)
    
    tool_id = safe_title.replace("-", "_")
    
    content = f"""---
title: "{title}"
date: 2025-12-08
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
        <a href="#the-math-behind-it" style="color: #666; text-decoration: underline; cursor: pointer;">
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
    const STORAGE_KEY_{tool_id} = "omnicalc_history_{tool_id}";

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
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {filename}")


# --- CALCULATOR DEFINITION ---

wilson_inputs = """
<label>Total Trials (e.g., Visitors, Reviews)</label>
<input type="number" id="n_trials" placeholder="e.g. 100">

<label>Successes (e.g., Sales, 5-Star Ratings)</label>
<input type="number" id="n_success" placeholder="e.g. 95">

<label>Confidence Level</label>
<select id="conf_level">
    <option value="1.64485">90%</option>
    <option value="1.95996" selected>95% (Standard)</option>
    <option value="2.57583">99%</option>
</select>
"""

wilson_js = """
    // 1. Get Inputs
    let n = parseFloat(document.getElementById('n_trials').value);
    let x = parseFloat(document.getElementById('n_success').value);
    let z = parseFloat(document.getElementById('conf_level').value);

    // 2. Validation
    if (isNaN(n) || isNaN(x) || n <= 0) {
        var resultText = "Please enter valid positive numbers.";
    } else if (x > n) {
        var resultText = "Successes cannot be greater than Total Trials.";
    } else {
        // 3. Wilson Score Formula Logic
        // p_hat is the observed proportion
        let p = x / n;
        
        // Parts of the formula broken down for readability
        let p1 = p + ( (z*z) / (2*n) );
        let p2 = z * Math.sqrt( ( (p*(1-p))/n ) + ( (z*z)/(4*n*n) ) );
        let p3 = 1 + ( (z*z) / n );
        
        // Calculate Lower and Upper Bounds
        let lower = (p1 - p2) / p3;
        let upper = (p1 + p2) / p3;
        
        // Convert to Percentages
        let obs_perc = (p * 100).toFixed(2);
        let min_perc = (lower * 100).toFixed(2);
        let max_perc = (upper * 100).toFixed(2);
        
        // 4. Format Output
        // We use a clean summary string for the result text
        var resultText = `
            <strong>True Score Range:</strong> ${min_perc}% — ${max_perc}%<br>
            <small style='opacity:0.8'>Observed Rate: ${obs_perc}% (at 95% Confidence)</small>
        `;
    }
"""

wilson_latex = """w = \\frac{\\hat{p} + \\frac{z^2}{2n} \\pm z \\sqrt{\\frac{\\hat{p}(1-\\hat{p})}{n} + \\frac{z^2}{4n^2}}}{1 + \\frac{z^2}{n}}"""

wilson_content = """
### Why "Average Rating" is a Lie
Imagine two products:
1. **Product A:** Has one review, and it is 5 stars. (Average: 5.0)
2. **Product B:** Has 100 reviews, with 95 positive. (Average: 4.95)

Mathematically, Product A has a higher average. But intuitively, you trust Product B more. 
The **Wilson Score** solves this by asking: *"Given the data we have, what is the 'true' rating we can be 95% confident in?"*

For Product A, the Wilson Score might be **20%** (because one data point is unreliable).
For Product B, the score is likely **92%** (because the data is solid).

### Real World Use Cases
* **Amazon/eCommerce:** Ranking products by "Best Match" instead of "Highest Average".
* **Reddit:** How "Best" comments are sorted (upvotes vs downvotes).
* **Conversion Rate Optimization:** Determining if a landing page change actually worked.
"""

create_calculator(
    title="True Rating Calculator (Wilson Score)", 
    category="Statistics", 
    description="Calculate the true statistical accuracy of a rating or conversion rate using the Wilson Score Interval.",
    inputs_html=wilson_inputs,
    calculation_js=wilson_js,
    formula_latex=wilson_latex,
    educational_content=wilson_content  # <--- NEW FIELD
)