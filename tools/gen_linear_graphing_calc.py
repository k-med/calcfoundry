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

    # --- INJECT TOOL_ID DIRECTLY INTO JS ---
    # We replace the placeholder in the JS string before writing it to the file
    calculation_js = calculation_js.replace("{tool_id}", tool_id)

    content = f"""---
title: "{title}"
date: {date_str}
categories: ["{category}"]
summary: "{description}"
math: true
disableSpecial1stPost: true
---

<script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>

{description}

{{{{< calculator >}}}}

<div class="calc-grid">
  <div class="calc-main">
    
    <div id="lines_container_{tool_id}" class="lines-container">
        </div>
    
    <div class="button-row">
        <button onclick="addLine_{tool_id}()" class="btn-secondary">+ Add Line</button>
        <button onclick="calculate_{tool_id}()" class="btn-primary">Plot & Solve</button>
    </div>

    <div id="graph_{tool_id}" class="graph-box"></div>

    <div id="result_box" class="result-box" style="display:none;">
        <span id="result_val"></span>
    </div>
    
    <div style="margin-top: 15px; text-align: center; font-size: 0.85em;">
        <a href="#the-math-behind-it" style="color: #888; text-decoration: underline; cursor: pointer;">
            How the math works
        </a>
    </div>
  </div>

  <div class="calc-history">
    <h4>Analysis Log</h4>
    <ul id="history_list_{tool_id}"></ul>
    <button onclick="clearHistory_{tool_id}()" class="btn-small">Clear Log</button>
  </div>
</div>

<script>
    const STORAGE_KEY_{tool_id} = "calcfoundry_history_{tool_id}"; 
    let lineCount_{tool_id} = 0;

    // Wait for window load to ensure Plotly is ready
    window.addEventListener('load', function() {{
        // Initialize with two lines
        addLine_{tool_id}(); 
        addLine_{tool_id}();
        renderHistory_{tool_id}();
        
        // Pre-fill inputs with example data so the user sees something immediately
        setTimeout(() => {{
            const inputs = document.querySelectorAll('#lines_container_{tool_id} input');
            if(inputs.length >= 4) {{
                inputs[0].value = 2;   // Line 1 Slope
                inputs[1].value = 1;   // Line 1 Intercept
                inputs[2].value = -0.5;// Line 2 Slope
                inputs[3].value = 4;   // Line 2 Intercept
                calculate_{tool_id}(); // Auto-plot
            }}
        }}, 100);
    }});

    function addLine_{tool_id}() {{
        const container = document.getElementById('lines_container_{tool_id}');
        const id = lineCount_{tool_id}++;
        
        const div = document.createElement('div');
        div.className = 'line-input-row';
        div.id = 'line_row_' + id;
        
        // HTML Structure for: y = [ m ] x + [ b ]  [X]
        div.innerHTML = `
            <div class="eq-group">
                <span class="eq-text y-equals">y =</span>
                <input type="number" class="eq-input" placeholder="m" step="any">
                <span class="eq-text">x +</span>
                <input type="number" class="eq-input" placeholder="b" step="any">
            </div>
            <button onclick="removeLine_{tool_id}(${{id}})" class="btn-remove" title="Remove Line">×</button>
        `;
        container.appendChild(div);
    }}

    function removeLine_{tool_id}(id) {{
        const row = document.getElementById('line_row_' + id);
        if(row) row.remove();
        // Re-calculate after removing a line to update the graph
        calculate_{tool_id}(); 
    }}

    function calculate_{tool_id}() {{
        {calculation_js}
        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        if(resultText) resBox.style.display = 'block';
        
        // Add to history if valid
        if (historyText && historyText !== "Lines Plotted") addToHistory_{tool_id}(historyText);
    }}

    function addToHistory_{tool_id}(item) {{
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
  .calc-history {{ background: #252526; padding: 15px; border-radius: 8px; font-size: 0.9em; height: fit-content; }}
  
  /* INPUT ROWS - THE FIX FOR UGLY BUTTONS */
  .lines-container {{ display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; }}
  
  .line-input-row {{ 
      display: flex; 
      align-items: center; 
      justify-content: space-between; 
      background: #2d2d2d; 
      padding: 10px 15px; 
      border-radius: 6px; 
      border-left: 4px solid #007bff; 
  }}
  
  .eq-group {{ display: flex; align-items: center; gap: 8px; flex: 1; }}
  .eq-text {{ font-weight: bold; font-family: monospace; font-size: 1.1em; color: #ddd; }}
  .y-equals {{ color: #007bff; }}
  
  /* INPUT FIELDS */
  .eq-input {{ 
      width: 70px; /* Fixed width prevents stretching */
      padding: 6px; 
      background: #111; 
      border: 1px solid #444; 
      color: white; 
      border-radius: 4px; 
      text-align: center;
  }}
  .eq-input:focus {{ border-color: #007bff; outline: none; }}

  /* BUTTONS */
  .button-row {{ display: flex; gap: 10px; margin-bottom: 20px; }}
  
  .btn-primary {{ flex: 2; padding: 12px; background: #007bff; color: white; border: none; cursor: pointer; border-radius: 4px; font-weight: bold; transition: background 0.2s; }}
  .btn-primary:hover {{ background: #0056b3; }}
  
  .btn-secondary {{ flex: 1; padding: 12px; background: #444; color: white; border: none; cursor: pointer; border-radius: 4px; transition: background 0.2s; }}
  .btn-secondary:hover {{ background: #555; }}

  /* CLOSE BUTTON FIX */
  .btn-remove {{ 
      flex: 0 0 28px; /* Fixed size, don't grow or shrink */
      height: 28px; 
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
      line-height: 1;
      margin-left: 10px;
  }}
  .btn-remove:hover {{ background: #a71d2a; }}

  /* GRAPH CONTAINER */
  .graph-box {{ 
      width: 100%; 
      height: 450px; 
      background: #111; 
      border: 1px solid #444; 
      border-radius: 4px;
      position: relative;
  }}
  
  .result-box {{ margin-top: 20px; padding: 15px; background: #2d2d2d; border-left: 4px solid #28a745; }}
  
  .calc-history h4 {{ margin-top: 0; border-bottom: 1px solid #444; padding-bottom: 5px; color: #ddd; }}
  .calc-history ul {{ padding-left: 20px; color: #bbb; margin: 0; }}
  .calc-history li {{ margin-bottom: 5px; }}
  .btn-small {{ background: #444; font-size: 0.8em; padding: 5px 10px; margin-top: 15px; border:none; color:white; cursor:pointer; width: 100%; border-radius: 4px; }}
</style>

{{{{< /calculator >}}}}

## How to Use
{educational_content}

## The Math Behind It
We calculate properties using the standard Slope-Intercept form:

$$
{formula_latex}
$$

**Where:**
{variable_definitions}
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {filename}")


# === DEFINING THE LINEAR GRAPHER LOGIC ===

graph_inputs = "" 

graph_js = """
    const containerId = 'lines_container_{tool_id}';
    const graphId = 'graph_{tool_id}';

    // 1. Gather all active inputs
    let lines = [];
    const container = document.getElementById(containerId);
    if(!container) return; // Safety check
    
    const rows = container.getElementsByClassName('line-input-row');
    
    for (let row of rows) {
        let inputs = row.getElementsByTagName('input');
        if (inputs.length >= 2) {
            let mVal = inputs[0].value;
            let bVal = inputs[1].value;

            // Only parse if not empty
            if (mVal !== "" && bVal !== "") {
                let m = parseFloat(mVal);
                let b = parseFloat(bVal);
                lines.push({m: m, b: b});
            }
        }
    }

    // 2. Determine Graph Range (Zoom level)
    let minX = -10, maxX = 10;
    let minY = -10, maxY = 10; 
    let intersections = [];
    let analysisHTML = "";

    // Analyze intersections to auto-scale graph
    if (lines.length > 1) {
        analysisHTML += "<strong>Intersections:</strong><br><ul style='font-size:0.9em; margin-bottom: 10px;'>";
        for (let i = 0; i < lines.length; i++) {
            for (let j = i + 1; j < lines.length; j++) {
                let l1 = lines[i];
                let l2 = lines[j];
                
                if (l1.m !== l2.m) {
                    let x_int = (l2.b - l1.b) / (l1.m - l2.m);
                    let y_int = l1.m * x_int + l1.b;
                    
                    intersections.push({x: x_int, y: y_int, label: `(${x_int.toFixed(2)}, ${y_int.toFixed(2)})`});
                    
                    // Expand graph range to include this intersection
                    if (x_int < minX) minX = x_int - 5;
                    if (x_int > maxX) maxX = x_int + 5;
                    if (y_int < minY) minY = y_int - 5;
                    if (y_int > maxY) maxY = y_int + 5;

                    analysisHTML += `<li>L${i+1} & L${j+1}: <span style="color:#28a745;">(${x_int.toFixed(2)}, ${y_int.toFixed(2)})</span></li>`;
                }
            }
        }
        analysisHTML += "</ul>";
    }
    
    // Fallback if no lines
    if(lines.length === 0) {
        analysisHTML = "Please enter values for Slope (m) and Y-Intercept (b).";
    }

    // 3. Generate Plot Data
    let plotData = [];
    
    lines.forEach((line, index) => {
        // Calculate Y values at the dynamic minX and maxX
        let y1 = line.m * minX + line.b;
        let y2 = line.m * maxX + line.b;
        
        plotData.push({
            x: [minX, maxX],
            y: [y1, y2],
            mode: 'lines',
            name: `y = ${line.m}x + ${line.b}`,
            line: { width: 3 }
        });
    });

    // Add intersection markers
    if (intersections.length > 0) {
        plotData.push({
            x: intersections.map(p => p.x),
            y: intersections.map(p => p.y),
            mode: 'markers',
            type: 'scatter',
            name: 'Intersections',
            marker: { size: 10, color: '#ff4444', line: {color: 'white', width: 2} },
            text: intersections.map(p => p.label)
        });
    }

    // 4. Render Plot
    let layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#ddd' },
        xaxis: { 
            title: 'X Axis', 
            zerolinecolor: '#666', 
            gridcolor: '#333',
            range: [minX, maxX] 
        },
        yaxis: { 
            title: 'Y Axis', 
            zerolinecolor: '#666', 
            gridcolor: '#333',
            range: [minY, maxY] // Auto-scale Y based on intersections
        },
        showlegend: true,
        legend: { x: 0, y: 1.1, orientation: "h", font: {size: 10} },
        margin: { t: 40, b: 40, l: 40, r: 20 },
        hovermode: 'closest'
    };
    
    // Ensure Plotly is loaded
    if (typeof Plotly !== 'undefined') {
        Plotly.newPlot(graphId, plotData, layout, {displayModeBar: false, responsive: true});
    } else {
        console.error("Plotly library not loaded.");
        document.getElementById(graphId).innerHTML = "<p style='padding:20px; color:red;'>Error: Graphing library failed to load.</p>";
    }

    var resultText = analysisHTML;
    var historyText = (intersections.length > 0) ? `${intersections.length} Intersection(s)` : "Graph Updated";
"""

graph_latex = r"y = mx + b \quad \bigg| \quad x_{int} = \frac{b_2 - b_1}{m_1 - m_2}"

graph_content = """
### Visualizing Linear Equations
This tool allows you to plot multiple lines simultaneously to see how they behave and where they meet.

### Features
1.  **Multiple Lines:** Click "Add Line" to compare as many equations as you need.
2.  **Intersection Solver:** The tool automatically calculates the exact $(x, y)$ coordinates where any two lines cross.
3.  **Auto-Zoom:** The graph automatically scales to show you the relevant intersection points.

### Who is this for?
* **Students:** Visualize systems of linear equations to verify your algebra homework.
* **Economics:** Find the equilibrium point where Supply ($y=mx+b$) meets Demand ($y=-mx+b$).
* **Business:** Calculate the Break-Even point where Revenue intersects with Costs.
"""

graph_vars = r"""
* $m$ is the **Slope** (Rise over Run).
* $b$ is the **Y-Intercept** (where the line crosses the vertical axis).
* $x_{int}$ is the x-coordinate of the **Intersection**.
"""

# === GENERATE THE FILE ===
create_calculator(
    title="Linear Equation Grapher", 
    category="Algebra", 
    description="Plot multiple linear equations (y=mx+b), find intersection points, and calculate x/y intercepts instantly with interactive graphs.",
    inputs_html=graph_inputs,
    calculation_js=graph_js,
    formula_latex=graph_latex,
    educational_content=graph_content,
    variable_definitions=graph_vars 
)