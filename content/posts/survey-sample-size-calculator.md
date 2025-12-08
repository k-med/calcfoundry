---
title: "Survey Sample Size Calculator"
date: 2025-12-08
categories: ["Statistics"]
summary: "Calculate exactly how many survey responses you need for statistically significant results. Supports finite population correction."
math: true
disableSpecial1stPost: true
---

Calculate exactly how many survey responses you need for statistically significant results. Supports finite population correction.

{{< calculator >}}

<div class="calc-grid">
  <div class="calc-main">
    
<label>Confidence Level</label>
<select id="confidence_level">
    <option value="1.645">90% (Low Risk)</option>
    <option value="1.96" selected>95% (Standard)</option>
    <option value="2.576">99% (High Precision)</option>
</select>

<label>Margin of Error (%)</label>
<input type="number" id="margin_error" placeholder="e.g. 5" value="5">

<label>Population Size (Optional)</label>
<input type="number" id="population_size" placeholder="Leave blank for infinite">

<label>Estimated Proportion (%)</label>
<input type="number" id="proportion" placeholder="e.g. 50" value="50">
<small style="color:#888;">Use 50% if unsure (this gives the maximum sample size).</small>

    <button onclick="calculate_survey_sample_size_calculator()">Calculate Sample Size</button>
    <div id="result_box" class="result-box" style="display:none;">
        <span id="result_val"></span>
    </div>
    
    <div style="margin-top: 15px; text-align: center; font-size: 0.85em;">
        <a href="#the-math-behind-it" style="color: #888; text-decoration: underline; cursor: pointer;">
            See the Formula
        </a>
    </div>
  </div>

  <div class="calc-history">
    <h4>History</h4>
    <ul id="history_list_survey_sample_size_calculator"></ul>
    <button onclick="clearHistory_survey_sample_size_calculator()" class="btn-small">Clear History</button>
  </div>
</div>

<script>
    const STORAGE_KEY_survey_sample_size_calculator = "calcfoundry_history_survey_sample_size_calculator"; 

    window.onload = function() { renderHistory_survey_sample_size_calculator(); };

    function calculate_survey_sample_size_calculator() {
        
    // Inputs
    let Z = parseFloat(document.getElementById('confidence_level').value);
    let e_percent = parseFloat(document.getElementById('margin_error').value);
    let pop = parseFloat(document.getElementById('population_size').value);
    let p_percent = parseFloat(document.getElementById('proportion').value);

    // Sanitize
    if (isNaN(e_percent) || e_percent <= 0) e_percent = 5; 
    if (isNaN(p_percent)) p_percent = 50;
    
    let e = e_percent / 100;
    let p = p_percent / 100;

    // 1. Calculate Standard Sample Size (Infinite Population)
    // Formula: (Z^2 * p * (1-p)) / e^2
    let numerator = Math.pow(Z, 2) * p * (1 - p);
    let denominator = Math.pow(e, 2);
    let n = numerator / denominator;

    // 2. Apply Finite Population Correction (if population is provided)
    // Formula: n_adj = n / (1 + ((n - 1) / Population))
    let isFinite = false;
    if (!isNaN(pop) && pop > 0) {
        n = n / (1 + ((n - 1) / pop));
        isFinite = true;
    }

    // Always round up for people
    let final_n = Math.ceil(n);

    // Output Generation
    let popText = isFinite ? `Population: ${pop.toLocaleString()}` : "Infinite Population";
    
    var resultText = `
        <strong>Required Sample Size:</strong> <span style="color:#4caf50; font-size:1.4em;">${final_n}</span><br>
        <hr style="border-color:#444; opacity:0.3; margin: 10px 0;">
        <small>${popText} @ ${document.getElementById('confidence_level').options[document.getElementById('confidence_level').selectedIndex].text}</small><br>
        <small>Margin of Error: ±${e_percent}%</small>
    `;

        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        resBox.style.display = 'block';
        addToHistory_survey_sample_size_calculator(resultText);
    }

    function addToHistory_survey_sample_size_calculator(item) {
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_survey_sample_size_calculator)) || [];
        history.unshift(item);
        if (history.length > 10) history.pop();
        localStorage.setItem(STORAGE_KEY_survey_sample_size_calculator, JSON.stringify(history));
        renderHistory_survey_sample_size_calculator();
    }

    function renderHistory_survey_sample_size_calculator() {
        const list = document.getElementById('history_list_survey_sample_size_calculator');
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_survey_sample_size_calculator)) || [];
        list.innerHTML = history.map(item => `<li>${item}</li>`).join('');
    }

    function clearHistory_survey_sample_size_calculator() {
        localStorage.removeItem(STORAGE_KEY_survey_sample_size_calculator);
        renderHistory_survey_sample_size_calculator();
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

## How to Use This Calculator

### Understanding the Results
In statistics, the "Sample Size" is the number of individual responses you need to collect to ensure that your survey results accurately represent the overall population within your chosen margin of error.


### Key Concepts:
* **Confidence Level:** How sure you want to be that the actual data falls within your margin of error. 95% is the industry standard.
* **Margin of Error:** The wiggle room you allow. If your survey says 60% of people like pizza with a 5% margin of error, the "true" number is between 55% and 65%.
* **Population:** If you are surveying a specific small group (e.g., "Employees at my company of 500 people"), input that number. If you are surveying "US Consumers," leave it blank (infinite).


## The Math Behind It
The tool uses Cochran's Sample Size Formula with a Finite Population Correction:

$$
n = \frac{\frac{Z^2 \cdot p(1-p)}{e^2}}{1 + \frac{\frac{Z^2 \cdot p(1-p)}{e^2} - 1}{N}}
$$

**Where:**


* $n$ is the **Sample Size** needed.
* $N$ is the **Population Size**.
* $Z$ is the **Z-score** (1.96 for 95% confidence).
* $p$ is the **Estimated Proportion** (0.5 yields the most conservative sample).
* $e$ is the **Margin of Error** (decimal format).

