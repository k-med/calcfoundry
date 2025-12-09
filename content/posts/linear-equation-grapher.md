---
title: "Linear Equation Grapher"
date: 2025-12-09
categories: ["Algebra"]
summary: "Plot multiple linear equations (y=mx+b), find intersection points, and calculate x/y intercepts instantly with interactive graphs."
math: true
disableSpecial1stPost: true
---

<script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>

Plot multiple linear equations (y=mx+b), find intersection points, and calculate x/y intercepts instantly with interactive graphs.

{{< calculator >}}

<div class="calc-grid">
  <div class="calc-main">
    <div id="lines_container_linear_equation_grapher">
        </div>
    
    <div style="display: flex; gap: 10px; margin-top: 10px;">
        <button onclick="addLine_linear_equation_grapher()" class="btn-secondary">+ Add Line</button>
        <button onclick="calculate_linear_equation_grapher()" class="btn-primary">Plot & Solve</button>
    </div>

    <div id="graph_linear_equation_grapher" style="width:100%; height:400px; margin-top:20px; border: 1px solid #444;"></div>

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
    <ul id="history_list_linear_equation_grapher"></ul>
    <button onclick="clearHistory_linear_equation_grapher()" class="btn-small">Clear Log</button>
  </div>
</div>

<script>
    const STORAGE_KEY_linear_equation_grapher = "calcfoundry_history_linear_equation_grapher"; 
    let lineCount_linear_equation_grapher = 0;

    window.onload = function() { 
        // Initialize with two lines by default
        addLine_linear_equation_grapher(); 
        addLine_linear_equation_grapher();
        renderHistory_linear_equation_grapher();
        
        // Pre-fill some example data
        document.getElementById('m_0').value = 2;
        document.getElementById('b_0').value = 1;
        document.getElementById('m_1').value = -0.5;
        document.getElementById('b_1').value = 4;
        
        calculate_linear_equation_grapher(); // Initial plot
    };

    function addLine_linear_equation_grapher() {
        const container = document.getElementById('lines_container_linear_equation_grapher');
        const id = lineCount_linear_equation_grapher++;
        
        const div = document.createElement('div');
        div.className = 'line-input-row';
        div.id = 'line_row_' + id;
        div.innerHTML = `
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-weight:bold; color:#007bff;">y = </span>
                <input type="number" id="m_${id}" placeholder="m (Slope)" step="any" style="flex:1;">
                <span style="font-weight:bold;">x + </span>
                <input type="number" id="b_${id}" placeholder="b (Y-Intercept)" step="any" style="flex:1;">
                <button onclick="removeLine_linear_equation_grapher(${id})" class="btn-remove" title="Remove Line">×</button>
            </div>
        `;
        container.appendChild(div);
    }

    function removeLine_linear_equation_grapher(id) {
        const row = document.getElementById('line_row_' + id);
        if(row) row.remove();
    }

    function calculate_linear_equation_grapher() {
        
    // 1. Gather all active inputs
    let lines = [];
    const container = document.getElementById('lines_container_' + tool_id);
    const rows = container.getElementsByClassName('line-input-row');
    
    for (let row of rows) {
        let inputs = row.getElementsByTagName('input');
        let m = parseFloat(inputs[0].value);
        let b = parseFloat(inputs[1].value);
        
        if (!isNaN(m) && !isNaN(b)) {
            lines.push({m: m, b: b, eq: `y = ${m}x + ${b}`});
        }
    }

    if (lines.length === 0) {
        document.getElementById('result_val').innerText = "Please add at least one valid line.";
        return;
    }

    // 2. Prepare Plot Data
    let plotData = [];
    let xRange = [-10, 10]; // Default range
    
    // Generate points for each line
    lines.forEach((line, index) => {
        let xValues = [xRange[0], xRange[1]];
        let yValues = [line.m * xRange[0] + line.b, line.m * xRange[1] + line.b];
        
        plotData.push({
            x: xValues,
            y: yValues,
            mode: 'lines',
            name: `Line ${index + 1}: y=${line.m}x + ${line.b}`,
            line: { width: 3 }
        });
    });

    // 3. Calculate Intersections & Properties
    let analysisHTML = "";
    let intersections = [];

    // Analyze individual lines
    analysisHTML += "<strong>Properties:</strong><br><ul style='font-size:0.9em; margin-bottom:10px;'>";
    lines.forEach((l, i) => {
        let xInt = (l.m !== 0) ? (-l.b / l.m).toFixed(2) : "None (Horizontal)";
        let yInt = l.b;
        analysisHTML += `<li>Line ${i+1}: X-Int at ${xInt}, Y-Int at ${yInt}</li>`;
    });
    analysisHTML += "</ul>";

    // Analyze intersections between pairs
    if (lines.length > 1) {
        analysisHTML += "<strong>Intersections:</strong><br><ul style='font-size:0.9em;'>";
        for (let i = 0; i < lines.length; i++) {
            for (let j = i + 1; j < lines.length; j++) {
                let l1 = lines[i];
                let l2 = lines[j];
                
                if (l1.m === l2.m) {
                     analysisHTML += `<li>L${i+1} & L${j+1}: Parallel (No intersection)</li>`;
                } else {
                    // m1*x + b1 = m2*x + b2  =>  x(m1 - m2) = b2 - b1
                    let x_int = (l2.b - l1.b) / (l1.m - l2.m);
                    let y_int = l1.m * x_int + l1.b;
                    
                    let ptStr = `(${x_int.toFixed(2)}, ${y_int.toFixed(2)})`;
                    analysisHTML += `<li>L${i+1} & L${j+1} intersect at <span style="color:#28a745; font-weight:bold;">${ptStr}</span></li>`;
                    intersections.push({x: x_int, y: y_int, label: `Int: L${i+1}-L${j+1}`});
                }
            }
        }
        analysisHTML += "</ul>";
    }

    // Add intersection points to plot
    if (intersections.length > 0) {
        plotData.push({
            x: intersections.map(p => p.x),
            y: intersections.map(p => p.y),
            mode: 'markers',
            type: 'scatter',
            name: 'Intersections',
            marker: { size: 10, color: 'red' },
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
        legend: { x: 0, y: 1.2, orientation: "h" },
        margin: { t: 30, b: 40, l: 50, r: 20 }
    };

    Plotly.newPlot('graph_' + tool_id, plotData, layout, {displayModeBar: false});

    var resultText = analysisHTML;
    var historyText = (intersections.length > 0) ? `${intersections.length} Intersection(s) found` : "Lines Plotted";

        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        resBox.style.display = 'block';
        
        // Only add to history if we have intersections
        if (historyText) addToHistory_linear_equation_grapher(historyText);
    }

    function addToHistory_linear_equation_grapher(item) {
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_linear_equation_grapher)) || [];
        history.unshift(item);
        if (history.length > 5) history.pop();
        localStorage.setItem(STORAGE_KEY_linear_equation_grapher, JSON.stringify(history));
        renderHistory_linear_equation_grapher();
    }

    function renderHistory_linear_equation_grapher() {
        const list = document.getElementById('history_list_linear_equation_grapher');
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_linear_equation_grapher)) || [];
        list.innerHTML = history.map(item => `<li>${item}</li>`).join('');
    }

    function clearHistory_linear_equation_grapher() {
        localStorage.removeItem(STORAGE_KEY_linear_equation_grapher);
        renderHistory_linear_equation_grapher();
    }
</script>

<style>
  .calc-grid { display: grid; gap: 20px; grid-template-columns: 1fr; }
  @media (min-width: 768px) { .calc-grid { grid-template-columns: 2fr 1fr; } }
  .calc-history { background: #252526; padding: 15px; border-radius: 8px; font-size: 0.9em; }
  .calc-history h4 { margin-top: 0; border-bottom: 1px solid #444; padding-bottom: 5px; }
  .calc-history ul { padding-left: 20px; color: #bbb; }
  .btn-small { background: #444; font-size: 0.8em; padding: 5px 10px; margin-top: 10px; border:none; color:white; cursor:pointer; }
  
  .calc-main { background: #1e1e1e; padding: 15px; border-radius: 8px; }
  .line-input-row { background: #2d2d2d; padding: 10px; margin-bottom: 10px; border-radius: 4px; border-left: 3px solid #007bff; }
  
  .calc-main input { background: #333; border: 1px solid #555; color: white; padding: 5px; border-radius: 3px; }
  
  .btn-primary { width: 100%; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; border-radius: 4px; font-weight:bold; }
  .btn-primary:hover { background: #0056b3; }
  
  .btn-secondary { width: 100%; padding: 10px; background: #444; color: white; border: none; cursor: pointer; border-radius: 4px; }
  .btn-secondary:hover { background: #555; }

  .btn-remove { background: #ff4444; color: white; border: none; width: 25px; height: 25px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-weight: bold; }
  
  .result-box { margin-top: 20px; padding: 15px; background: #2d2d2d; border-left: 4px solid #28a745; }
</style>

{{< /calculator >}}

## How to Use

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


## The Math Behind It
We calculate properties using the standard Slope-Intercept form:

$$
y = mx + b \quad \bigg| \quad x_{int} = \frac{b_2 - b_1}{m_1 - m_2}
$$

**Where:**

* $m$ is the **Slope** (Rise over Run).
* $b$ is the **Y-Intercept** (where the line crosses the vertical axis).
* $x_{int}$ is the x-coordinate of the **Intersection**.

