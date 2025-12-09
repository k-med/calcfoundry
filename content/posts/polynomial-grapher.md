---
title: "Polynomial Grapher"
date: 2025-12-09
categories: ["Algebra"]
summary: "Plot and analyze Quadratic, Cubic, and Quartic functions. Automatically calculates vertex and roots for parabolas."
math: true
disableSpecial1stPost: true
---

Plot and analyze Quadratic, Cubic, and Quartic functions. Automatically calculates vertex and roots for parabolas.

{{< calculator >}}

<div class="calc-grid">
  <div class="calc-main">
    
    <div id="loading_status_polynomial_grapher" style="display:none; color: #888; font-size: 0.8em; margin-bottom: 5px;">Loading Graph Engine...</div>

    <div id="polys_container_polynomial_grapher" class="lines-container">
        </div>
    
    <div class="button-row">
        <button onclick="addPoly_polynomial_grapher()" class="btn-secondary">+ Add Function</button>
        <button onclick="calculate_polynomial_grapher()" class="btn-primary">Plot & Analyze</button>
    </div>

    <div id="graph_polynomial_grapher" class="graph-box"></div>

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
    <ul id="history_list_polynomial_grapher"></ul>
    <button onclick="clearHistory_polynomial_grapher()" class="btn-small">Clear Log</button>
  </div>
</div>

<script>
    const STORAGE_KEY_polynomial_grapher = "calcfoundry_poly_polynomial_grapher"; 
    let polyCount_polynomial_grapher = 0;

    // --- ROBUST SCRIPT LOADER ---
    function loadPlotlyAndInit_polynomial_grapher() {
        if (typeof Plotly !== 'undefined') {
            initCalculator_polynomial_grapher();
        } else {
            const status = document.getElementById('loading_status_polynomial_grapher');
            if(status) status.style.display = 'block';

            const script = document.createElement('script');
            script.src = "https://cdn.plot.ly/plotly-2.24.1.min.js";
            script.onload = function() {
                if(status) status.style.display = 'none';
                initCalculator_polynomial_grapher();
            };
            script.onerror = function() {
                if(status) status.innerHTML = "Error: Could not load graphing library.";
            };
            document.head.appendChild(script);
        }
    }

    // Entry point
    window.addEventListener('load', loadPlotlyAndInit_polynomial_grapher);

    function initCalculator_polynomial_grapher() {
        // Initialize with one Quadratic by default
        addPoly_polynomial_grapher(2); 
        renderHistory_polynomial_grapher();
        
        // Pre-fill inputs for a nice parabola
        setTimeout(() => {
            const inputs = document.querySelectorAll('#polys_container_polynomial_grapher input');
            if(inputs.length >= 3) {
                inputs[0].value = 1;   // a
                inputs[1].value = -2;  // b
                inputs[2].value = -3;  // c
                calculate_polynomial_grapher(); 
            }
        }, 200);
    }

    function addPoly_polynomial_grapher(defaultDegree = 2) {
        const container = document.getElementById('polys_container_polynomial_grapher');
        const id = polyCount_polynomial_grapher++;
        
        const div = document.createElement('div');
        div.className = 'line-input-row';
        div.id = 'poly_row_' + id;
        
        // Header with Degree Selector
        // The inputs container will be populated by changeDegree_polynomial_grapher
        div.innerHTML = `
            <div style="width:100%;">
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                    <select id="degree_select_${id}" class="degree-select" onchange="updateInputs_polynomial_grapher(${id})">
                        <option value="1">Degree 1 (Linear)</option>
                        <option value="2" selected>Degree 2 (Quadratic)</option>
                        <option value="3">Degree 3 (Cubic)</option>
                        <option value="4">Degree 4 (Quartic)</option>
                    </select>
                    <button onclick="removePoly_polynomial_grapher(${id})" class="btn-remove" title="Remove">×</button>
                </div>
                <div id="inputs_area_${id}" class="eq-group"></div>
            </div>
        `;
        container.appendChild(div);
        
        // Trigger initial input build
        // Manually set value if default passed
        if(defaultDegree) document.getElementById(`degree_select_${id}`).value = defaultDegree;
        updateInputs_polynomial_grapher(id);
    }

    function updateInputs_polynomial_grapher(id) {
        const degree = parseInt(document.getElementById(`degree_select_${id}`).value);
        const area = document.getElementById(`inputs_area_${id}`);
        let html = '<span class="eq-text y-equals">y =</span>';
        
        // Generates inputs like [ ]x^2 + [ ]x + [ ]
        const coeffs = ['e','d','c','b','a']; // generic
        // We only need 'degree + 1' coefficients
        // For Deg 2: ax^2 + bx + c
        
        for(let i=degree; i>=0; i--) {
            // Add symbol if not first term
            if(i < degree) html += '<span class="eq-text">+</span>';
            
            html += `<input type="number" class="eq-input" data-power="${i}" placeholder="0" step="any">`;
            
            if(i > 1) html += `<span class="eq-text">x<sup>${i}</sup></span>`;
            else if (i === 1) html += `<span class="eq-text">x</span>`;
        }
        
        area.innerHTML = html;
    }

    function removePoly_polynomial_grapher(id) {
        const row = document.getElementById('poly_row_' + id);
        if(row) row.remove();
        calculate_polynomial_grapher(); 
    }

    function calculate_polynomial_grapher() {
        
    const containerId = 'polys_container_polynomial_grapher';
    const graphId = 'graph_polynomial_grapher';

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
    // We scan a default range, but we might want to center on the Vertex for quadratics
    let minX = -10, maxX = 10;
    
    // Auto-center logic for Quadratics (find vertex x = -b/2a)
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
    let step = (maxX - minX) / 200; // Resolution

    polynomials.forEach((poly, index) => {
        let xVals = [];
        let yVals = [];
        
        for(let x = minX; x <= maxX; x += step) {
            let y = 0;
            // Evaluate polynomial y = ax^n + ...
            for(let pow in poly.coeffs) {
                y += poly.coeffs[pow] * Math.pow(x, pow);
            }
            xVals.push(x);
            yVals.push(y);
        }
        
        // Name generation: "2x^2 - 4x + 1"
        let name = "";
        let powers = Object.keys(poly.coeffs).sort((a,b) => b-a);
        powers.forEach((pow, i) => {
            let val = poly.coeffs[pow];
            if(val === 0 && powers.length > 1) return; // Skip 0 terms
            
            let sign = (val >= 0 && i > 0) ? " + " : " ";
            if(val < 0) sign = " - ";
            
            let absVal = Math.abs(val);
            // Don't show "1" if it's 1x^2, unless it's just "1" (const)
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

    // 3. Analysis (Focus on Quadratic Roots/Vertex)
    let analysisHTML = "";
    let historyText = "";

    polynomials.forEach((p, i) => {
        if(p.degree === 2) {
            let a = p.coeffs[2];
            let b = p.coeffs[1];
            let c = p.coeffs[0];
            
            // Vertex
            let h = -b / (2*a);
            let k = (a*h*h) + (b*h) + c;
            
            // Discriminant
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
    // historyText is set inside the loop

        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        if(resultText) resBox.style.display = 'block';
        
        // Log analysis if available
        if (historyText) addToHistory_polynomial_grapher(historyText);
    }

    function addToHistory_polynomial_grapher(item) {
        // Only log if it contains meaningful data (like Vertex info)
        if(!item.includes("Vertex")) return;

        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_polynomial_grapher)) || [];
        // Avoid duplicate logging of same calculation
        if (history.length === 0 || history[0] !== item) {
            history.unshift(item);
            if (history.length > 5) history.pop();
            localStorage.setItem(STORAGE_KEY_polynomial_grapher, JSON.stringify(history));
            renderHistory_polynomial_grapher();
        }
    }

    function renderHistory_polynomial_grapher() {
        const list = document.getElementById('history_list_polynomial_grapher');
        if(!list) return;
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_polynomial_grapher)) || [];
        list.innerHTML = history.map(item => `<li>${item}</li>`).join('');
    }

    function clearHistory_polynomial_grapher() {
        localStorage.removeItem(STORAGE_KEY_polynomial_grapher);
        renderHistory_polynomial_grapher();
    }
</script>

<style>
  /* MAIN LAYOUT */
  .calc-grid { display: grid; gap: 20px; grid-template-columns: 1fr; }
  @media (min-width: 900px) { .calc-grid { grid-template-columns: 2fr 1fr; } }
  
  .calc-main { background: #1e1e1e; padding: 20px; border-radius: 8px; border: 1px solid #333; }
  
  /* INPUT ROWS */
  .lines-container { display: flex; flex-direction: column; gap: 10px; margin-bottom: 20px; }
  
  .line-input-row { 
      background: #2d2d2d; 
      padding: 12px; 
      border-radius: 6px; 
      border-left: 4px solid #9c27b0; /* Purple for Polynomials */
  }
  
  .degree-select {
      background: #444; color: #ddd; border: 1px solid #555; padding: 2px 5px; border-radius: 3px; font-size: 0.85em;
  }

  .eq-group { 
      display: flex; 
      align-items: center; 
      flex-wrap: wrap; /* Allow wrapping for long polynomials */
      margin-top: 8px;
  }

  .eq-text { 
      font-weight: bold; 
      font-family: monospace; 
      font-size: 1.1em; 
      color: #ddd; 
      margin: 0 4px; 
  }
  .y-equals { color: #9c27b0; margin-left: 0; margin-right: 8px; }
  
  /* INPUT FIELDS */
  .eq-input { 
      width: 50px; 
      padding: 6px; 
      background: #111; 
      border: 1px solid #444; 
      color: white; 
      border-radius: 4px; 
      text-align: center;
  }
  .eq-input:focus { border-color: #9c27b0; outline: none; }

  /* BUTTONS */
  .button-row { display: flex; gap: 10px; margin-bottom: 20px; }
  
  .btn-primary { flex: 2; padding: 12px; background: #9c27b0; color: white; border: none; cursor: pointer; border-radius: 4px; font-weight: bold; transition: background 0.2s; }
  .btn-primary:hover { background: #7b1fa2; }
  
  .btn-secondary { flex: 1; padding: 12px; background: #444; color: white; border: none; cursor: pointer; border-radius: 4px; transition: background 0.2s; }
  .btn-secondary:hover { background: #555; }

  .btn-remove { 
      background: #dc3545; color: white; border: none; border-radius: 3px; 
      cursor: pointer; padding: 2px 8px; font-weight: bold; font-size: 0.9em;
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
  .calc-history li { margin-bottom: 8px; line-height: 1.4; }
  .btn-small { background: #444; font-size: 0.8em; padding: 5px 10px; margin-top: 15px; border:none; color:white; cursor:pointer; width: 100%; border-radius: 4px; }
</style>

{{< /calculator >}}

## How to Use

### Graphing Polynomials
This tool allows you to visualize functions of higher degrees. While a linear equation ($y=mx+b$) produces a straight line, higher-order polynomials produce curves with peaks and valleys.

### Degrees Explained
* **Degree 1 (Linear):** A straight line.
* **Degree 2 (Quadratic):** A Parabola (U-shape). This calculator will automatically find the **Vertex** (the turning point) and the **Roots** (where it crosses the x-axis).
* **Degree 3 (Cubic):** An S-shaped curve that can have up to two turning points.
* **Degree 4 (Quartic):** A W-shaped or M-shaped curve with up to three turning points.


## The Math Behind It
Standard Polynomial Form:

$$
P(x) = a_n x^n + a_{n-1} x^{n-1} + \dots + a_1 x + a_0
$$

**Where:**

* $n$ is the **Degree** (highest power).
* $a_n$ are the **Coefficients** (the numbers in front of the variables).

