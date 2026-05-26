---
title: "Quadratic Equation Solver"
date: 2026-05-26
categories: ["Math"]
summary: "Solve quadratic equations of the form ax² + bx + c = 0. Calculate real and complex roots, vertex coordinates, and plot key characteristics."
math: true
disableSpecial1stPost: true
---

Solve quadratic equations of the form ax² + bx + c = 0. Calculate real and complex roots, vertex coordinates, and plot key characteristics.

{{< calculator >}}

<div class="calc-grid">
  <div class="calc-main">
    
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

    <button onclick="calculate_quadratic_equation_solver()">Solve Equation</button>
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
    <ul id="history_list_quadratic_equation_solver"></ul>
    
    <div style="display:flex; gap:10px; margin-top:10px;">
        <button onclick="downloadHistory_quadratic_equation_solver()" class="btn-small" style="flex:1;">Save</button>
        <button onclick="clearHistory_quadratic_equation_solver()" class="btn-small" style="flex:1;">Clear</button>
    </div>
  </div>
</div>

<script>
    const STORAGE_KEY_quadratic_equation_solver = "calcfoundry_history_quadratic_equation_solver"; 

    window.onload = function() { renderHistory_quadratic_equation_solver(); };

    function calculate_quadratic_equation_solver() {
        
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

        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        resBox.style.display = 'block';
        if(historySummary) addToHistory_quadratic_equation_solver(historySummary);
    }

    function addToHistory_quadratic_equation_solver(item) {
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_quadratic_equation_solver)) || [];
        if (history.length === 0 || history[0] !== item) {
            history.unshift(item);
            if (history.length > 10) history.pop();
            localStorage.setItem(STORAGE_KEY_quadratic_equation_solver, JSON.stringify(history));
            renderHistory_quadratic_equation_solver();
        }
    }

    function renderHistory_quadratic_equation_solver() {
        const list = document.getElementById('history_list_quadratic_equation_solver');
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_quadratic_equation_solver)) || [];
        list.innerHTML = history.map(item => `<li>${item}</li>`).join('');
    }

    function clearHistory_quadratic_equation_solver() {
        localStorage.removeItem(STORAGE_KEY_quadratic_equation_solver);
        renderHistory_quadratic_equation_solver();
    }

    function downloadHistory_quadratic_equation_solver() {
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_quadratic_equation_solver)) || [];
        if (history.length === 0) {
            alert("No history to download.");
            return;
        }

        let content = "CalcFoundry - Quadratic Equation Solver History\n";
        content += "Date: " + new Date().toLocaleDateString() + "\n";
        content += "-----------------------------------\n\n";
        
        history.forEach(item => {
            let cleanItem = item.replace(/<[^>]*>?/gm, '');
            content += cleanItem + "\n";
        });

        const blob = new Blob([content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "Quadratic_Equation_Solver_History.txt";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
</script>

<style>
  .calc-grid { display: grid; gap: 20px; grid-template-columns: 1fr; }
  @media (min-width: 768px) { .calc-grid { grid-template-columns: 2fr 1fr; } }
  .calc-history { background: #252526; padding: 15px; border-radius: 8px; font-size: 0.9em; }
  .calc-history h4 { margin-top: 0; border-bottom: 1px solid #444; padding-bottom: 5px; }
  .calc-history ul { padding-left: 20px; color: #bbb; }
  .btn-small { background: #444; font-size: 0.8em; padding: 8px 10px; margin-top: 0; color: white; border: 1px solid #555; cursor:pointer; border-radius: 4px; }
  .btn-small:hover { background: #555; }
  
  .calc-main label { display: block; margin-top: 10px; font-weight: bold; }
  .calc-main input, .calc-main select { width: 100%; padding: 8px; margin-top: 5px; background: #333; border: 1px solid #555; color: white; }
  .calc-main button { margin-top: 20px; width: 100%; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }
  .calc-main button:hover { background: #0056b3; }
  .row-inputs div { flex: 1; }
</style>

{{< /calculator >}}

## How to Use This Calculator

### Understanding Quadratic Equations
A quadratic equation is a second-order polynomial equation in a single variable. The graph of a quadratic function is a **parabola**, a U-shaped curve that opens either upward or downward.

### Parabola Features
1. **The Discriminant ($D = b^2 - 4ac$):**
   - If $D > 0$: The parabola crosses the x-axis at two distinct points (two real roots).
   - If $D = 0$: The parabola touches the x-axis at exactly one point (one real repeated root).
   - If $D < 0$: The parabola does not touch the x-axis, and its roots are complex conjugate pairs.
2. **The Vertex ($h, k$):** The peak or trough of the parabola. It represents the maximum or minimum value of the quadratic function.
3. **Leading Coefficient ($a$):** Determines the width of the parabola and its direction. If $a$ is positive, it opens upward. If $a$ is negative, it opens downward.


## The Math Behind It
The tool uses the following mathematical principle:

$$
x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}
$$

**Where:**


* $x$ is the **unknown variable** we are solving for.
* $a$ is the **quadratic coefficient** ($a 
eq 0$).
* $b$ is the **linear coefficient**.
* $c$ is the **constant term**.

