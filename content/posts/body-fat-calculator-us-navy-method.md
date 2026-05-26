---
title: "Body Fat Calculator US Navy Method"
date: 2026-05-26
categories: ["Health"]
summary: "Estimate your body fat percentage using the standard US Navy circumference-based equations. Supports both US Imperial and Metric systems."
math: true
disableSpecial1stPost: true
---

Estimate your body fat percentage using the standard US Navy circumference-based equations. Supports both US Imperial and Metric systems.

{{< calculator >}}

<div class="calc-grid">
  <div class="calc-main">
    
<label>Gender</label>
<select id="gender_bf" onchange="toggleGender_bf()">
    <option value="male" selected>Male</option>
    <option value="female">Female</option>
</select>

<label>Measurement Unit</label>
<select id="units_bf" onchange="toggleUnits_bf()">
    <option value="imperial" selected>Imperial (inches / lbs)</option>
    <option value="metric">Metric (cm / kg)</option>
</select>

<label>Weight (optional)</label>
<div class="row-inputs">
    <div>
        <input type="number" id="weight_bf" placeholder="e.g. 180" value="180">
    </div>
    <div>
        <span id="weight_unit_bf" style="line-height:40px; margin-left:5px;">lbs</span>
    </div>
</div>

<label>Height</label>
<div id="height_imperial_bf" class="row-inputs">
    <div>
        <input type="number" id="feet_bf" placeholder="ft" value="5">
    </div>
    <div>
        <input type="number" id="inches_bf" placeholder="in" value="10">
    </div>
</div>
<div id="height_metric_bf" style="display:none;" class="row-inputs">
    <div>
        <input type="number" id="cm_bf" placeholder="cm" value="178">
    </div>
</div>

<label>Neck Circumference</label>
<div class="row-inputs">
    <div>
        <input type="number" id="neck_bf" placeholder="e.g. 15" value="15" step="0.1">
    </div>
    <div>
        <span id="neck_unit_bf" style="line-height:40px; margin-left:5px;">inches</span>
    </div>
</div>

<label>Waist Circumference (at navel for men, narrowest point for women)</label>
<div class="row-inputs">
    <div>
        <input type="number" id="waist_bf" placeholder="e.g. 36" value="36" step="0.1">
    </div>
    <div>
        <span id="waist_unit_bf" style="line-height:40px; margin-left:5px;">inches</span>
    </div>
</div>

<div id="hip_container_bf" style="display:none;">
    <label>Hip Circumference (widest point)</label>
    <div class="row-inputs">
        <div>
            <input type="number" id="hip_bf" placeholder="e.g. 38" value="38" step="0.1">
        </div>
        <div>
            <span id="hip_unit_bf" style="line-height:40px; margin-left:5px;">inches</span>
        </div>
    </div>
</div>

<script>
function toggleGender_bf() {
    let gender = document.getElementById('gender_bf').value;
    let hipContainer = document.getElementById('hip_container_bf');
    if (gender === 'female') {
        hipContainer.style.display = 'block';
    } else {
        hipContainer.style.display = 'none';
    }
}

function toggleUnits_bf() {
    let units = document.getElementById('units_bf').value;
    let isMetric = (units === 'metric');
    
    document.getElementById('height_imperial_bf').style.display = isMetric ? 'none' : 'flex';
    document.getElementById('height_metric_bf').style.display = isMetric ? 'flex' : 'none';
    
    document.getElementById('weight_unit_bf').innerText = isMetric ? 'kg' : 'lbs';
    document.getElementById('neck_unit_bf').innerText = isMetric ? 'cm' : 'inches';
    document.getElementById('waist_unit_bf').innerText = isMetric ? 'cm' : 'inches';
    document.getElementById('hip_unit_bf').innerText = isMetric ? 'cm' : 'inches';
}
</script>

    <button onclick="calculate_body_fat_calculator_us_navy_method()">Calculate Body Fat</button>
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
    <h4>Recent Calculations</h4>
    <ul id="history_list_body_fat_calculator_us_navy_method"></ul>
    
    <div style="display:flex; gap:10px; margin-top:10px;">
        <button onclick="downloadHistory_body_fat_calculator_us_navy_method()" class="btn-small" style="flex:1;">Save</button>
        <button onclick="clearHistory_body_fat_calculator_us_navy_method()" class="btn-small" style="flex:1;">Clear</button>
    </div>
  </div>
</div>

<script>
    const STORAGE_KEY_body_fat_calculator_us_navy_method = "calcfoundry_history_body_fat_calculator_us_navy_method"; 

    window.onload = function() { renderHistory_body_fat_calculator_us_navy_method(); };

    function calculate_body_fat_calculator_us_navy_method() {
        
    let gender = document.getElementById('gender_bf').value;
    let units = document.getElementById('units_bf').value;
    let weight = parseFloat(document.getElementById('weight_bf').value);
    
    let height_in = 0;
    let neck_in = 0;
    let waist_in = 0;
    let hip_in = 0;
    
    let isMetric = (units === 'metric');
    
    if (isMetric) {
        let cm = parseFloat(document.getElementById('cm_bf').value) || 0;
        height_in = cm / 2.54;
        neck_in = (parseFloat(document.getElementById('neck_bf').value) || 0) / 2.54;
        waist_in = (parseFloat(document.getElementById('waist_bf').value) || 0) / 2.54;
        if (gender === 'female') {
            hip_in = (parseFloat(document.getElementById('hip_bf').value) || 0) / 2.54;
        }
    } else {
        let ft = parseFloat(document.getElementById('feet_bf').value) || 0;
        let inches = parseFloat(document.getElementById('inches_bf').value) || 0;
        height_in = (ft * 12) + inches;
        neck_in = parseFloat(document.getElementById('neck_bf').value) || 0;
        waist_in = parseFloat(document.getElementById('waist_bf').value) || 0;
        if (gender === 'female') {
            hip_in = parseFloat(document.getElementById('hip_bf').value) || 0;
        }
    }
    
    let resultText = "";
    let historySummary = "";
    
    let valid = true;
    if (height_in <= 0 || neck_in <= 0 || waist_in <= 0) {
        valid = false;
        resultText = "Please enter valid measurements for height, neck, and waist.";
    }
    if (gender === 'male' && waist_in <= neck_in) {
        valid = false;
        resultText = "Waist circumference must be greater than neck circumference.";
    }
    if (gender === 'female' && (hip_in <= 0 || (waist_in + hip_in) <= neck_in)) {
        valid = false;
        resultText = "Please check waist, hip, and neck measurements. Waist + Hip must exceed Neck.";
    }
    
    if (valid) {
        let bfp = 0;
        if (gender === 'male') {
            bfp = 86.010 * Math.log10(waist_in - neck_in) - 70.041 * Math.log10(height_in) + 36.76;
        } else {
            bfp = 163.205 * Math.log10(waist_in + hip_in - neck_in) - 97.684 * Math.log10(height_in) - 78.387;
        }
        
        if (bfp < 2) bfp = 2; // Baseline physical minimum
        
        let category = "";
        let color = "";
        
        if (gender === 'male') {
            if (bfp < 6) { category = "Essential Fat"; color = "#3498db"; }
            else if (bfp < 14) { category = "Athlete"; color = "#2ecc71"; }
            else if (bfp < 18) { category = "Fitness"; color = "#27ae60"; }
            else if (bfp < 25) { category = "Average"; color = "#f39c12"; }
            else { category = "Obese"; color = "#e74c3c"; }
        } else {
            if (bfp < 14) { category = "Essential Fat"; color = "#3498db"; }
            else if (bfp < 21) { category = "Athlete"; color = "#2ecc71"; }
            else if (bfp < 25) { category = "Fitness"; color = "#27ae60"; }
            else if (bfp < 32) { category = "Average"; color = "#f39c12"; }
            else { category = "Obese"; color = "#e74c3c"; }
        }
        
        let extraText = "";
        if (!isNaN(weight) && weight > 0) {
            let fat_mass = weight * (bfp / 100);
            let lean_mass = weight - fat_mass;
            let weight_unit = isMetric ? "kg" : "lbs";
            extraText = `<br><small>Fat Mass: ${fat_mass.toFixed(1)} ${weight_unit} | Lean Mass: ${lean_mass.toFixed(1)} ${weight_unit}</small>`;
        }
        
        resultText = `
            <strong>Estimated Body Fat:</strong> <span style="font-size:1.6em; color:${color}; font-weight:bold;">${bfp.toFixed(1)}%</span><br>
            <strong style="color:${color}; text-transform: uppercase;">Category: ${category}</strong>
            ${extraText}
        `;
        
        historySummary = `${gender === 'male' ? 'Male' : 'Female'}: ${bfp.toFixed(1)}% (${category})`;
    }

        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        resBox.style.display = 'block';
        if(historySummary) addToHistory_body_fat_calculator_us_navy_method(historySummary);
    }

    function addToHistory_body_fat_calculator_us_navy_method(item) {
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_body_fat_calculator_us_navy_method)) || [];
        if (history.length === 0 || history[0] !== item) {
            history.unshift(item);
            if (history.length > 10) history.pop();
            localStorage.setItem(STORAGE_KEY_body_fat_calculator_us_navy_method, JSON.stringify(history));
            renderHistory_body_fat_calculator_us_navy_method();
        }
    }

    function renderHistory_body_fat_calculator_us_navy_method() {
        const list = document.getElementById('history_list_body_fat_calculator_us_navy_method');
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_body_fat_calculator_us_navy_method)) || [];
        list.innerHTML = history.map(item => `<li>${item}</li>`).join('');
    }

    function clearHistory_body_fat_calculator_us_navy_method() {
        localStorage.removeItem(STORAGE_KEY_body_fat_calculator_us_navy_method);
        renderHistory_body_fat_calculator_us_navy_method();
    }

    function downloadHistory_body_fat_calculator_us_navy_method() {
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_body_fat_calculator_us_navy_method)) || [];
        if (history.length === 0) {
            alert("No history to download.");
            return;
        }

        let content = "CalcFoundry - Body Fat Calculator US Navy Method History\n";
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
        a.download = "Body_Fat_Calculator_US_Navy_Method_History.txt";
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

## How to Interpret Your Results

### Understanding the US Navy Circumference Method
The US Navy Body Fat formula is a widely accepted method to estimate body fat percentage without using expensive equipment like DEXA scans or hydrostatic weighing. It relies on standard anatomical circumferences that track closely with subcutaneous and visceral fat deposits.

### Measuring Guidelines
To get the most accurate results, use a flexible, non-stretchable tape measure:
1. **Height:** Measured without shoes.
2. **Neck:** Measure just below the larynx (Adam's apple), wrapping horizontally.
3. **Waist:** 
   - **Men:** Measure horizontally at the level of the navel.
   - **Women:** Measure horizontally at the narrowest part of the abdomen (usually just above the navel).
4. **Hips (Women only):** Measure horizontally at the widest part of the glutes.

### Standard Categories (ACE Guidelines)
| Category | Men | Women |
| :--- | :--- | :--- |
| **Essential Fat** | 2–5% | 10–13% |
| **Athletes** | 6–13% | 14–20% |
| **Fitness** | 14–17% | 21–24% |
| **Average** | 18–24% | 25–31% |
| **Obese** | 25%+ | 32%+ |


## The Math Behind It
The tool uses the following mathematical principle:

$$
\begin{aligned}
\text{BFP}_{\text{male}} &= 86.010 \log_{10}(W - N) - 70.041 \log_{10}(H) + 36.76 \\
\text{BFP}_{\text{female}} &= 163.205 \log_{10}(W + Hp - N) - 97.684 \log_{10}(H) - 78.387
\end{aligned}
$$

**Where:**


* $W$ is the **Waist Circumference** (inches).
* $N$ is the **Neck Circumference** (inches).
* $H$ is the **Height** (inches).
* $Hp$ is the **Hip Circumference** (inches, females only).
* *Note: If Metric units are entered, they are converted to inches ($	ext{inches} = 	ext{cm} / 2.54$) before computing.*

