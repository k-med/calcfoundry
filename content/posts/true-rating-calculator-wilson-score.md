---
title: "True Rating Calculator (Wilson Score)"
date: 2025-12-08
categories: ["Statistics"]
summary: "Calculate the true statistical accuracy of a rating or conversion rate using the Wilson Score Interval."
math: true
disableSpecial1stPost: true
---

Calculate the true statistical accuracy of a rating or conversion rate using the Wilson Score Interval.

{{< calculator >}}

<div class="calc-grid">
  <div class="calc-main">
    
<label>Total Trials (e.g., Visitors, Reviews)</label>
<input type="number" id="n_trials" placeholder="e.g. 100">

<label>Successes (e.g., Sales, 5-Star Ratings)</label>
<input type="number" id="n_success" placeholder="e.g. 95">

<label>Confidence Level</label>
<select id="conf_level">
    <option value="1.64485">90%</option>
    <option value="1.95996" selected>95% (Standard)</option>
    <option value="2.57583">99%</option>
</select>

    <button onclick="calculate_true_rating_calculator_wilson_score()">Calculate Confidence</button>
    <div id="result_box" class="result-box" style="display:none;">
        <span id="result_val"></span>
    </div>
  </div>

  <div class="calc-history">
    <h4>History</h4>
    <ul id="history_list_true_rating_calculator_wilson_score"></ul>
    <button onclick="clearHistory_true_rating_calculator_wilson_score()" class="btn-small">Clear History</button>
  </div>
</div>

<script>
    const STORAGE_KEY_true_rating_calculator_wilson_score = "omnicalc_history_true_rating_calculator_wilson_score";

    // Load history on page load
    window.onload = function() {
        renderHistory_true_rating_calculator_wilson_score();
    };

    function calculate_true_rating_calculator_wilson_score() {
        // -- AI Generated Logic Start --
        
    // 1. Get Inputs
    let n = parseFloat(document.getElementById('n_trials').value);
    let x = parseFloat(document.getElementById('n_success').value);
    let z = parseFloat(document.getElementById('conf_level').value);

    // 2. Validation
    if (isNaN(n) || isNaN(x) || n <= 0) {
        var resultText = "Please enter valid positive numbers.";
    } else if (x > n) {
        var resultText = "Successes cannot be greater than Total Trials.";
    } else {
        // 3. Wilson Score Formula Logic
        // p_hat is the observed proportion
        let p = x / n;
        
        // Parts of the formula broken down for readability
        let p1 = p + ( (z*z) / (2*n) );
        let p2 = z * Math.sqrt( ( (p*(1-p))/n ) + ( (z*z)/(4*n*n) ) );
        let p3 = 1 + ( (z*z) / n );
        
        // Calculate Lower and Upper Bounds
        let lower = (p1 - p2) / p3;
        let upper = (p1 + p2) / p3;
        
        // Convert to Percentages
        let obs_perc = (p * 100).toFixed(2);
        let min_perc = (lower * 100).toFixed(2);
        let max_perc = (upper * 100).toFixed(2);
        
        // 4. Format Output
        // We use a clean summary string for the result text
        var resultText = `
            <strong>True Score Range:</strong> ${min_perc}% — ${max_perc}%<br>
            <small style='opacity:0.8'>Observed Rate: ${obs_perc}% (at 95% Confidence)</small>
        `;
    }

        // -- AI Generated Logic End --

        // 'resultText' must be defined in the calculation_js above
        // Display Result
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        resBox.style.display = 'block';

        // Save to History
        addToHistory_true_rating_calculator_wilson_score(resultText);
    }

    function addToHistory_true_rating_calculator_wilson_score(item) {
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_true_rating_calculator_wilson_score)) || [];
        history.unshift(item); // Add to top
        if (history.length > 10) history.pop(); // Keep max 10
        localStorage.setItem(STORAGE_KEY_true_rating_calculator_wilson_score, JSON.stringify(history));
        renderHistory_true_rating_calculator_wilson_score();
    }

    function renderHistory_true_rating_calculator_wilson_score() {
        const list = document.getElementById('history_list_true_rating_calculator_wilson_score');
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_true_rating_calculator_wilson_score)) || [];
        list.innerHTML = history.map(item => `<li>${item}</li>`).join('');
    }

    function clearHistory_true_rating_calculator_wilson_score() {
        localStorage.removeItem(STORAGE_KEY_true_rating_calculator_wilson_score);
        renderHistory_true_rating_calculator_wilson_score();
    }
</script>

<style>
  /* Layout for Side-by-Side History */
  .calc-grid { display: grid; gap: 20px; grid-template-columns: 1fr; }
  @media (min-width: 768px) { .calc-grid { grid-template-columns: 2fr 1fr; } }
  
  .calc-history { background: #252526; padding: 15px; border-radius: 8px; font-size: 0.9em; }
  .calc-history h4 { margin-top: 0; border-bottom: 1px solid #444; padding-bottom: 5px; }
  .calc-history ul { padding-left: 20px; color: #bbb; }
  .btn-small { background: #444; font-size: 0.8em; padding: 5px 10px; margin-top: 10px; }
  
  /* Input styling specific to this calc */
  .calc-main label { display: block; margin-top: 10px; font-weight: bold; }
  .calc-main input, .calc-main select { width: 100%; padding: 8px; margin-top: 5px; background: #333; border: 1px solid #555; color: white; }
  .calc-main button { margin-top: 20px; width: 100%; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }
  .calc-main button:hover { background: #0056b3; }
  .result-box { margin-top: 20px; padding: 15px; background: #2d2d2d; border-left: 4px solid #007bff; }
</style>

{{< /calculator >}}

### Mathematical Principle

This calculator uses the **Wilson Score Interval** for binomial proportions. Unlike a normal approximation interval, the Wilson interval is asymmetric and remains accurate even for small sample sizes or extreme probabilities (near 0 or 1).

$$
w = \frac{\hat{p} + \frac{z^2}{2n} \pm z \sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}
$$
