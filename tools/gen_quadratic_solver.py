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
    <button onclick="calculate_{tool_id}()">Solve Equation</button>
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
    <h4>Recent Equations</h4>
    <ul id="history_list_{tool_id}"></ul>
    
    <div style="display:flex; gap:10px; margin-top:10px;">
        <button onclick="downloadHistory_{tool_id}()" class="btn-small" style="flex:1;">Save</button>
        <button onclick="clearHistory_{tool_id}()" class="btn-small" style="flex:1;">Clear</button>
    </div>
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
        if(historySummary) addToHistory_{tool_id}(historySummary);
    }}

    function addToHistory_{tool_id}(item) {{
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_{tool_id})) || [];
        if (history.length === 0 || history[0] !== item) {{
            history.unshift(item);
            if (history.length > 10) history.pop();
            localStorage.setItem(STORAGE_KEY_{tool_id}, JSON.stringify(history));
            renderHistory_{tool_id}();
        }}
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

    function downloadHistory_{tool_id}() {{
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_{tool_id})) || [];
        if (history.length === 0) {{
            alert("No history to download.");
            return;
        }}

        let content = "CalcFoundry - {title} History\\n";
        content += "Date: " + new Date().toLocaleDateString() + "\\n";
        content += "-----------------------------------\\n\\n";
        
        history.forEach(item => {{
            let cleanItem = item.replace(/<[^>]*>?/gm, '');
            content += cleanItem + "\\n";
        }});

        const blob = new Blob([content], {{ type: 'text/plain' }});
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "{title.replace(' ', '_')}_History.txt";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }}
</script>

<style>
  .calc-grid {{ display: grid; gap: 20px; grid-template-columns: 1fr; }}
  @media (min-width: 768px) {{ .calc-grid {{ grid-template-columns: 2fr 1fr; }} }}
  .calc-history {{ background: #252526; padding: 15px; border-radius: 8px; font-size: 0.9em; }}
  .calc-history h4 {{ margin-top: 0; border-bottom: 1px solid #444; padding-bottom: 5px; }}
  .calc-history ul {{ padding-left: 20px; color: #bbb; }}
  .btn-small {{ background: #444; font-size: 0.8em; padding: 8px 10px; margin-top: 0; color: white; border: 1px solid #555; cursor:pointer; border-radius: 4px; }}
  .btn-small:hover {{ background: #555; }}
  
  .calc-main label {{ display: block; margin-top: 10px; font-weight: bold; }}
  .calc-main input, .calc-main select {{ width: 100%; padding: 8px; margin-top: 5px; background: #333; border: 1px solid #555; color: white; }}
  .calc-main button {{ margin-top: 20px; width: 100%; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }}
  .calc-main button:hover {{ background: #0056b3; }}
  .row-inputs div {{ flex: 1; }}
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


# === DEFINING THE QUADRATIC SOLVER ===

quad_inputs = """
<div class="row-inputs">
    <div>
        <label>Coefficient a</label>
        <input type="number" id="coeff_a" placeholder="e.g. 1" value="1" step="any">
    </div>
    <div>
        <label>Coefficient b</label>
        <input type="number" id="coeff_b" placeholder="e.g. -5" value="-5" step="any">
    </div>
    <div>
        <label>Coefficient c</label>
        <input type="number" id="coeff_c" placeholder="e.g. 6" value="6" step="any">
    </div>
</div>
"""

quad_js = """
    let a = parseFloat(document.getElementById('coeff_a').value);
    let b = parseFloat(document.getElementById('coeff_b').value);
    let c = parseFloat(document.getElementById('coeff_c').value);

    if (isNaN(a)) a = 1;
    if (isNaN(b)) b = 0;
    if (isNaN(c)) c = 0;

    let resultText = "";
    let historySummary = "";

    if (a === 0) {
        if (b === 0) {
            resultText = "If a and b are both zero, the equation is not valid (no variable to solve).";
        } else {
            let x = -c / b;
            resultText = `
                <strong>Linear Equation Solver (since a = 0):</strong><br>
                Equation: ${b}x + ${c} = 0<br>
                <strong>Root:</strong> x = <span style="color:#4caf50; font-size:1.3em;">${x.toFixed(4)}</span>
            `;
            historySummary = `Linear: ${b}x+${c}=0 -> x=${x.toFixed(2)}`;
        }
    } else {
        let D = (b * b) - (4 * a * c);
        let h = -b / (2 * a);
        let k = (a * h * h) + (b * h) + c;
        let direction = (a > 0) ? "Opens Upward (Minimum)" : "Opens Downward (Maximum)";
        
        let rootText = "";
        
        if (D > 0) {
            let x1 = (-b + Math.sqrt(D)) / (2 * a);
            let x2 = (-b - Math.sqrt(D)) / (2 * a);
            rootText = `
                <strong>Two Real Roots:</strong><br>
                x₁ = <span style="color:#4caf50; font-size:1.2em; font-weight:bold;">${x1.toFixed(4)}</span><br>
                x₂ = <span style="color:#4caf50; font-size:1.2em; font-weight:bold;">${x2.toFixed(4)}</span>
            `;
            historySummary = `${a}x² + ${b}x + ${c} = 0: x={${x1.toFixed(2)}, ${x2.toFixed(2)}}`;
        } else if (D === 0) {
            let x = -b / (2 * a);
            rootText = `
                <strong>One Real Root (Repeated):</strong><br>
                x = <span style="color:#4caf50; font-size:1.2em; font-weight:bold;">${x.toFixed(4)}</span>
            `;
            historySummary = `${a}x² + ${b}x + ${c} = 0: x=${x.toFixed(2)}`;
        } else {
            let realPart = -b / (2 * a);
            let imagPart = Math.sqrt(-D) / (2 * a);
            rootText = `
                <strong>Two Complex Roots:</strong><br>
                x₁ = <span style="color:#ff9800; font-size:1.2em; font-weight:bold;">${realPart.toFixed(4)} + ${imagPart.toFixed(4)}i</span><br>
                x₂ = <span style="color:#ff9800; font-size:1.2em; font-weight:bold;">${realPart.toFixed(4)} - ${imagPart.toFixed(4)}i</span>
            `;
            historySummary = `${a}x² + ${b}x + ${c} = 0: Complex Roots`;
        }

        resultText = `
            ${rootText}
            <hr style="border-color:#444; opacity:0.3; margin: 10px 0;">
            <strong>Parabola Properties:</strong><br>
            Discriminant (D): <span style="font-weight:bold;">${D.toFixed(4)}</span><br>
            Vertex (h, k): <span style="color:#2196f3; font-weight:bold;">(${h.toFixed(4)}, ${k.toFixed(4)})</span><br>
            Direction: <span style="font-weight:bold;">${direction}</span>
        `;
    }
"""

quad_latex = r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}"

quad_content = """
### Understanding Quadratic Equations
A quadratic equation is a second-order polynomial equation in a single variable. The graph of a quadratic function is a **parabola**, a U-shaped curve that opens either upward or downward.

### Parabola Features
1. **The Discriminant ($D = b^2 - 4ac$):**
   - If $D > 0$: The parabola crosses the x-axis at two distinct points (two real roots).
   - If $D = 0$: The parabola touches the x-axis at exactly one point (one real repeated root).
   - If $D < 0$: The parabola does not touch the x-axis, and its roots are complex conjugate pairs.
2. **The Vertex ($h, k$):** The peak or trough of the parabola. It represents the maximum or minimum value of the quadratic function.
3. **Leading Coefficient ($a$):** Determines the width of the parabola and its direction. If $a$ is positive, it opens upward. If $a$ is negative, it opens downward.
"""

quad_vars = """
* $x$ is the **unknown variable** we are solving for.
* $a$ is the **quadratic coefficient** ($a \neq 0$).
* $b$ is the **linear coefficient**.
* $c$ is the **constant term**.
"""

# === GENERATE THE FILE ===
create_calculator(
    title="Quadratic Equation Solver", 
    category="Math", 
    description="Solve quadratic equations of the form ax² + bx + c = 0. Calculate real and complex roots, vertex coordinates, and plot key characteristics.",
    inputs_html=quad_inputs,
    calculation_js=quad_js,
    formula_latex=quad_latex,
    educational_content=quad_content,
    variable_definitions=quad_vars 
)
