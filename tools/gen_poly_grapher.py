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

    # Inject tool_id into JS
    calculation_js = calculation_js.replace("{tool_id}", tool_id)

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
    
    <div id="loading_status_{tool_id}" style="display:none; color: #888; font-size: 0.8em; margin-bottom: 5px;">Loading Graph Engine...</div>

    <div id="polys_container_{tool_id}" class="lines-container">
        </div>
    
    <div class="button-row">
        <button onclick="addPoly_{tool_id}()" class="btn-secondary">+ Add Function</button>
        <button onclick="calculate_{tool_id}()" class="btn-primary">Plot & Analyze</button>
    </div>

    <div id="graph_{tool_id}" class="graph-box"></div>

    <div id="result_box" class="result-box" style="display:none;">
        <span id="result_val"></span>
    </div>
    
    <div style="margin-top: 15px; text-align: center; font-size: 0.85em;">
        <a href="#the-math-behind-it" style="color: #888; text-decoration: underline; cursor: pointer;">
            Understanding Polynomial Degrees
        </a>
    </div>
  </div>

  <div class="calc-history">
    <h4>Function Properties</h4>
    <ul id="history_list_{tool_id}"></ul>
    <button onclick="clearHistory_{tool_id}()" class="btn-small">Clear Log</button>
  </div>
</div>

<script>
    const STORAGE_KEY_{tool_id} = "calcfoundry_poly_{tool_id}"; 
    let polyCount_{tool_id} = 0;

    // --- ROBUST SCRIPT LOADER ---
    function loadPlotlyAndInit_{tool_id}() {{
        if (typeof Plotly !== 'undefined') {{
            initCalculator_{tool_id}();
        }} else {{
            const status = document.getElementById('loading_status_{tool_id}');
            if(status) status.style.display = 'block';

            const script = document.createElement('script');
            script.src = "https://cdn.plot.ly/plotly-2.24.1.min.js";
            script.onload = function() {{
                if(status) status.style.display = 'none';
                initCalculator_{tool_id}();
            }};
            script.onerror = function() {{
                if(status) status.innerHTML = "Error: Could not load graphing library.";
            }};
            document.head.appendChild(script);
        }}
    }}

    // Entry point
    window.addEventListener('load', loadPlotlyAndInit_{tool_id});

    function initCalculator_{tool_id}() {{
        // Initialize with one Quadratic by default
        addPoly_{tool_id}(2); 
        renderHistory_{tool_id}();
        
        // Pre-fill inputs for a nice parabola
        setTimeout(() => {{
            const inputs = document.querySelectorAll('#polys_container_{tool_id} input');
            if(inputs.length >= 3) {{
                inputs[0].value = 1;   // x^2
                inputs[1].value = -2;  // x
                inputs[2].value = -3;  // c
                calculate_{tool_id}(); 
            }}
        }}, 200);
    }}

    function addPoly_{tool_id}(defaultDegree = 2) {{
        const container = document.getElementById('polys_container_{tool_id}');
        const id = polyCount_{tool_id}++;
        
        const div = document.createElement('div');
        div.className = 'line-input-row';
        div.id = 'poly_row_' + id;
        
        // STRUCTURE: Header (Select + Delete) -> Inputs (Flex Wrap)
        div.innerHTML = `
            <div class="row-header">
                <select id="degree_select_${{id}}" class="degree-select" onchange="updateInputs_{tool_id}(${{id}})">
                    <option value="1">Degree 1 (Linear)</option>
                    <option value="2" selected>Degree 2 (Quadratic)</option>
                    <option value="3">Degree 3 (Cubic)</option>
                    <option value="4">Degree 4 (Quartic)</option>
                </select>
                <button onclick="removePoly_{tool_id}(${{id}})" class="btn-remove" title="Remove">×</button>
            </div>
            
            <div id="inputs_area_${{id}}" class="eq-group">
                </div>
        `;
        container.appendChild(div);
        
        if(defaultDegree) document.getElementById(`degree_select_${{id}}`).value = defaultDegree;
        updateInputs_{tool_id}(id);
    }}

    function updateInputs_{tool_id}(id) {{
        const degree = parseInt(document.getElementById(`degree_select_${{id}}`).value);
        const area = document.getElementById(`inputs_area_${{id}}`);
        let html = '<div class="term-wrapper"><span class="eq-label">y =</span></div>';
        
        for(let i=degree; i>=0; i--) {{
            html += '<div class="term-wrapper">';
            
            // Operator (except for the very first term after y=)
            if(i < degree) html += '<span class="eq-operator">+</span>';
            
            // Input Box
            html += `<input type="number" class="eq-input" data-power="${{i}}" placeholder="0" step="any">`;
            
            // Variable Label (x^2, x, etc)
            if(i > 1) html += `<span class="eq-var">x<sup>${{i}}</sup></span>`;
            else if (i === 1) html += `<span class="eq-var">x</span>`;
            
            html += '</div>';
        }}
        
        area.innerHTML = html;
    }}

    function removePoly_{tool_id}(id) {{
        const row = document.getElementById('poly_row_' + id);
        if(row) row.remove();
        calculate_{tool_id}(); 
    }}

    function calculate_{tool_id}() {{
        {calculation_js}
        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        if(resultText) resBox.style.display = 'block';
        
        if (historyText) addToHistory_{tool_id}(historyText);
    }}

    function addToHistory_{tool_id}(item) {{
        if(!item.includes("Vertex")) return;
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_{tool_id})) || [];
        if (history.length === 0 || history[0] !== item) {{
            history.unshift(item);
            if (history.length > 5) history.pop();
            localStorage.setItem(STORAGE_KEY_{tool_id}, JSON.stringify(history));
            renderHistory_{tool_id}();
        }}
    }}

    function renderHistory_{tool_id}() {{
        const list = document.getElementById('history_list_{tool_id}');
        if(!list) return;
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_{tool_id})) || [];
        list.innerHTML = history.map(item => `<li>${{item}}</li>`).join('');
    }}

    function clearHistory_{tool_id}() {{
        localStorage.removeItem(STORAGE_KEY_{tool_id});
        renderHistory_{tool_id}();
    }}
</script>

<style>
  /* MAIN LAYOUT */
  .calc-grid {{ display: grid; gap: 20px; grid-template-columns: 1fr; }}
  @media (min-width: 900px) {{ .calc-grid {{ grid-template-columns: 2fr 1fr; }} }}
  
  .calc-main {{ background: #1e1e1e; padding: 20px; border-radius: 8px; border: 1px solid #333; }}
  
  /* INPUT ROWS */
  .lines-container {{ 
      display: flex; 
      flex-direction: column; 
      gap: 15px; 
      margin-bottom: 20px;
  }}
  
  .line-input-row {{ 
      background: #2d2d2d; 
      padding: 10px; 
      border-radius: 6px; 
      border-left: 4px solid #9c27b0; 
  }}

  /* HEADER (Degree Select + Delete) */
  .row-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #444;
      padding-bottom: 8px;
      margin-bottom: 10px;
  }}
  
  .degree-select {{
      background: #333; color: #ddd; border: 1px solid #555; 
      padding: 4px 8px; border-radius: 4px; font-size: 0.9em;
      cursor: pointer;
  }}

  /* EQUATION FLOW - The Horizontal Fix */
  .eq-group {{ 
      display: flex; 
      flex-wrap: wrap; /* THIS IS KEY: Allows wrapping */
      align-items: center; 
      gap: 5px; 
      padding-top: 5px;
  }}

  /* Grouping Input + Variable together */
  .term-wrapper {{
      display: flex;
      align-items: center;
      white-space: nowrap;
      margin-bottom: 5px; /* Spacing between wrapped lines */
  }}

  /* TEXT ELEMENTS */
  .eq-label {{ font-weight: bold; color: #9c27b0; font-family: monospace; font-size: 1.2em; margin-right: 8px; }}
  .eq-operator {{ font-weight: bold; color: #888; margin: 0 6px; }}
  .eq-var {{ font-family: 'Times New Roman', serif; font-style: italic; color: #ddd; font-size: 1.1em; margin-left: 4px; }}
  
  /* COMPACT INPUT FIELDS */
  .eq-input {{ 
      width: 60px; /* Nice and compact */
      padding: 6px; 
      background: #111; 
      border: 1px solid #444; 
      color: white; 
      border-radius: 4px; 
      text-align: center;
      font-size: 0.95em;
  }}
  .eq-input:focus {{ border-color: #9c27b0; outline: none; background: #000; }}

  /* BUTTONS */
  .button-row {{ display: flex; gap: 10px; margin-bottom: 20px; }}
  
  .btn-primary {{ flex: 2; padding: 12px; background: #9c27b0; color: white; border: none; cursor: pointer; border-radius: 4px; font-weight: bold; transition: background 0.2s; }}
  .btn-primary:hover {{ background: #7b1fa2; }}
  
  .btn-secondary {{ flex: 1; padding: 12px; background: #444; color: white; border: none; cursor: pointer; border-radius: 4px; transition: background 0.2s; }}
  .btn-secondary:hover {{ background: #555; }}

  /* FIXED SQUARE DELETE BUTTON */
  .btn-remove {{ 
      flex: 0 0 30px; /* Don't grow, don't shrink, 30px basis */
      height: 30px; 
      background: #dc3545; 
      color: white; 
      border: none; 
      border-radius: 4px; 
      cursor: pointer; 
      display: flex; 
      align-items: center; 
      justify-content: center;
      font-weight: bold; 
      font-size: 1.2em; 
      padding: 0; /* Remove padding to keep it square */
  }}
  .btn-remove:hover {{ background: #a71d2a; }}

  /* GRAPH CONTAINER */
  .graph-box {{ 
      width: 100%; 
      height: 450px; 
      background: #111; 
      border: 1px solid #444; 
      border-radius: 4px;
  }}
  
  .result-box {{ margin-top: 20px; padding: 15px; background: #2d2d2d; border-left: 4px solid #28a745; }}
  
  /* HISTORY */
  .calc-history {{ background: #252526; padding: 15px; border-radius: 8px; font-size: 0.9em; height: fit-content; }}
  .calc-history h4 {{ margin-top: 0; border-bottom: 1px solid #444; padding-bottom: 5px; color: #ddd; }}
  .calc-history ul {{ padding-left: 20px; color: #bbb; margin: 0; }}
  .calc-history li {{ margin-bottom: 8px; line-height: 1.4; }}
  .btn-small {{ background: #444; font-size: 0.8em; padding: 5px 10px; margin-top: 15px; border:none; color:white; cursor:pointer; width: 100%; border-radius: 4px; }}
</style>

{{{{< /calculator >}}}}

## How to Use
{educational_content}

## The Math Behind It
Standard Polynomial Form:

$$
{formula_latex}
$$

**Where:**
{variable_definitions}
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {filename}")


# === DEFINING THE POLY GRAPHER LOGIC ===

graph_inputs = "" # Handled dynamically

graph_js = """
    const containerId = 'polys_container_{tool_id}';
    const graphId = 'graph_{tool_id}';

    // 1. Gather all polynomials
    let polynomials = [];
    const container = document.getElementById(containerId);
    if(!container) return; 
    
    const rows = container.getElementsByClassName('line-input-row');
    
    for (let row of rows) {
        let inputs = row.getElementsByClassName('eq-input');
        let coeffs = {}; // Map power -> value
        let maxDegree = 0;
        let valid = false;

        for(let input of inputs) {
            let power = parseInt(input.getAttribute('data-power'));
            let val = parseFloat(input.value);
            
            if(!isNaN(val)) {
                coeffs[power] = val;
                if(val !== 0 && power > maxDegree) maxDegree = power;
                valid = true;
            } else {
                coeffs[power] = 0; // Treat empty as 0
            }
        }

        if(valid) {
            polynomials.push({coeffs: coeffs, degree: maxDegree});
        }
    }

    if(polynomials.length === 0) {
        document.getElementById('result_val').innerHTML = "Please enter coefficients to plot.";
        return;
    }

    // 2. Generate Plot Data
    let minX = -10, maxX = 10;
    
    // Auto-center logic for Quadratics
    polynomials.forEach(p => {
        if(p.degree === 2) {
            let a = p.coeffs[2];
            let b = p.coeffs[1];
            if(a !== 0) {
                let h = -b / (2*a);
                if(h < minX) minX = h - 5;
                if(h > maxX) maxX = h + 5;
            }
        }
    });

    let plotData = [];
    let step = (maxX - minX) / 200; 

    polynomials.forEach((poly, index) => {
        let xVals = [];
        let yVals = [];
        
        for(let x = minX; x <= maxX; x += step) {
            let y = 0;
            for(let pow in poly.coeffs) {
                y += poly.coeffs[pow] * Math.pow(x, pow);
            }
            xVals.push(x);
            yVals.push(y);
        }
        
        // Name generation
        let name = "";
        let powers = Object.keys(poly.coeffs).sort((a,b) => b-a);
        powers.forEach((pow, i) => {
            let val = poly.coeffs[pow];
            if(val === 0 && powers.length > 1) return; 
            
            let sign = (val >= 0 && i > 0) ? " + " : " ";
            if(val < 0) sign = " - ";
            
            let absVal = Math.abs(val);
            let valStr = (absVal === 1 && pow > 0) ? "" : absVal;
            
            let term = "";
            if(pow == 0) term = `${valStr}`;
            else if(pow == 1) term = `${valStr}x`;
            else term = `${valStr}x^${pow}`;
            
            name += sign + term;
        });

        plotData.push({
            x: xVals,
            y: yVals,
            mode: 'lines',
            name: name.trim() || "y=0",
            line: { width: 3 }
        });
    });

    // 3. Analysis (Quadratic focus)
    let analysisHTML = "";
    let historyText = "";

    polynomials.forEach((p, i) => {
        if(p.degree === 2) {
            let a = p.coeffs[2];
            let b = p.coeffs[1];
            let c = p.coeffs[0];
            
            let h = -b / (2*a);
            let k = (a*h*h) + (b*h) + c;
            
            let D = (b*b) - (4*a*c);
            let roots = "";
            
            if(D > 0) {
                let r1 = (-b + Math.sqrt(D)) / (2*a);
                let r2 = (-b - Math.sqrt(D)) / (2*a);
                roots = `Roots at x = ${r1.toFixed(2)}, ${r2.toFixed(2)}`;
            } else if (D === 0) {
                let r = -b / (2*a);
                roots = `One Root at x = ${r.toFixed(2)}`;
            } else {
                roots = "No Real Roots";
            }
            
            analysisHTML += `<strong>Function ${i+1} (Quadratic):</strong><br>`;
            analysisHTML += `<small>Vertex: (${h.toFixed(2)}, ${k.toFixed(2)})</small><br>`;
            analysisHTML += `<small>${roots}</small><br><hr style="border-color:#444; margin:5px 0;">`;
            
            historyText = `Quad: Vertex (${h.toFixed(2)}, ${k.toFixed(2)})`;
        }
    });

    if(!analysisHTML) analysisHTML = "Plot generated. <br><small>Add a Quadratic function to see vertex/roots analysis.</small>";

    // 4. Render
    let layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#ddd' },
        xaxis: { title: 'X', zerolinecolor: '#666', gridcolor: '#333' },
        yaxis: { title: 'Y', zerolinecolor: '#666', gridcolor: '#333' },
        margin: { t: 30, b: 40, l: 40, r: 20 },
        showlegend: true,
        legend: { x: 0, y: 1.1, orientation: "h" }
    };
    
    if (typeof Plotly !== 'undefined') {
        Plotly.newPlot(graphId, plotData, layout, {displayModeBar: false, responsive: true});
    }

    var resultText = analysisHTML;
"""

graph_latex = r"P(x) = a_n x^n + a_{n-1} x^{n-1} + \dots + a_1 x + a_0"

graph_content = """
### Graphing Polynomials
This tool allows you to visualize functions of higher degrees. While a linear equation ($y=mx+b$) produces a straight line, higher-order polynomials produce curves with peaks and valleys.

### Degrees Explained
* **Degree 1 (Linear):** A straight line.
* **Degree 2 (Quadratic):** A Parabola (U-shape). This calculator will automatically find the **Vertex** (the turning point) and the **Roots** (where it crosses the x-axis).
* **Degree 3 (Cubic):** An S-shaped curve that can have up to two turning points.
* **Degree 4 (Quartic):** A W-shaped or M-shaped curve with up to three turning points.
"""

graph_vars = r"""
* $n$ is the **Degree** (highest power).
* $a_n$ are the **Coefficients** (the numbers in front of the variables).
"""

# === GENERATE THE FILE ===
create_calculator(
    title="Polynomial Grapher", 
    category="Algebra", 
    description="Plot and analyze Quadratic, Cubic, and Quartic functions. Automatically calculates vertex and roots for parabolas.",
    inputs_html=graph_inputs,
    calculation_js=graph_js,
    formula_latex=graph_latex,
    educational_content=graph_content,
    variable_definitions=graph_vars 
)