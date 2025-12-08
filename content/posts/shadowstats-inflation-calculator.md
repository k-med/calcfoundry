---
title: "ShadowStats Inflation Calculator"
date: 2025-12-09
categories: ["Economics"]
summary: "Compare Official US CPI inflation against the ShadowStats (1980-based) true inflation. See how much the methodology changes affect your wallet."
math: true
disableSpecial1stPost: true
---

Compare Official US CPI inflation against the ShadowStats (1980-based) true inflation. See how much the methodology changes affect your wallet.

{{< calculator >}}

<div class="calc-grid">
  <div class="calc-main">
    
<label>Start Year (1913 - Present)</label>
<input type="number" id="start_year" placeholder="e.g. 1970" value="1970">

<label>Amount in Start Year ($)</label>
<input type="number" id="start_amount" placeholder="e.g. 1000" value="1000">

<label>Target Year</label>
<input type="number" id="end_year" placeholder="e.g. 2024" value="2024">

    <button onclick="calculate_shadowstats_inflation_calculator()">Compare Inflation Realities</button>
    <div id="result_box" class="result-box" style="display:none;">
        <span id="result_val"></span>
    </div>
    
    <div style="margin-top: 15px; text-align: center; font-size: 0.85em;">
        <a href="#the-math-behind-it" style="color: #888; text-decoration: underline; cursor: pointer;">
            Methodology Explained
        </a>
    </div>
  </div>

  <div class="calc-history">
    <h4>History</h4>
    <ul id="history_list_shadowstats_inflation_calculator"></ul>
    <button onclick="clearHistory_shadowstats_inflation_calculator()" class="btn-small">Clear History</button>
  </div>
</div>

<script>
    const STORAGE_KEY_shadowstats_inflation_calculator = "calcfoundry_history_shadowstats_inflation_calculator"; 

    // --- OFFICIAL CPI DATA (Simplified Anchor Points for Accuracy) ---
    // Source: BLS CPI-U Historical Data
    const CPI_ANCHORS = {
        1913: 9.9, 1920: 20.0, 1930: 16.7, 1940: 14.0, 1950: 24.1, 
        1960: 29.6, 1970: 38.8, 1980: 82.4, 1990: 130.7, 2000: 172.2, 
        2010: 218.0, 2020: 258.8, 2023: 304.7, 2024: 314.0, 2025: 322.0
    };

    window.onload = function() { renderHistory_shadowstats_inflation_calculator(); };

    function getOfficialCPI(year) {
        // Returns exact anchor if exists, otherwise linear interpolation
        if (CPI_ANCHORS[year]) return CPI_ANCHORS[year];
        
        // Find closest anchors
        let keys = Object.keys(CPI_ANCHORS).map(Number).sort((a,b)=>a-b);
        if (year < keys[0]) return CPI_ANCHORS[keys[0]]; // Floor
        if (year > keys[keys.length-1]) return CPI_ANCHORS[keys[keys.length-1]]; // Ceiling (Flatline future)

        let low = keys.filter(k => k < year).pop();
        let high = keys.find(k => k > year);
        
        // Interpolate
        let ratio = (year - low) / (high - low);
        return CPI_ANCHORS[low] + (ratio * (CPI_ANCHORS[high] - CPI_ANCHORS[low]));
    }

    function calculate_shadowstats_inflation_calculator() {
        
    let y1 = parseInt(document.getElementById('start_year').value);
    let amt = parseFloat(document.getElementById('start_amount').value);
    let y2 = parseInt(document.getElementById('end_year').value);
    
    let resultText = "";
    let historyText = "";

    // Validation
    if (isNaN(y1) || isNaN(amt) || isNaN(y2)) {
        resultText = "Please enter valid years and amount.";
    } else if (y1 < 1913 || y2 < 1913) {
        resultText = "Data is only available starting from 1913 (Creation of the Fed).";
    } else if (y1 >= y2) {
        resultText = "Start Year must be before Target Year.";
    } else {
        
        // 1. Get Official CPI Values
        let cpi1_off = getOfficialCPI(y1);
        let cpi2_off = getOfficialCPI(y2);
        
        // 2. Calculate Shadow Divergence
        // ShadowStats logic: 
        // Pre-1980: Matches Official.
        // 1980-1990: Adds ~1.5% annually to official.
        // 1990-Present: Adds ~4-7% annually to official (widening gap).
        
        // We reconstruct a "Shadow Index" relative to the official one.
        function getShadowMultiplier(year) {
            if (year <= 1980) return 1.0;
            
            // Calculate how many years past 1980
            let years_post_80 = year - 1980;
            let years_post_90 = Math.max(0, year - 1990);
            
            // Cumulative compounding divergence
            // 1.2% divergence factor for 80s, 5.0% factor for post-90s
            // This is a mathematical approximation of the ShadowStats SGS chart
            let divergence = Math.pow(1.012, years_post_80) * Math.pow(1.038, years_post_90);
            return divergence;
        }

        let shadow_mult1 = getShadowMultiplier(y1);
        let shadow_mult2 = getShadowMultiplier(y2);

        // Adjust the Official CPI by the multiplier to get "Shadow Index"
        let cpi1_shadow = cpi1_off * shadow_mult1;
        let cpi2_shadow = cpi2_off * shadow_mult2;

        // 3. Calculate Final Values
        let val_official = amt * (cpi2_off / cpi1_off);
        let val_shadow = amt * (cpi2_shadow / cpi1_shadow);
        
        let diff = val_shadow - val_official;
        let pct_diff = ((val_shadow - val_official) / val_official) * 100;

        // Formatter
        const fmt = (num) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(num);

        resultText = `
            <div style="margin-bottom:10px;">
                <strong>To buy the same goods in ${y2}:</strong>
            </div>
            
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Method</th>
                        <th>Projected Cost</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Official Gov't CPI</td>
                        <td class="official-col">${fmt(val_official)}</td>
                    </tr>
                    <tr>
                        <td>ShadowStats (1980 Base)</td>
                        <td class="shadow-col">${fmt(val_shadow)}</td>
                    </tr>
                    <tr>
                        <td><strong>The "Fudge" Gap</strong></td>
                        <td class="diff-col">+${fmt(diff)} (+${pct_diff.toFixed(0)}%)</td>
                    </tr>
                </tbody>
            </table>
            
            <hr style="border-color:#444; opacity:0.3; margin: 15px 0;">
            <small>If you feel like life is ${pct_diff.toFixed(0)}% more expensive than the news says, the ShadowStats model agrees with you.</small>
        `;
        
        historyText = `${y1} ($${amt}) → ${y2}: Gap +${pct_diff.toFixed(0)}%`;
    }

        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        resBox.style.display = 'block';
        addToHistory_shadowstats_inflation_calculator(historyText);
    }

    function addToHistory_shadowstats_inflation_calculator(item) {
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_shadowstats_inflation_calculator)) || [];
        history.unshift(item);
        if (history.length > 5) history.pop();
        localStorage.setItem(STORAGE_KEY_shadowstats_inflation_calculator, JSON.stringify(history));
        renderHistory_shadowstats_inflation_calculator();
    }

    function renderHistory_shadowstats_inflation_calculator() {
        const list = document.getElementById('history_list_shadowstats_inflation_calculator');
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_shadowstats_inflation_calculator)) || [];
        list.innerHTML = history.map(item => `<li>${item}</li>`).join('');
    }

    function clearHistory_shadowstats_inflation_calculator() {
        localStorage.removeItem(STORAGE_KEY_shadowstats_inflation_calculator);
        renderHistory_shadowstats_inflation_calculator();
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
  .calc-main button { margin-top: 20px; width: 100%; padding: 10px; background: #d32f2f; color: white; border: none; cursor: pointer; font-weight:bold; }
  .calc-main button:hover { background: #b71c1c; }
  .result-box { margin-top: 20px; padding: 15px; background: #2d2d2d; border-left: 4px solid #d32f2f; }
  
  .comparison-table { width: 100%; margin-top: 15px; border-collapse: collapse; }
  .comparison-table th, .comparison-table td { padding: 8px; text-align: left; border-bottom: 1px solid #444; }
  .comparison-table th { color: #aaa; font-size: 0.9em; }
  .official-col { color: #4caf50; font-weight: bold; }
  .shadow-col { color: #ff5252; font-weight: bold; }
  .diff-col { color: #ff9800; font-style: italic; }
</style>

{{< /calculator >}}

## How to Interpret the Split

### The Tale of Two Inflations
This calculator allows you to see the difference between the **Official CPI** (Consumer Price Index) reported by the Bureau of Labor Statistics and the **ShadowStats Alternative CPI**.

### Why the difference?
In 1980 and again in 1990, the US government changed how it calculates inflation. Critics, most notably John Williams of ShadowStats, argue these changes were political moves designed to lower reported inflation (and thus lower Social Security COLA payments).

#### The Two Main "Gimmicks" Removed by ShadowStats:
1.  **Substitution Bias:** The government assumes that if steak gets expensive, you switch to hamburger, so your "cost of living" didn't go up. ShadowStats argues this lowers your standard of living.
2.  **Hedonics:** If a computer costs the same but gets faster, the government counts that as a *price drop*. ShadowStats argues you still paid the same amount of cash.

By removing these adjustments and using the original **1980 Methodology**, ShadowStats typically shows inflation running 4% to 8% higher than official reports.


## The Math Behind It
The tool calculates two different future values ($FV$) based on different Consumer Price Indices (CPI):

$$
FV = P \times \frac{CPI_{End}}{CPI_{Start}} \quad \text{vs} \quad FV_{Shadow} = P \times \frac{CPI_{End} \cdot (1+d)^n}{CPI_{Start}}
$$

**Where:**


* $FV$ is the **Future Value** (Cost in Target Year).
* $P$ is the **Principal** (Amount in Start Year).
* $d$ is the **Divergence Factor** (The difference in methodology).
* $n$ is the number of years the divergence has compounded.

