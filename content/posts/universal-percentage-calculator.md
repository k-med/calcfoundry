---
title: "Universal Percentage Calculator"
date: 2025-12-08
categories: ["Math"]
summary: "The only percentage tool you need. Calculate percentage increases, find parts of a whole, and solve 'X is what percent of Y' problems instantly."
math: true
disableSpecial1stPost: true
---

The only percentage tool you need. Calculate percentage increases, find parts of a whole, and solve 'X is what percent of Y' problems instantly.

{{< calculator >}}

<div class="calc-grid">
  <div class="calc-main">
    
<label>What do you want to calculate?</label>
<select id="calc_mode" onchange="updateLabels_universal_percentage_calculator()">
    <option value="percent_of">Percentage of a Number (e.g., 20% of 150)</option>
    <option value="what_percent">What % is X of Y? (e.g., 5 is what % of 20?)</option>
    <option value="percent_change">Percentage Increase/Decrease</option>
</select>

<label id="label_a">Percentage (%)</label>
<input type="number" id="input_a" placeholder="Enter first value">

<label id="label_b">Total Value</label>
<input type="number" id="input_b" placeholder="Enter second value">

    <button onclick="calculate_universal_percentage_calculator()">Calculate</button>
    <div id="result_box" class="result-box" style="display:none;">
        <span id="result_val"></span>
    </div>
    
    <div style="margin-top: 15px; text-align: center; font-size: 0.85em;">
        <a href="#the-math-behind-it" style="color: #888; text-decoration: underline; cursor: pointer;">
            How does this work?
        </a>
    </div>
  </div>

  <div class="calc-history">
    <h4>History</h4>
    <ul id="history_list_universal_percentage_calculator"></ul>
    <button onclick="clearHistory_universal_percentage_calculator()" class="btn-small">Clear History</button>
  </div>
</div>

<script>
    const STORAGE_KEY_universal_percentage_calculator = "calcfoundry_history_universal_percentage_calculator"; 

    window.onload = function() { 
        renderHistory_universal_percentage_calculator();
        // Trigger label update on load
        updateLabels_universal_percentage_calculator(); 
    };

    // Dynamic Label Switching Logic
    function updateLabels_universal_percentage_calculator() {
        const mode = document.getElementById('calc_mode').value;
        const lblA = document.getElementById('label_a');
        const lblB = document.getElementById('label_b');
        
        if (mode === 'percent_of') {
            lblA.innerText = "Percentage (%)";
            lblB.innerText = "Total Value";
        } else if (mode === 'what_percent') {
            lblA.innerText = "Part Value";
            lblB.innerText = "Total Value";
        } else if (mode === 'percent_change') {
            lblA.innerText = "Old Value";
            lblB.innerText = "New Value";
        }
    }

    function calculate_universal_percentage_calculator() {
        
    const mode = document.getElementById('calc_mode').value;
    const valA = parseFloat(document.getElementById('input_a').value);
    const valB = parseFloat(document.getElementById('input_b').value);

    let result = 0;
    let resultText = "";
    let historyText = "";

    if (isNaN(valA) || isNaN(valB)) {
        resultText = "Please enter valid numbers in both fields.";
        historyText = "Invalid Input";
    } else {
        if (mode === 'percent_of') {
            // Logic: What is A% of B?
            result = (valA / 100) * valB;
            resultText = `
                <strong>Result:</strong> <span style="color:#4caf50; font-size:1.4em;">${result.toLocaleString()}</span><br>
                <small>${valA}% of ${valB} is ${result}</small>
            `;
            historyText = `${valA}% of ${valB} = ${result}`;
        } 
        else if (mode === 'what_percent') {
            // Logic: A is what % of B?
            if (valB === 0) {
                resultText = "Cannot divide by zero.";
                historyText = "Error";
            } else {
                result = (valA / valB) * 100;
                resultText = `
                    <strong>Result:</strong> <span style="color:#4caf50; font-size:1.4em;">${result.toFixed(2)}%</span><br>
                    <small>${valA} is ${result.toFixed(2)}% of ${valB}</small>
                `;
                historyText = `${valA} is ${result.toFixed(2)}% of ${valB}`;
            }
        } 
        else if (mode === 'percent_change') {
            // Logic: Change from A to B
            if (valA === 0) {
                resultText = "Starting value cannot be zero for change calculation.";
                historyText = "Error";
            } else {
                result = ((valB - valA) / valA) * 100;
                let direction = result > 0 ? "Increase" : "Decrease";
                let color = result > 0 ? "#4caf50" : "#ff5252"; // Green for up, Red for down
                
                resultText = `
                    <strong>${direction}:</strong> <span style="color:${color}; font-size:1.4em;">${Math.abs(result).toFixed(2)}%</span><br>
                    <small>From ${valA} to ${valB}</small>
                `;
                historyText = `${valA} -> ${valB}: ${result.toFixed(2)}%`;
            }
        }
    }

        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        resBox.style.display = 'block';
        addToHistory_universal_percentage_calculator(historyText);
    }

    function addToHistory_universal_percentage_calculator(item) {
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_universal_percentage_calculator)) || [];
        history.unshift(item);
        if (history.length > 10) history.pop();
        localStorage.setItem(STORAGE_KEY_universal_percentage_calculator, JSON.stringify(history));
        renderHistory_universal_percentage_calculator();
    }

    function renderHistory_universal_percentage_calculator() {
        const list = document.getElementById('history_list_universal_percentage_calculator');
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_universal_percentage_calculator)) || [];
        list.innerHTML = history.map(item => `<li>${item}</li>`).join('');
    }

    function clearHistory_universal_percentage_calculator() {
        localStorage.removeItem(STORAGE_KEY_universal_percentage_calculator);
        renderHistory_universal_percentage_calculator();
    }
</script>

<style>
  .calc-grid { display: grid; gap: 20px; grid-template-columns: 1fr; }
  @media (min-width: 768px) { .calc-grid { grid-template-columns: 2fr 1fr; } }
  .calc-history { background: #252526; padding: 15px; border-radius: 8px; font-size: 0.9em; }
  .calc-history h4 { margin-top: 0; border-bottom: 1px solid #444; padding-bottom: 5px; }
  .calc-history ul { padding-left: 20px; color: #bbb; }
  .btn-small { background: #444; font-size: 0.8em; padding: 5px 10px; margin-top: 10px; }
  .calc-main label { display: block; margin-top: 10px; font-weight: bold; }
  .calc-main input, .calc-main select { width: 100%; padding: 8px; margin-top: 5px; background: #333; border: 1px solid #555; color: white; }
  .calc-main button { margin-top: 20px; width: 100%; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }
  .calc-main button:hover { background: #0056b3; }
  .result-box { margin-top: 20px; padding: 15px; background: #2d2d2d; border-left: 4px solid #007bff; }
</style>

{{< /calculator >}}

## How to Use

### Why this matters
Percentages are the universal language of comparison. Whether you are calculating a discount at a store, analyzing stock market returns, or grading a test, understanding how to manipulate these numbers is essential.

### The Three Modes explained
1. **Percentage of a Number:** Use this to find a portion. *Example: "What is 20% of my $50 bill?"*
2. **What % is X of Y:** Use this to find the rate. *Example: "I got 45 questions right out of 50. What is my grade?"*
3. **Percentage Change:** Use this to compare growth or loss. *Example: "My rent went from $1,000 to $1,100. How much did it go up?"*


## The Math Behind It
Depending on the mode you selected, the tool uses one of these three formulas:

$$

\begin{align*}
\text{1. Percentage of:} & \quad P = \frac{\text{Percent}}{100} \times \text{Total} \\
\text{2. What \% is X of Y:} & \quad \% = \frac{\text{Part}}{\text{Total}} \times 100 \\
\text{3. Percent Change:} & \quad \Delta\% = \frac{\text{New} - \text{Old}}{\text{Old}} \times 100
\end{align*}

$$

**Where:**


* $P$ is the **Part** (the result).
* $\Delta\%$ is the **Change** in percentage.
* Values are standard decimal or integer inputs.

