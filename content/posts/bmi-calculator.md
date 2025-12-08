---
title: "BMI Calculator"
date: 2025-12-08
categories: ["Health"]
summary: "Check your Body Mass Index (BMI) instantly. Supports both Metric (cm/kg) and Imperial (ft/lbs) units with accurate health categories."
math: true
disableSpecial1stPost: true
---

Check your Body Mass Index (BMI) instantly. Supports both Metric (cm/kg) and Imperial (ft/lbs) units with accurate health categories.

{{< calculator >}}

<div class="calc-grid">
  <div class="calc-main">
    <div style="display:flex; gap:10px; margin-bottom:15px;">
        <button id="btn_imperial_bmi_calculator" onclick="setMode_bmi_calculator('imperial')" class="mode-btn active">US (Imperial)</button>
        <button id="btn_metric_bmi_calculator" onclick="setMode_bmi_calculator('metric')" class="mode-btn">Metric</button>
    </div>

    <input type="hidden" id="calc_mode_bmi_calculator" value="imperial">

    
<div id="group_imperial">
    <label>Height</label>
    <div class="row-inputs">
        <div><input type="number" id="feet" placeholder="ft"></div>
        <div><input type="number" id="inches" placeholder="in"></div>
    </div>
    
    <label>Weight</label>
    <input type="number" id="lbs" placeholder="lbs">
</div>

<div id="group_metric" style="display:none;">
    <label>Height (cm)</label>
    <input type="number" id="cm" placeholder="e.g. 175">
    
    <label>Weight (kg)</label>
    <input type="number" id="kg" placeholder="e.g. 70">
</div>

    
    <button onclick="calculate_bmi_calculator()">Calculate BMI</button>
    
    <div id="result_box" class="result-box" style="display:none;">
        <span id="result_val"></span>
    </div>

    <div style="margin-top: 15px; text-align: center; font-size: 0.85em;">
        <a href="#the-math-behind-it" style="color: #888; text-decoration: underline; cursor: pointer;">
            BMI Formula
        </a>
    </div>
  </div>

  <div class="calc-history">
    <h4>Recent Checks</h4>
    <ul id="history_list_bmi_calculator"></ul>
    <button onclick="clearHistory_bmi_calculator()" class="btn-small">Clear History</button>
  </div>
</div>

<script>
    const STORAGE_KEY_bmi_calculator = "calcfoundry_history_bmi_calculator"; 

    window.onload = function() { 
        renderHistory_bmi_calculator();
        setMode_bmi_calculator('imperial'); 
    };

    function setMode_bmi_calculator(mode) {
        document.getElementById('calc_mode_bmi_calculator').value = mode;
        document.getElementById('group_imperial').style.display = (mode === 'imperial') ? 'block' : 'none';
        document.getElementById('group_metric').style.display = (mode === 'metric') ? 'block' : 'none';
        document.getElementById('btn_imperial_bmi_calculator').className = (mode === 'imperial') ? 'mode-btn active' : 'mode-btn';
        document.getElementById('btn_metric_bmi_calculator').className = (mode === 'metric') ? 'mode-btn active' : 'mode-btn';
    }

    function calculate_bmi_calculator() {
        
    const mode = document.getElementById('calc_mode_bmi_calculator').value;
    let bmi = 0;
    let weight_display = "";
    let height_display = "";

    if (mode === 'imperial') {
        let ft = parseFloat(document.getElementById('feet').value) || 0;
        let inc = parseFloat(document.getElementById('inches').value) || 0;
        let lbs = parseFloat(document.getElementById('lbs').value) || 0;
        
        let total_inches = (ft * 12) + inc;
        
        if (total_inches > 0 && lbs > 0) {
            bmi = 703 * (lbs / (total_inches * total_inches));
            weight_display = lbs + " lbs";
            height_display = ft + "'" + inc + '"';
        }
    } else {
        let cm = parseFloat(document.getElementById('cm').value) || 0;
        let kg = parseFloat(document.getElementById('kg').value) || 0;
        
        if (cm > 0 && kg > 0) {
            let m = cm / 100;
            bmi = kg / (m * m);
            weight_display = kg + " kg";
            height_display = cm + " cm";
        }
    }

    let resultText = "";
    let historyItem = "";

    if (bmi > 0) {
        let category = "";
        let color = "";
        
        if (bmi < 18.5) { category = "Underweight"; color = "#3498db"; }
        else if (bmi < 24.9) { category = "Normal Weight"; color = "#4caf50"; }
        else if (bmi < 29.9) { category = "Overweight"; color = "#ff9800"; }
        else { category = "Obese"; color = "#f44336"; }

        resultText = `
            <strong>Your BMI:</strong> <span style="font-size:1.6em; color:${color};">${bmi.toFixed(1)}</span><br>
            <strong style="color:${color}; text-transform: uppercase;">${category}</strong>
            <hr style="border-color:#444; opacity:0.3; margin: 10px 0;">
            <small>Healthy range is usually 18.5 – 24.9</small>
        `;
        historyItem = `BMI ${bmi.toFixed(1)} (${category})`;
    } else {
        resultText = "Please enter valid height and weight measurements.";
        historyItem = "Invalid Input";
    }

        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        resBox.style.display = 'block';
        addToHistory_bmi_calculator(historyItem);
    }

    function addToHistory_bmi_calculator(item) {
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_bmi_calculator)) || [];
        history.unshift(item);
        if (history.length > 5) history.pop(); 
        localStorage.setItem(STORAGE_KEY_bmi_calculator, JSON.stringify(history));
        renderHistory_bmi_calculator();
    }

    function renderHistory_bmi_calculator() {
        const list = document.getElementById('history_list_bmi_calculator');
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_bmi_calculator)) || [];
        list.innerHTML = history.map(item => `<li>${item}</li>`).join('');
    }

    function clearHistory_bmi_calculator() {
        localStorage.removeItem(STORAGE_KEY_bmi_calculator);
        renderHistory_bmi_calculator();
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
  
  .mode-btn { flex:1; padding: 8px; background: #333; border: 1px solid #555; color: #888; cursor: pointer; }
  .mode-btn.active { background: #007bff; color: white; border-color: #007bff; }

  .result-box { margin-top: 20px; padding: 15px; background: #2d2d2d; border-left: 4px solid #007bff; }
  .row-inputs { display: flex; gap: 10px; }
  .row-inputs div { flex: 1; }
</style>

{{< /calculator >}}

## How to Interpret Your Results

### Understanding Body Mass Index
The Body Mass Index (BMI) is a screening method used by healthcare providers to identify potential weight problems. While it is not a perfect diagnostic tool (it does not account for muscle mass or bone density), it is the global standard for initial health assessment.

### Standard Categories (WHO)
* **Underweight:** BMI less than 18.5
* **Normal weight:** BMI between 18.5 and 24.9
* **Overweight:** BMI between 25 and 29.9
* **Obese:** BMI of 30 or greater

### A Note on Muscle Mass
Athletes and bodybuilders may have a high BMI because muscle weighs more than fat. In these cases, a high BMI does not necessarily indicate poor health.


## The Math Behind It
BMI is calculated differently depending on your unit system, though the underlying ratio remains the same:

$$

\begin{aligned}
\text{Metric:} & \quad BMI = \frac{\text{weight (kg)}}{\text{height (m)}^2} \\
\text{Imperial:} & \quad BMI = 703 \times \frac{\text{weight (lbs)}}{\text{height (in)}^2}
\end{aligned}

$$

**Where:**


* **Weight**: Measured in kilograms (kg) or pounds (lbs).
* **Height**: Measured in meters (m) or inches (in).
* **703**: The conversion factor used only for the Imperial formula.

