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
    
    <div id="loading_status_{tool_id}" style="display:none; color: #888; font-size: 0.8em; margin-bottom: 5px;">Loading 3D Engine...</div>

    <div style="margin-bottom: 15px; border-bottom: 1px solid #444; padding-bottom: 10px;">
        <label style="font-weight:bold; color:#ddd; margin-right:10px;">Select Shape:</label>
        <select id="shape_select_{tool_id}" class="shape-select" onchange="updateInputs_{tool_id}()">
            <option value="paraboloid">Elliptic Paraboloid (The Bowl)</option>
            <option value="saddle">Hyperbolic Paraboloid (The Saddle)</option>
            <option value="torus">Torus (The Donut)</option>
            <option value="sphere">Sphere</option>
            <option value="cone">Cone</option>
        </select>
    </div>

    <div id="inputs_container_{tool_id}" class="inputs-box">
        </div>
    
    <button onclick="calculate_{tool_id}()" class="btn-primary">Generate 3D Surface</button>

    <div id="graph_{tool_id}" class="graph-box"></div>

    <div id="result_box" class="result-box" style="display:none;">
        <span id="result_val"></span>
    </div>
    
    <div style="margin-top: 15px; text-align: center; font-size: 0.85em;">
        <a href="#the-math-behind-it" style="color: #888; text-decoration: underline; cursor: pointer;">
            How 3D Surfaces are Calculated
        </a>
    </div>
  </div>

  <div class="calc-history">
    <h4>Shape Properties</h4>
    <div id="math_display_{tool_id}" style="color:#bbb; font-style:italic; margin-bottom:15px; font-size:0.9em;">
        Select a shape to see its formula.
    </div>
    <ul id="history_list_{tool_id}"></ul>
    <button onclick="clearHistory_{tool_id}()" class="btn-small">Clear Log</button>
  </div>
</div>

<script>
    const STORAGE_KEY_{tool_id} = "calcfoundry_3d_{tool_id}"; 

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

    window.addEventListener('load', loadPlotlyAndInit_{tool_id});

    function initCalculator_{tool_id}() {{
        updateInputs_{tool_id}(); // Build initial inputs
        renderHistory_{tool_id}();
        
        // Render initial graph (Paraboloid) after a brief delay
        setTimeout(() => {{
            calculate_{tool_id}();
        }}, 500);
    }}

    function updateInputs_{tool_id}() {{
        const shape = document.getElementById('shape_select_{tool_id}').value;
        const container = document.getElementById('inputs_container_{tool_id}');
        const mathDisp = document.getElementById('math_display_{tool_id}');
        
        let html = '';
        let formula = '';

        // Helper for input html
        const makeInput = (id, label, val, min, max, step) => `
            <div class="term-wrapper">
                <span class="eq-label">${{label}} =</span>
                <input type="number" id="${{id}}" class="eq-input" value="${{val}}" step="${{step}}">
            </div>
        `;

        if (shape === 'paraboloid') {{
            html += '<div class="eq-group">';
            html += '<span class="eq-main-label">z = </span>';
            html += makeInput('coef_a', 'x²', 0.5, -10, 10, 0.1);
            html += '<span class="eq-operator">+</span>';
            html += makeInput('coef_b', 'y²', 0.5, -10, 10, 0.1);
            html += '</div>';
            formula = "z = ax² + by²";
        }} 
        else if (shape === 'saddle') {{
            html += '<div class="eq-group">';
            html += '<span class="eq-main-label">z = </span>';
            html += makeInput('coef_a', 'x²', 1, -10, 10, 0.1);
            html += '<span class="eq-operator">-</span>';
            html += makeInput('coef_b', 'y²', 1, -10, 10, 0.1);
            html += '</div>';
            formula = "z = ax² - by²";
        }}
        else if (shape === 'torus') {{
            html += '<div class="eq-group">';
            html += makeInput('radius_R', 'Major Radius (R)', 5, 1, 20, 0.5);
            html += makeInput('radius_r', 'Tube Radius (r)', 2, 0.5, 10, 0.5);
            html += '</div>';
            formula = "Parametric Torus (R, r)";
        }}
        else if (shape === 'sphere') {{
             html += '<div class="eq-group">';
             html += makeInput('radius_R', 'Radius (r)', 5, 1, 20, 0.5);
             html += '</div>';
             formula = "x² + y² + z² = r²";
        }}
        else if (shape === 'cone') {{
            html += '<div class="eq-group">';
            html += '<span class="eq-main-label">z = </span>';
            html += makeInput('coef_a', 'Slope', 1, 0.1, 5, 0.1);
            html += '<span class="eq-var">√(x² + y²)</span>';
            html += '</div>';
            formula = "z = a√(x² + y²)";
        }}

        container.innerHTML = html;
        mathDisp.innerText = "Formula: " + formula;
    }}

    function calculate_{tool_id}() {{
        {calculation_js}
        
        // Render 3D Plot
        let layout = {{
            margin: {{ t: 0, b: 0, l: 0, r: 0 }},
            paper_bgcolor: 'rgba(0,0,0,0)',
            scene: {{
                xaxis: {{title: 'X', gridcolor: '#444', zerolinecolor: '#666', showbackground: false}},
                yaxis: {{title: 'Y', gridcolor: '#444', zerolinecolor: '#666', showbackground: false}},
                zaxis: {{title: 'Z', gridcolor: '#444', zerolinecolor: '#666', showbackground: false}},
                camera: {{ eye: {{x: 1.5, y: 1.5, z: 1.5}} }} // Nice Isometric view
            }}
        }};

        Plotly.newPlot('graph_{tool_id}', [data], layout, {{displayModeBar: true, responsive: true}});
        
        // Add to history
        addToHistory_{tool_id}(historyText);
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
  
  /* SHAPE SELECT */
  .shape-select {{
      background: #333; color: #fff; border: 1px solid #555; padding: 8px; border-radius: 4px; font-size: 1em; width: 100%; max-width: 300px;
  }}

  /* INPUT AREA */
  .inputs-box {{
      background: #2d2d2d;
      padding: 15px;
      border-radius: 6px;
      border-left: 4px solid #00bcd4; /* Cyan for 3D */
      margin-bottom: 20px;
  }}

  .eq-group {{ 
      display: flex; 
      flex-wrap: wrap; 
      align-items: center; 
      gap: 10px; 
  }}

  .term-wrapper {{
      display: inline-flex !important;
      align-items: center;
      white-space: nowrap;
      gap: 5px;
  }}

  /* TEXT ELEMENTS */
  .eq-main-label {{ font-weight: bold; color: #00bcd4; font-size: 1.2em; }}
  .eq-label {{ font-weight: bold; color: #ddd; }}
  .eq-operator {{ font-weight: bold; color: #888; }}
  .eq-var {{ color: #bbb; font-style: italic; }}
  
  /* COMPACT INPUT FIELDS */
  .eq-input {{ 
      width: 70px !important;
      padding: 6px !important;
      background: #111 !important; 
      border: 1px solid #444 !important; 
      color: white !important; 
      border-radius: 4px !important; 
      text-align: center;
  }}
  .eq-input:focus {{ border-color: #00bcd4 !important; outline: none; }}

  /* BUTTONS */
  .btn-primary {{ width: 100%; padding: 12px; background: #00bcd4; color: #111; border: none; cursor: pointer; border-radius: 4px; font-weight: bold; margin-bottom: 20px; transition: background 0.2s; }}
  .btn-primary:hover {{ background: #00acc1; }}

  /* GRAPH CONTAINER */
  .graph-box {{ 
      width: 100%; 
      height: 500px; /* Taller for 3D */
      background: #111; 
      border: 1px solid #444; 
      border-radius: 4px;
  }}
  
  .calc-history {{ background: #252526; padding: 15px; border-radius: 8px; font-size: 0.9em; height: fit-content; }}
  .calc-history ul {{ padding-left: 20px; color: #bbb; margin: 0; }}
  .calc-history li {{ margin-bottom: 8px; line-height: 1.4; }}
  .btn-small {{ background: #444; font-size: 0.8em; padding: 5px 10px; margin-top: 15px; border:none; color:white; cursor:pointer; width: 100%; border-radius: 4px; }}
</style>

{{{{< /calculator >}}}}

## How to Use
{educational_content}

## The Math Behind It
We use Multivariable Calculus to plot these surfaces.

$$
{formula_latex}
$$

**Where:**
{variable_definitions}
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {filename}")


# === DEFINING THE 3D GRAPHER LOGIC ===

# Inputs are handled dynamically via `updateInputs` in HTML section
# We only need the calculation logic here
graph_inputs = "" 

graph_js = """
    const shape = document.getElementById('shape_select_{tool_id}').value;
    let data = {};
    let historyText = "";

    // -- GENERATOR HELPERS --
    // Create linearly spaced array
    const linspace = (start, end, num) => {
        let arr = [];
        let step = (end - start) / (num - 1);
        for(let i=0; i<num; i++) arr.push(start + (step * i));
        return arr;
    };

    if (shape === 'paraboloid' || shape === 'saddle' || shape === 'cone') {
        // --- EXPLICIT SURFACES z = f(x,y) ---
        let a = parseFloat(document.getElementById('coef_a').value) || 1;
        let b = 1;
        if(document.getElementById('coef_b')) b = parseFloat(document.getElementById('coef_b').value) || 1;
        
        let size = 20;
        let range = 10;
        let x = linspace(-range, range, size);
        let y = linspace(-range, range, size);
        let z = [];

        for(let i=0; i<y.length; i++) {
            let row = [];
            for(let j=0; j<x.length; j++) {
                let val = 0;
                let xi = x[j];
                let yi = y[i];
                
                if (shape === 'paraboloid') {
                    val = a * xi*xi + b * yi*yi;
                } else if (shape === 'saddle') {
                    val = a * xi*xi - b * yi*yi;
                } else if (shape === 'cone') {
                    val = a * Math.sqrt(xi*xi + yi*yi);
                }
                row.push(val);
            }
            z.push(row);
        }

        data = {
            z: z,
            x: x,
            y: y,
            type: 'surface',
            colorscale: 'Viridis',
            showscale: false
        };
        
        let eq = (shape === 'paraboloid') ? `z = ${a}x² + ${b}y²` : (shape === 'saddle' ? `z = ${a}x² - ${b}y²` : `z = ${a}√(x²+y²)`);
        historyText = `${shape.charAt(0).toUpperCase() + shape.slice(1)}: ${eq}`;
    } 
    else if (shape === 'torus' || shape === 'sphere') {
        // --- PARAMETRIC SURFACES ---
        let steps = 30; // Mesh resolution
        let u = linspace(0, 2*Math.PI, steps); // 0 to 360 deg
        let v = linspace(0, 2*Math.PI, steps);
        
        let x = [], y = [], z = [];

        let R = parseFloat(document.getElementById('radius_R').value) || 5;
        let r = 0;
        if(document.getElementById('radius_r')) r = parseFloat(document.getElementById('radius_r').value) || 2;

        for(let i=0; i<v.length; i++) {
            let x_row = [], y_row = [], z_row = [];
            for(let j=0; j<u.length; j++) {
                let theta = u[j];
                let phi = v[i];
                
                let px, py, pz;
                
                if (shape === 'torus') {
                    // Torus Formula
                    px = (R + r * Math.cos(theta)) * Math.cos(phi);
                    py = (R + r * Math.cos(theta)) * Math.sin(phi);
                    pz = r * Math.sin(theta);
                } else {
                    // Sphere Formula (R is used as radius here)
                    // u = theta (azimuth), v = phi (elevation 0 to PI)
                    let phi_sphere = linspace(0, Math.PI, steps)[i];
                    px = R * Math.sin(phi_sphere) * Math.cos(theta);
                    py = R * Math.sin(phi_sphere) * Math.sin(theta);
                    pz = R * Math.cos(phi_sphere);
                }

                x_row.push(px);
                y_row.push(py);
                z_row.push(pz);
            }
            x.push(x_row);
            y.push(y_row);
            z.push(z_row);
        }

        data = {
            x: x, y: y, z: z,
            type: 'surface',
            colorscale: 'Jet',
            showscale: false
        };
        
        let desc = (shape === 'torus') ? `R=${R}, r=${r}` : `r=${R}`;
        historyText = `${shape.charAt(0).toUpperCase() + shape.slice(1)}: ${desc}`;
    }
"""

graph_latex = r"\text{Paraboloid: } z = \frac{x^2}{a^2} + \frac{y^2}{b^2} \quad | \quad \text{Saddle: } z = \frac{y^2}{b^2} - \frac{x^2}{a^2}"

graph_content = """
### Exploring 3D Topology
Topologies are the shapes of space. While 2D graphs show lines, 3D graphs show surfaces. This tool helps you visualize how changing parameters affects the curvature of space.

### The Shapes
1.  **Elliptic Paraboloid:** Often called a "Bowl." It has a single minimum point. Used in satellite dishes to focus signals.
2.  **Hyperbolic Paraboloid:** The "Saddle" or "Pringle." It curves up in one direction and down in the other. This is a classic example of a surface with "negative curvature."
3.  **Torus:** A Donut shape. It is a surface with a "genus" of 1 (one hole).
"""

graph_vars = r"""
* $x, y, z$ are the spatial coordinates.
* $R$ is the **Major Radius** (distance from center to the tube).
* $r$ is the **Minor Radius** (thickness of the tube).
"""

# === GENERATE THE FILE ===
create_calculator(
    title="3D Topology Explorer", 
    category="Geometry", 
    description="Interactive 3D Surface Grapher. Visualize Paraboloids, Hyperboloids, Torus knots, and Spheres in real-time.",
    inputs_html=graph_inputs,
    calculation_js=graph_js,
    formula_latex=graph_latex,
    educational_content=graph_content,
    variable_definitions=graph_vars 
)