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

<script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>

{description}

{{{{< calculator >}}}}

<div class="calc-grid">
  <div class="calc-main">
    <div id="lines_container_{tool_id}">
        </div>
    
    <div style="display: flex; gap: 10px; margin-top: 10px;">
        <button onclick="addLine_{tool_id}()" class="btn-secondary">+ Add Line</button>
        <button onclick="calculate_{tool_id}()" class="btn-primary">Plot & Solve</button>
    </div>

    <div id="graph_{tool_id}" style="width:100%; height:400px; margin-top:20px; border: 1px solid #444;"></div>

    <div id="result_box" class="result-box" style="display:none;">
        <span id="result_val"></span>
    </div>
    
    <div style="margin-top: 15px; text-align: center; font-size: 0.85em;">
        <a href="#the-math-behind-it" style="color: #888; text-decoration: underline; cursor: pointer;">
            Understanding Slope-Intercept Form
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
    // DEFINE THE ID FOR JS SCOPE
    const tool_id_{tool_id} = "{tool_id}";
    const STORAGE_KEY_{tool_id} = "calcfoundry_history_{tool_id}"; 
    let lineCount_{tool_id} = 0;

    // Use addEventListener to avoid overwriting other page scripts
    window.addEventListener('load', function() {{
        // Initialize with two lines by default
        addLine_{tool_id}(); 
        addLine_{tool_id}();
        renderHistory_{tool_id}();
        
        // Pre-fill some example data
        const m0 = document.getElementById('m_0');
        const b0 = document.getElementById('b_0');
        const m1 = document.getElementById('m_1');
        const b1 = document.getElementById('b_1');

        if(m0) m0.value = 2;
        if(b0) b0.value = 1;
        if(m1) m1.value = -0.5;
        if(b1) b1.value = 4;
        
        calculate_{tool_id}(); // Initial plot
    }});

    function addLine_{tool_id}() {{
        const container = document.getElementById('lines_container_{tool_id}');
        const id = lineCount_{tool_id}++;
        
        const div = document.createElement('div');
        div.className = 'line-input-row';
        div.id = 'line_row_' + id;
        div.innerHTML = `
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-weight:bold; color:#007bff;">y = </span>
                <input type="number" id="m_${{id}}" placeholder="m" step="any" style="flex:1; min-width: 60px;">
                <span style="font-weight:bold;">x + </span>
                <input type="number" id="b_${{id}}" placeholder="b" step="any" style="flex:1; min-width: 60px;">
                <button onclick="removeLine_{tool_id}(${{id}})" class="btn-remove" title="Remove Line">×</button>
            </div>
        `;
        container.appendChild(div);
    }}

    function removeLine_{tool_id}(id) {{
        const row = document.getElementById('line_row_' + id);
        if(row) row.remove();
    }}

    function calculate_{tool_id}() {{
        {calculation_js}
        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        resBox.style.display = 'block';
        
        // Only add to history if we have meaningful results
        if (historyText && historyText !== "Lines Plotted") addToHistory_{tool_id}(historyText);
    }}

    function addToHistory_{tool_id}(item) {{
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_{tool_id})) || [];
        // Prevent duplicate consecutive entries
        if (history.length === 0 || history[0] !== item) {{
            history.unshift(item);
            if (history.length > 5) history.pop();
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
</script>

<style>
  .calc-grid {{ display: grid; gap: 20px; grid-template-columns: 1fr; }}
  @media (min-width: 768px) {{ .calc-grid {{ grid-template-columns: 2fr 1fr; }} }}
  .calc-history {{ background: #252526; padding: 15px; border-radius: 8px; font-size: 0.9em; }}
  .calc-history h4 {{ margin-top: 0; border-bottom: 1px solid #444; padding-bottom: 5px; }}
  .calc-history ul {{ padding-left: 20px; color: #bbb; }}
  .btn-small {{ background: #444; font-size: 0.8em; padding: 5px 10px; margin-top: 10px; border:none; color:white; cursor:pointer; }}
  
  .calc-main {{ background: #1e1e1e; padding: 15px; border-radius: 8px; }}
  .line-input-row {{ background: #2d2d2d; padding: 10px; margin-bottom: 10px; border-radius: 4px; border-left: 3px solid #007bff; }}
  
  .calc-main input {{ background: #333; border: 1px solid #555; color: white; padding: 5px; border-radius: 3px; }}
  
  .btn-primary {{ width: 100%; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; border-radius: 4px; font-weight:bold; }}
  .btn-primary:hover {{ background: #0056b3; }}
  
  .btn-secondary {{ width: 100%; padding: 10px; background: #444; color: white; border: none; cursor: pointer; border-radius: 4px; }}
  .btn-secondary:hover {{ background: #555; }}

  .btn-remove {{ background: #ff4444; color: white; border: none; width: 25px; height: 25px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-weight: bold; }}
  
  .result-box {{ margin-top: 20px; padding: 15px; background: #2d2d2d; border-left: 4px solid #28a745; }}
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

# Inputs are generated dynamically via JS
graph_inputs = "" 

graph_js = """
    // Retrieve the tool ID from the variable we defined in the HTML
    // Note: In the python f-string context, {tool_id} becomes the actual string.
    // In JS context, we use the variable we defined: tool_id_{tool_id}
    
    const currentToolId = tool_id_{tool_id};

    // 1. Gather all active inputs
    let lines = [];
    const container = document.getElementById('lines_container_' + currentToolId);
    const rows = container.getElementsByClassName('line-input-row');
    
    for (let row of rows) {
        let inputs = row.getElementsByTagName('input');
        // Ensure inputs exist before accessing
        if (inputs.length >= 2) {
            let mVal = inputs[0].value;
            let bVal = inputs[1].value;

            // Only parse if not empty strings
            if (mVal !== "" && bVal !== "") {
                let m = parseFloat(mVal);
                let b = parseFloat(bVal);
                lines.push({m: m, b: b, eq: `y = ${m}x + ${b}`});
            }
        }
    }

    if (lines.length === 0) {
        document.getElementById('result_val').innerText = "Please enter valid numbers for Slope (m) and Y-Intercept (b).";
        return;
    }

    // 2. Calculate Intersections to determine Graph Range
    let intersections = [];
    let minX = -10, maxX = 10; // Defaults

    let analysisHTML = "";
    
    // Analyze individual lines
    analysisHTML += "<strong>Properties:</strong><br><ul style='font-size:0.9em; margin-bottom:10px;'>";
    lines.forEach((l, i) => {
        let xInt = (l.m !== 0) ? (-l.b / l.m).toFixed(2) : "None (Horizontal)";
        let yInt = l.b;
        analysisHTML += `<li>Line ${i+1}: X-Int at ${xInt}, Y-Int at ${yInt}</li>`;
    });
    analysisHTML += "</ul>";

    // Analyze intersections
    if (lines.length > 1) {
        analysisHTML += "<strong>Intersections:</strong><br><ul style='font-size:0.9em;'>";
        for (let i = 0; i < lines.length; i++) {
            for (let j = i + 1; j < lines.length; j++) {
                let l1 = lines[i];
                let l2 = lines[j];
                
                if (l1.m === l2.m) {
                     analysisHTML += `<li>L${i+1} & L${j+1}: Parallel (No intersection)</li>`;
                } else {
                    let x_int = (l2.b - l1.b) / (l1.m - l2.m);
                    let y_int = l1.m * x_int + l1.b;
                    
                    intersections.push({x: x_int, y: y_int, label: `Int: L${i+1}-L${j+1}`});
                    
                    // Expand graph range to include this intersection
                    if (x_int < minX) minX = x_int - 5;
                    if (x_int > maxX) maxX = x_int + 5;

                    analysisHTML += `<li>L${i+1} & L${j+1} at <span style="color:#28a745; font-weight:bold;">(${x_int.toFixed(2)}, ${y_int.toFixed(2)})</span></li>`;
                }
            }
        }
        analysisHTML += "</ul>";
    }

    // 3. Generate Plot Data with Dynamic Range
    let plotData = [];
    
    lines.forEach((line, index) => {
        // Calculate Y values at the new minX and maxX
        let y1 = line.m * minX + line.b;
        let y2 = line.m * maxX + line.b;
        
        plotData.push({
            x: [minX, maxX],
            y: [y1, y2],
            mode: 'lines',
            name: `y=${line.m}x + ${line.b}`,
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
            marker: { size: 12, color: '#ff4444', line: {color: 'white', width: 2} },
            text: intersections.map(p => p.label)
        });
    }

    // 4. Render Plot
    let layout = {
        title: 'Linear Equations Plot',
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#ddd' },
        xaxis: { title: 'X Axis', zerolinecolor: '#666', gridcolor: '#333' },
        yaxis: { title: 'Y Axis', zerolinecolor: '#666', gridcolor: '#333' },
        showlegend: true,
        legend: { x: 0, y: 1.1, orientation: "h" },
        margin: { t: 50, b: 40, l: 50, r: 20 },
        hovermode: 'closest'
    };

    Plotly.newPlot('graph_' + currentToolId, plotData, layout, {displayModeBar: false});

    var resultText = analysisHTML;
    var historyText = (intersections.length > 0) ? `${intersections.length} Intersection(s) found` : "Lines Plotted";
"""

graph_latex = r"y = mx + b \quad \bigg| \quad x_{int} = \frac{b_2 - b_1}{m_1 - m_2}"

graph_content = """
### Visualizing Linear Equations
This tool allows you to plot multiple lines simultaneously to see how they behave and where they meet.

### Features
1.  **Multiple Lines:** Click "Add Line" to compare as many equations as you need.
2.  **Intersection Solver:** The tool automatically calculates the exact $(x, y)$ coordinates where any two lines cross.
3.  **Intercepts:** Quickly see where each line crosses the X and Y axes.

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