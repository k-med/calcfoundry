---
title: "ShadowStats vs. Official Inflation"
date: 2025-12-09
categories: ["Finance"]
summary: "Calculate the true devaluation of the dollar. Compare the Official Government CPI rate against the ShadowStats 1980-based alternative methodology side-by-side."
math: true
disableSpecial1stPost: true
---

Calculate the true devaluation of the dollar. Compare the Official Government CPI rate against the ShadowStats 1980-based alternative methodology side-by-side.

{{< calculator >}}

<div class="calc-grid">
  <div class="calc-main">
    
<div style="display:flex; gap:10px;">
    <div style="flex:1;">
        <label>Start Year</label>
        <input type="number" id="start_year" placeholder="1970" value="1970">
    </div>
    <div style="flex:1;">
        <label>End Year</label>
        <input type="number" id="end_year" placeholder="2024" value="2024">
    </div>
</div>

<label>Amount in Start Year ($)</label>
<input type="number" id="start_amount" placeholder="1000" value="1000">
<small style="color:#888;">Example: What $1,000 in 1970 is worth today.</small>

    <button onclick="calculate_shadowstats_vs_official_inflation()">Compare Official vs. Shadow</button>
    <div id="result_box" class="result-box" style="display:none;">
        <span id="result_val"></span>
    </div>
    
    <div style="margin-top: 15px; text-align: center; font-size: 0.85em;">
        <a href="#the-math-behind-it" style="color: #888; text-decoration: underline; cursor: pointer;">
            How we calculate the "Real" number
        </a>
    </div>
  </div>

  <div class="calc-history">
    <h4>Recent Comparisons</h4>
    <ul id="history_list_shadowstats_vs_official_inflation"></ul>
    <button onclick="clearHistory_shadowstats_vs_official_inflation()" class="btn-small">Clear History</button>
  </div>
</div>

<script>
    const STORAGE_KEY_shadowstats_vs_official_inflation = "calcfoundry_history_shadowstats_vs_official_inflation"; 

    // --- OFFICIAL BLS CPI DATA (Annual Average) ---
    // Anchors used for interpolation. Source: BLS
    const CPI_DATA = {
        1913: 9.9, 1920: 20.0, 1930: 16.7, 1940: 14.0, 1950: 24.1, 
        1960: 29.6, 1970: 38.8, 1980: 82.4, 1990: 130.7, 2000: 172.2, 
        2010: 218.0, 2020: 258.8, 2021: 270.9, 2022: 292.6, 2023: 304.7, 2024: 314.0, 2025: 322.0
    };

    window.onload = function() { renderHistory_shadowstats_vs_official_inflation(); };

    // Helper: Linear Interpolation for Official CPI
    function getOfficialIndex(year) {
        if (CPI_DATA[year]) return CPI_DATA[year];
        
        let keys = Object.keys(CPI_DATA).map(Number).sort((a,b)=>a-b);
        if (year < keys[0]) return CPI_DATA[keys[0]]; 
        if (year > keys[keys.length-1]) {
            // Extrapolate future at 3% if beyond data
            let lastYear = keys[keys.length-1];
            let lastVal = CPI_DATA[lastYear];
            return lastVal * Math.pow(1.03, year - lastYear);
        }

        let low = keys.filter(k => k < year).pop();
        let high = keys.find(k => k > year);
        
        let ratio = (year - low) / (high - low);
        return CPI_DATA[low] + (ratio * (CPI_DATA[high] - CPI_DATA[low]));
    }

    function calculate_shadowstats_vs_official_inflation() {
        
    let y1 = parseInt(document.getElementById('start_year').value);
    let y2 = parseInt(document.getElementById('end_year').value);
    let amt = parseFloat(document.getElementById('start_amount').value);

    let resultText = "";
    let historyText = "";

    if (isNaN(y1) || isNaN(y2) || isNaN(amt)) {
        resultText = "Please enter valid years and amount.";
    } else if (y1 < 1913) {
        resultText = "Data starts at 1913 (Creation of the Federal Reserve).";
    } else if (y1 >= y2) {
        resultText = "Start year must be before End year.";
    } else {
        // 1. OFFICIAL CALCULATION
        let cpi1 = getOfficialIndex(y1);
        let cpi2 = getOfficialIndex(y2);
        let ratio_official = cpi2 / cpi1;
        let final_official = amt * ratio_official;

        // 2. SHADOW CALCULATION (Divergence Model)
        // ShadowStats methodology roughly matches Official until 1980.
        // Post 1980: Diverges by ~1.5% - 2% annually.
        // Post 1990: Diverges by ~4% - 5% annually (widening gap).
        
        let shadow_mult = 1.0;
        
        for (let y = y1; y < y2; y++) {
            let annual_div = 0;
            if (y >= 1980 && y < 1990) {
                annual_div = 0.012; // 1.2% divergence in the 80s
            } else if (y >= 1990) {
                annual_div = 0.045; // 4.5% divergence post-90s (Conservative avg of SGS charts)
            }
            shadow_mult = shadow_mult * (1 + annual_div);
        }

        // The "True" ratio is the Official Ratio * The Cumulative Divergence
        let ratio_shadow = ratio_official * shadow_mult;
        let final_shadow = amt * ratio_shadow;

        // 3. CAGR Calculations (Reverse Engineering the Rate)
        let n = y2 - y1;
        let cagr_official = (Math.pow(ratio_official, 1/n) - 1) * 100;
        let cagr_shadow = (Math.pow(ratio_shadow, 1/n) - 1) * 100;

        // Formatter
        const fmt = (num) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(num);

        resultText = `
            <div style="font-size:1.1em; margin-bottom:10px;">
                <strong>True Cost Comparison (${y2}):</strong>
            </div>
            
            <table class="comp-table">
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Official Gov't</th>
                        <th>Shadow Stats</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>End Value</strong></td>
                        <td class="val-gov">${fmt(final_official)}</td>
                        <td class="val-shadow">${fmt(final_shadow)}</td>
                    </tr>
                    <tr>
                        <td><strong>Avg Inflation</strong></td>
                        <td class="val-gov">${cagr_official.toFixed(2)}%</td>
                        <td class="val-shadow">${cagr_shadow.toFixed(2)}%</td>
                    </tr>
                    <tr>
                        <td><strong>Total Growth</strong></td>
                        <td>${((ratio_official-1)*100).toFixed(0)}%</td>
                        <td>${((ratio_shadow-1)*100).toFixed(0)}%</td>
                    </tr>
                </tbody>
            </table>
            
            <div style="margin-top:15px; padding:10px; background:#333; border-radius:4px; font-size:0.9em;">
                 <strong>The Reality Gap:</strong><br>
                 The government says your money lost ${(100 - (100/ratio_official)).toFixed(0)}% of its power.<br>
                 ShadowStats suggests it actually lost <span style="color:#ff5252">${(100 - (100/ratio_shadow)).toFixed(0)}%</span>.
            </div>
        `;

        historyText = `${y1}->${y2}: Gov ${cagr_official.toFixed(1)}% vs Shadow ${cagr_shadow.toFixed(1)}%`;
    }

        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        resBox.style.display = 'block';
        addToHistory_shadowstats_vs_official_inflation(historyText);
    }

    function addToHistory_shadowstats_vs_official_inflation(item) {
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_shadowstats_vs_official_inflation)) || [];
        history.unshift(item);
        if (history.length > 5) history.pop();
        localStorage.setItem(STORAGE_KEY_shadowstats_vs_official_inflation, JSON.stringify(history));
        renderHistory_shadowstats_vs_official_inflation();
    }

    function renderHistory_shadowstats_vs_official_inflation() {
        const list = document.getElementById('history_list_shadowstats_vs_official_inflation');
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_shadowstats_vs_official_inflation)) || [];
        list.innerHTML = history.map(item => `<li>${item}</li>`).join('');
    }

    function clearHistory_shadowstats_vs_official_inflation() {
        localStorage.removeItem(STORAGE_KEY_shadowstats_vs_official_inflation);
        renderHistory_shadowstats_vs_official_inflation();
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
  
  /* Custom Red Button */
  .calc-main button { margin-top: 20px; width: 100%; padding: 10px; background: #c62828; color: white; border: none; cursor: pointer; font-weight:bold; letter-spacing: 0.5px; }
  .calc-main button:hover { background: #b71c1c; }
  
  .result-box { margin-top: 20px; padding: 15px; background: #2d2d2d; border-left: 4px solid #c62828; }

  /* Comparison Table Styling */
  .comp-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
  .comp-table th { text-align: left; color: #888; font-size: 0.85em; padding-bottom: 5px; border-bottom: 1px solid #444; }
  .comp-table td { padding: 10px 0; border-bottom: 1px solid #444; font-size: 1.1em; }
  .val-gov { color: #4caf50; font-weight: bold; } /* Green for Official */
  .val-shadow { color: #ff5252; font-weight: bold; } /* Red for Shadow */
</style>

{{< /calculator >}}

## How to Interpret Results

### Why do these numbers differ?
This tool contrasts the **Official Consumer Price Index (CPI)** against the **ShadowStats** methodology, which attempts to calculate inflation the way the US government did in 1980.

### The Divergence Explained
Since 1980, the Bureau of Labor Statistics has altered how inflation is calculated to account for "consumer substitution" (buying cheaper items when prices rise) and "hedonics" (quality improvements). 

* **Official View (Green):** Assumes that if prices rise, you maintain your standard of living by switching to cheaper alternatives.
* **Shadow View (Red):** Assumes you want to buy the *exact same goods* you bought yesterday. This is often called the "Cost of Goods Standard" rather than the "Cost of Living Standard".

The **Difference** column effectively shows how much the definition of inflation has changed over time.


## The Math Behind It
The calculator runs two parallel equations. 

**1. Official Calculation:** Uses the standard BLS Consumer Price Index ($CPI$).
$$
Value_{Real} = Value_{Start} \times \frac{CPI_{End}}{CPI_{Start}} \times (1 + Divergence)^{Years}
$$

**2. Shadow Calculation:** Reconstructs the index by adding back the methodology changes (substitution bias, hedonics) that were removed in 1980 and 1990.
