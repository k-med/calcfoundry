import os
from datetime import datetime

# --- CONFIGURATION & PATH SETUP ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "content", "posts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_calculator(title, category, description, inputs_html, calculation_js, formula_latex, educational_content, variable_definitions):
    safe_title = "".join(c for c in title if c.isalnum() or c == " ").lower().strip().replace(" ", "-")
    filename = os.path.join(OUTPUT_DIR, f"{safe_title}.md")
    
    tool_id = safe_title.replace("-", "_")
    date_str = datetime.now().strftime("%Y-%m-%d")

    content = f"""---
title: "{title}"
date: {date_str}
categories: ["{category}"]
summary: "{description}"
math: true
disableSpecial1stPost: true
---

{description}

{{{{< calculator >}}}}

<div class="calc-grid">
  <div class="calc-main">
    {inputs_html}
    <button onclick="calculate_{tool_id}()">Calculate Payments</button>
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
    <ul id="history_list_{tool_id}"></ul>
    
    <div style="display:flex; gap:10px; margin-top:10px;">
        <button onclick="downloadHistory_{tool_id}()" class="btn-small" style="flex:1;">Save</button>
        <button onclick="clearHistory_{tool_id}()" class="btn-small" style="flex:1;">Clear</button>
    </div>
  </div>
</div>

<script>
    const STORAGE_KEY_{tool_id} = "calcfoundry_history_{tool_id}"; 

    window.onload = function() {{ renderHistory_{tool_id}(); }};

    function calculate_{tool_id}() {{
        {calculation_js}
        
        const resBox = document.getElementById('result_box');
        document.getElementById('result_val').innerHTML = resultText;
        resBox.style.display = 'block';
        if(historySummary) addToHistory_{tool_id}(historySummary);
    }}

    function addToHistory_{tool_id}(item) {{
        let history = JSON.parse(localStorage.getItem(STORAGE_KEY_{tool_id})) || [];
        if (history.length === 0 || history[0] !== item) {{
            history.unshift(item);
            if (history.length > 10) history.pop();
            localStorage.setItem(STORAGE_KEY_{tool_id}, JSON.stringify(history));
            renderHistory_{tool_id}();
        }}
    }}

    function renderHistory_{tool_id}() {{
        const list = document.getElementById('history_list_{tool_id}');
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_{tool_id})) || [];
        list.innerHTML = history.map(item => `<li>${{item}}</li>`).join('');
    }}

    function clearHistory_{tool_id}() {{
        localStorage.removeItem(STORAGE_KEY_{tool_id});
        renderHistory_{tool_id}();
    }}

    function downloadHistory_{tool_id}() {{
        const history = JSON.parse(localStorage.getItem(STORAGE_KEY_{tool_id})) || [];
        if (history.length === 0) {{
            alert("No history to download.");
            return;
        }}

        let content = "CalcFoundry - {title} History\\n";
        content += "Date: " + new Date().toLocaleDateString() + "\\n";
        content += "-----------------------------------\\n\\n";
        
        history.forEach(item => {{
            let cleanItem = item.replace(/<[^>]*>?/gm, '');
            content += cleanItem + "\\n";
        }});

        const blob = new Blob([content], {{ type: 'text/plain' }});
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "{title.replace(' ', '_')}_History.txt";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }}
</script>

<style>
  .calc-grid {{ display: grid; gap: 20px; grid-template-columns: 1fr; }}
  @media (min-width: 768px) {{ .calc-grid {{ grid-template-columns: 2fr 1fr; }} }}
  .calc-history {{ background: #252526; padding: 15px; border-radius: 8px; font-size: 0.9em; }}
  .calc-history h4 {{ margin-top: 0; border-bottom: 1px solid #444; padding-bottom: 5px; }}
  .calc-history ul {{ padding-left: 20px; color: #bbb; }}
  .btn-small {{ background: #444; font-size: 0.8em; padding: 8px 10px; margin-top: 0; color: white; border: 1px solid #555; cursor:pointer; border-radius: 4px; }}
  .btn-small:hover {{ background: #555; }}
  
  .calc-main label {{ display: block; margin-top: 10px; font-weight: bold; }}
  .calc-main input, .calc-main select {{ width: 100%; padding: 8px; margin-top: 5px; background: #333; border: 1px solid #555; color: white; }}
  .calc-main button {{ margin-top: 20px; width: 100%; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }}
  .calc-main button:hover {{ background: #0056b3; }}
</style>

{{{{< /calculator >}}}}

## How to Use This Calculator
{educational_content}

## The Math Behind It
The tool uses the following mathematical principle:

$$
{formula_latex}
$$

**Where:**

{variable_definitions}
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {filename}")


# === DEFINING THE MORTGAGE & LOAN CALCULATOR ===

mortgage_inputs = """
<label>Loan Amount ($)</label>
<input type="number" id="loan_amount" placeholder="e.g. 300000" value="300000">

<label>Annual Interest Rate (%)</label>
<input type="number" id="interest_rate" placeholder="e.g. 6.0" value="6.0" step="0.01">

<label>Loan Term (Years)</label>
<input type="number" id="loan_term" placeholder="e.g. 30" value="30">

<label>Payment Frequency</label>
<select id="payment_freq">
    <option value="12" selected>Monthly</option>
    <option value="26">Fortnightly</option>
    <option value="52">Weekly</option>
</select>

<label>Optional Extra Payment per Period ($)</label>
<input type="number" id="extra_payment" placeholder="e.g. 200" value="0">
"""

mortgage_js = """
    let P = parseFloat(document.getElementById('loan_amount').value);
    let r_annual = parseFloat(document.getElementById('interest_rate').value);
    let t_years = parseFloat(document.getElementById('loan_term').value);
    let freq = parseInt(document.getElementById('payment_freq').value);
    let extra = parseFloat(document.getElementById('extra_payment').value) || 0;

    let resultText = "";
    let historySummary = "";

    if (isNaN(P) || P <= 0 || isNaN(r_annual) || r_annual < 0 || isNaN(t_years) || t_years <= 0) {
        resultText = "Please enter valid positive numbers for loan amount, interest rate, and term.";
    } else {
        let r = r_annual / 100 / freq; // periodic interest rate
        let N = t_years * freq;        // total number of periods

        // Standard periodic payment (M)
        let M = 0;
        if (r > 0) {
            M = P * (r * Math.pow(1 + r, N)) / (Math.pow(1 + r, N) - 1);
        } else {
            M = P / N;
        }

        // Amortization tracking with/without extra payments
        let balance_base = P;
        let total_interest_base = 0;
        for (let i = 0; i < N; i++) {
            let interest = balance_base * r;
            let principal = M - interest;
            if (principal > balance_base) {
                principal = balance_base;
            }
            total_interest_base += interest;
            balance_base -= principal;
            if (balance_base <= 0) break;
        }

        let balance_extra = P;
        let total_interest_extra = 0;
        let payments_made_extra = 0;
        let total_paid_extra = 0;
        let M_total = M + extra;

        for (let i = 0; i < N; i++) {
            let interest = balance_extra * r;
            let principal = M_total - interest;
            if (principal > balance_extra) {
                principal = balance_extra;
            }
            total_interest_extra += interest;
            balance_extra -= principal;
            payments_made_extra++;
            if (balance_extra <= 0) {
                break;
            }
        }

        let total_cost_base = P + total_interest_base;
        let total_cost_extra = P + total_interest_extra;
        let interest_saved = total_interest_base - total_interest_extra;
        let time_saved_periods = N - payments_made_extra;
        
        let freq_name = "month";
        let time_saved_text = "";
        if (freq === 12) {
            freq_name = "month";
            let years_saved = Math.floor(time_saved_periods / 12);
            let months_saved = time_saved_periods % 12;
            time_saved_text = (years_saved > 0 ? years_saved + " years " : "") + (months_saved > 0 ? months_saved + " months" : "");
        } else if (freq === 26) {
            freq_name = "fortnight";
            let years_saved = Math.floor(time_saved_periods / 26);
            let fortnights_saved = time_saved_periods % 26;
            time_saved_text = (years_saved > 0 ? years_saved + " years " : "") + (fortnights_saved > 0 ? fortnights_saved + " fortnights" : "");
        } else {
            freq_name = "week";
            let years_saved = Math.floor(time_saved_periods / 52);
            let weeks_saved = time_saved_periods % 52;
            time_saved_text = (years_saved > 0 ? years_saved + " years " : "") + (weeks_saved > 0 ? weeks_saved + " weeks" : "");
        }

        const fmt = (num) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(num);

        resultText = `
            <strong>Base Payment per ${freq_name}:</strong> <span style="color:#4caf50; font-size:1.3em; font-weight:bold;">${fmt(M)}</span><br>
            <small style="opacity:0.8">Total Payments: ${N} | Total Cost: ${fmt(total_cost_base)} (Interest: ${fmt(total_interest_base)})</small>
        `;

        if (extra > 0) {
            resultText += `
                <hr style="border-color:#444; opacity:0.3; margin: 10px 0;">
                <strong>With Extra Payments (${fmt(extra)}/period):</strong><br>
                Payment per ${freq_name}: <span style="color:#2196f3; font-weight:bold;">${fmt(M_total)}</span><br>
                Total Cost: ${fmt(total_cost_extra)} (Interest: ${fmt(total_interest_extra)})<br>
                <span style="color:#4caf50; font-weight:bold;">Saved ${fmt(interest_saved)} in Interest</span><br>
                <span style="color:#4caf50; font-weight:bold;">Paid off ${time_saved_text || "0 periods"} early</span>
            `;
        }
        
        historySummary = `${fmt(P)} @ ${r_annual}% for ${t_years}y: ${fmt(M)}/${freq_name}`;
        if (extra > 0) {
            historySummary += ` (+${fmt(extra)} extra, saved ${fmt(interest_saved)})`;
        }
    }
"""

mortgage_latex = r"M = P \frac{r(1+r)^N}{(1+r)^N - 1}"

mortgage_content = """
### Understanding Amortization & Interest Savings
When you take out a loan, each periodic payment is split between **paying off the principal** (the amount you borrowed) and **paying the interest** (the cost of borrowing). 

1. **Early Years:** Most of your payment goes towards interest, meaning your loan balance decreases very slowly.
2. **Later Years:** As the outstanding balance drops, the interest portion shrinks, and more of your payment goes towards the principal.
3. **The Power of Extra Payments:** Because interest is calculated based on your remaining principal, making even small extra payments directly targets the principal. This reduces the balance faster, compounding your interest savings over the remainder of the loan term.
"""

mortgage_vars = """
* $M$ is the **Periodic Payment**.
* $P$ is the **Loan Principal** (total borrowed amount).
* $r$ is the **Periodic Interest Rate** (Annual Rate / Frequency).
* $N$ is the **Total Number of Payments** (Years $\times$ Frequency).
"""

# === GENERATE THE FILE ===
create_calculator(
    title="Mortgage Loan Calculator", 
    category="Finance", 
    description="Calculate your periodic mortgage or loan payments, see the impact of extra payments, and estimate how much interest you can save.",
    inputs_html=mortgage_inputs,
    calculation_js=mortgage_js,
    formula_latex=mortgage_latex,
    educational_content=mortgage_content,
    variable_definitions=mortgage_vars 
)
