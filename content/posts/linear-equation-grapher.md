---
title: "Linear Equation Grapher"
date: 2025-12-10
categories: ["Algebra"]
summary: "Plot multiple linear equations (y=mx+b), find intersection points, and calculate x/y intercepts instantly with interactive graphs."
math: true
disableSpecial1stPost: true
---

Plot multiple linear equations (y=mx+b), find intersection points, and calculate x/y intercepts instantly with interactive graphs.

{{< calculator >}}

<div class="calc-grid">
  <div class="calc-main">
    
    <div id="loading_status_linear_equation_grapher" style="display:none; color: #888; font-size: 0.8em; margin-bottom: 5px;">Loading Graph Engine...</div>

    <div id="lines_container_linear_equation_grapher" class="lines-container">
        </div>
    
    <div class="button-row">
        <button onclick="addLine_linear_equation_grapher()" class="btn-secondary">+ Add Line</button>
        <button onclick="calculate_linear_equation_grapher()" class="btn-primary">Plot & Solve</button>
    </div>

    <div id="graph_linear_equation_grapher" class="graph-box"></div>

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
    <ul id="history_list_linear_equation_grapher"></ul>
    
    <div style="display:flex; gap:10px; margin-top:10px;">
        <button onclick="downloadHistory_linear_equation_grapher()" class="btn-small" style="flex:1;">Save</button>
        <button onclick="clearHistory_linear_equation_grapher()" class="btn-small" style="flex:1;">Clear Log</button>
    </div>
  </div>
</div>

<script>
    const STORAGE_KEY_linear_equation_grapher = "calcfoundry_history_linear_equation_grapher"; 
    let lineCount_linear_equation_grapher = 0;

    // --- ROBUST SCRIPT LOADER ---
    // This ensures Plotly is loaded even if Hugo strips the static tag
    function loadPlotlyAndInit_linear_equation_grapher() {
        if (typeof Plotly !== 'undefined') {
            initCalculator_linear_equation_grapher();
        } else {
            const status = document.getElementById('loading_status_linear_equation_grapher');
            if(status) status.style.display = 'block';

            const script = document.createElement('script');
            script.src = "https://cdn.plot.ly/plotly-2.24.1.min.js";
            script.onload = function() {
                if(status) status.style.display = 'none';
                initCalculator_linear_equation_grapher();
            };
            script.onerror = function() {
                if(status) status.innerHTML = "Error: Could not load graphing library.";
            };
            document.head.appendChild(script);
        }
    }

    // Entry point
    window.addEventListener('load', loadPlotlyAndInit_linear_equation_grapher);

    function initCalculator_linear_equation_grapher() {
        // Initialize with two lines
        addLine_linear_equation_grapher(); 
        addLine_linear_equation_grapher();
        renderHistory_linear_equation_grapher();
        
        // Pre-fill inputs
        setTimeout(() => {
            const inputs = document.querySelectorAll('#lines_container_linear_equation_grapher input');
            if(inputs.length >= 4) {
                inputs[0].value = 2;   
                inputs[1].value = 1;   
                inputs[2].value = -0.5;
                inputs[3].value = 4;   
                calculate_linear_equation_grapher(); 
            }
        }, 200);
    }

    function addLine_linear_equation_grapher() {
        const container = document.getElementById('lines_container_linear_equation_grapher');
        const id = lineCount_linear_equation_grapher++;
        
        const div = document.createElement('div');
        div.className = 'line-input-row';
        div.id = 'line_row_' + id;
        
        // TIGHTER LAYOUT STRUCTURE
        div.innerHTML = `
            <div class="eq-group">
                <span class="eq-text y-equals">y =</span>
                <input type="number" class="eq-input" placeholder="m" step="any">
                <span class="eq-text">x +</span>
                <input type="number" class="eq-input" placeholder="b" step="any">
            </div>
            <button onclick="removeLine_linear_equation_grapher(${id})" class="btn-remove" title="Remove Line">×</button>
        `;
        container.appendChild(div);
    }

    function removeLine_linear_equation_grapher(id) {
        const row = document.getElementById('line_row_' + id);
        if(row) row.remove();
        calculate_linear_equation_grapher(); 
    }

    function calculate_linear_equation_grapher() {
        
    const containerId = 'lines_container_linear_equation_grapher';
    const graphId = 'graph_linear_equation_grapher';

    // 1. Gather all active inputs
    let lines = [];
    const container = document.getElementById(containerId);
    if(!container) return; 
    
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
                    
                    if (x_int < minX) minX = x_int - 5;
                    if (x_int > maxX) maxX = x_int + 5;
                    if (y_int < minY) minY = y_int - 5;
                    if (y_int > maxY) maxY = y_int + 5;

                    analysisHTML += `<li>L${i+1} & L${j+1}: <span style="color:#28a745;">(${x_int.toFixed(2)}, ${y_int.toFixed(2)})</span></li>`;
                } else {
                    analysisHTML += `<li>L${i+1} & L${j+1}: Parallel</li>`;
                }
            }
        }
        analysisHTML += "</ul>";
    }
    
    if(lines.length === 0) {
        analysisHTML = "Please enter values for Slope (m) and Y-Intercept (b).";
    }

    // 3. Generate Plot Data
    let plotData = [];
    
    lines.forEach((line, index) => {
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
        xaxis: { title: 'X Axis', zerolinecolor: '#666', gridcolor: '#333', range: [minX, maxX] },
        yaxis: { title: 'Y Axis', zerolinecolor: '#666', gridcolor: '#333', range: [minY, maxY] },
        showlegend: true,
        legend: { x: 0, y: 1.1, orientation: "h", font: {size: 10} },
        margin: { t: 40, b: 40, l: 40, r: 20 },
        hovermode: 'closest'
    };
    
    if (typeof Plotly !== 'undefined') {
        Plotly.newPlot(graphId, plotData, layout, {displayModeBar: false, responsive: true});
    } else {
        document.getElementById(graphId).innerHTML = "<p style='padding:20px; color:#ffcc00;'>Graphing engine is loading, please wait...</p>";
    }

    var resultText = analysisHTML;
    
    // UPDATED HISTORY TEXT
    // Now saves actual coordinates (e.g., "(2.00, 4.00), (-1.50, 3.20)") instead of just "2 Intersections"
    var historyText = (intersections.length > 0) ? intersections.map(p => p.label).join(", ") : "Graph Updated";

        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        if(resultText) resBox.style.display = 'block';
        
        if (historyText && historyText !== "Graph Updated") addToHistory_linear_equation_grapher(historyText);
    }

    function addToHistory_linear_equation_grapher(item) {
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_linear_equation_grapher)) || [];
        // Prevent duplicate consecutive entries
        if (history.length === 0 || history[0] !== item) {
            history.unshift(item);
            if (history.length > 5) history.pop();
            localStorage.setItem(STORAGE_KEY_linear_equation_grapher, JSON.stringify(history));
            renderHistory_linear_equation_grapher();
        }
    }

    function renderHistory_linear_equation_grapher() {
        const list = document.getElementById('history_list_linear_equation_grapher');
        if(!list) return;
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_linear_equation_grapher)) || [];
        list.innerHTML = history.map(item => `<li>${item}</li>`).join('');
    }

    function clearHistory_linear_equation_grapher() {
        localStorage.removeItem(STORAGE_KEY_linear_equation_grapher);
        renderHistory_linear_equation_grapher();
    }

    function downloadHistory_linear_equation_grapher() {
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_linear_equation_grapher)) || [];
        if (history.length === 0) {
            alert("No history to download.");
            return;
        }

        // 1. Prepare Content
        let content = "CalcFoundry - Linear Equation Grapher History\n";
        content += "Date: " + new Date().toLocaleDateString() + "\n";
        content += "-----------------------------------\n\n";
        
        history.forEach(item => {
            // Remove HTML tags for clean text file
            let cleanItem = item.replace(/<[^>]*>?/gm, '');
            content += cleanItem + "\n";
        });

        // 2. Create Blob
        const blob = new Blob([content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);

        // 3. Trigger Download
        const a = document.createElement('a');
        a.href = url;
        a.download = "Linear_Equation_Grapher_History_" + new Date().toISOString().slice(0,10) + ".txt";
        document.body.appendChild(a);
        a.click();
        
        // 4. Cleanup
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
</script>

<style>
  /* MAIN LAYOUT */
  .calc-grid { display: grid; gap: 20px; grid-template-columns: 1fr; }
  @media (min-width: 900px) { .calc-grid { grid-template-columns: 2fr 1fr; } }
  
  .calc-main { background: #1e1e1e; padding: 20px; border-radius: 8px; border: 1px solid #333; }
  
  /* INPUT ROWS - FIXED FOR HORIZONTAL LAYOUT */
  .lines-container { display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; }
  
  .line-input-row { 
      display: flex; 
      align-items: center; 
      justify-content: space-between; 
      background: #2d2d2d; 
      padding: 8px 12px; 
      border-radius: 6px; 
      border-left: 4px solid #007bff;
      flex-wrap: nowrap; /* Prevent wrapping */
  }
  
  .eq-group { 
      display: flex; 
      align-items: center; 
      flex: 1; 
      white-space: nowrap; /* Keep text on one line */
      overflow-x: auto; /* Handle overflow gracefully on tiny screens */
  }

  .eq-text { 
      font-weight: bold; 
      font-family: monospace; 
      font-size: 1.1em; 
      color: #ddd; 
      margin: 0 8px; /* Breathing room for text */
  }
  .y-equals { color: #007bff; margin-left: 0; }
  
  /* INPUT FIELDS - SMALLER */
  .eq-input { 
      width: 55px; /* Significantly smaller width */
      padding: 6px; 
      background: #111; 
      border: 1px solid #444; 
      color: white; 
      border-radius: 4px; 
      text-align: center;
      min-width: 50px;
  }
  .eq-input:focus { border-color: #007bff; outline: none; }

  /* BUTTONS */
  .button-row { display: flex; gap: 10px; margin-bottom: 20px; }
  
  .btn-primary { flex: 2; padding: 12px; background: #007bff; color: white; border: none; cursor: pointer; border-radius: 4px; font-weight: bold; transition: background 0.2s; }
  .btn-primary:hover { background: #0056b3; }
  
  .btn-secondary { flex: 1; padding: 12px; background: #444; color: white; border: none; cursor: pointer; border-radius: 4px; transition: background 0.2s; }
  .btn-secondary:hover { background: #555; }

  .btn-remove { 
      flex: 0 0 24px;
      height: 24px; 
      background: #dc3545; 
      color: white; 
      border: none; 
      border-radius: 4px; 
      cursor: pointer; 
      display: flex; 
      align-items: center; 
      justify-content: center; 
      font-weight: bold;
      margin-left: 10px;
  }
  .btn-remove:hover { background: #a71d2a; }

  /* GRAPH CONTAINER */
  .graph-box { 
      width: 100%; 
      height: 450px; 
      background: #111; 
      border: 1px solid #444; 
      border-radius: 4px;
  }
  
  .result-box { margin-top: 20px; padding: 15px; background: #2d2d2d; border-left: 4px solid #28a745; }
  
  /* HISTORY */
  .calc-history { background: #252526; padding: 15px; border-radius: 8px; font-size: 0.9em; height: fit-content; }
  .calc-history h4 { margin-top: 0; border-bottom: 1px solid #444; padding-bottom: 5px; color: #ddd; }
  .calc-history ul { padding-left: 20px; color: #bbb; margin: 0; }
  .calc-history li { margin-bottom: 5px; }
  
  /* UPDATED BUTTON STYLE TO MATCH BMI CALCULATOR */
  .btn-small { background: #444; font-size: 0.8em; padding: 8px 10px; margin-top: 0; color: white; border: 1px solid #555; cursor:pointer; border-radius: 4px; }
  .btn-small:hover { background: #555; }
</style>

{{< /calculator >}}

## How to Use

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


## The Math Behind It
We calculate properties using the standard Slope-Intercept form:

$$
y = mx + b \quad \bigg| \quad x_{int} = \frac{b_2 - b_1}{m_1 - m_2}
$$

**Where:**

* $m$ is the **Slope** (Rise over Run).
* $b$ is the **Y-Intercept** (where the line crosses the vertical axis).
* $x_{int}$ is the x-coordinate of the **Intersection**.

