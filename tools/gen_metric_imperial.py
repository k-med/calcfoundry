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
    
    <button onclick="calculate_{tool_id}()">Convert</button>
    
    <div id="result_box" class="result-box" style="display:none;">
        <span id="result_val"></span>
    </div>
    
    <div style="margin-top: 15px; text-align: center; font-size: 0.85em;">
        <a href="#the-math-behind-it" style="color: #888; text-decoration: underline; cursor: pointer;">
            See Conversion Formulas
        </a>
    </div>
  </div>

  <div class="calc-history">
    <h4>Conversion Log</h4>
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
  .result-box {{ margin-top: 20px; padding: 15px; background: #2d2d2d; border-left: 4px solid #007bff; }}
  
  .checkbox-wrapper {{ display: flex; align-items: center; margin-top: 10px; }}
  .checkbox-wrapper input {{ width: auto; margin-right: 10px; margin-top: 0; }}
</style>

{{{{< /calculator >}}}}

## How to Use
{educational_content}

## The Math Behind It
Most conversions are simple multiplication, but Temperature requires an offset adjustment.

$$
{formula_latex}
$$

**Where:**

{variable_definitions}
"""
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {filename}")


# === DEFINING THE CONVERTER ===

conv_inputs = """
<label>What are you converting?</label>
<select id="conv_mode">
    <optgroup label="Length & Distance">
        <option value="mi_km">Miles ↔ Kilometers</option>
        <option value="ft_m">Feet ↔ Meters</option>
        <option value="in_cm">Inches ↔ Centimeters</option>
    </optgroup>
    <optgroup label="Weight & Mass">
        <option value="lbs_kg">Pounds ↔ Kilograms</option>
        <option value="oz_g">Ounces ↔ Grams</option>
    </optgroup>
    <optgroup label="Volume & Cooking">
        <option value="gal_l">Gallons ↔ Liters</option>
        <option value="fl_oz_ml">Fluid Oz ↔ Milliliters</option>
    </optgroup>
    <optgroup label="Temperature">
        <option value="f_c">Fahrenheit ↔ Celsius</option>
    </optgroup>
</select>

<label>Enter Value</label>
<input type="number" id="input_val" placeholder="e.g. 10">

<div class="checkbox-wrapper">
    <input type="checkbox" id="reverse_dir">
    <label for="reverse_dir" style="margin:0; font-weight:normal; cursor:pointer;">Swap Direction (Metric to Imperial)</label>
</div>
<small style="color:#888; display:block; margin-top:5px;" id="direction_label">Currently: Imperial &rarr; Metric</small>

<script>
    // Simple UI update to show direction immediately
    document.getElementById('reverse_dir').addEventListener('change', function() {
        let label = document.getElementById('direction_label');
        if(this.checked) {
            label.innerHTML = "Currently: Metric &rarr; Imperial";
        } else {
            label.innerHTML = "Currently: Imperial &rarr; Metric";
        }
    });
</script>
"""

conv_js = """
    const mode = document.getElementById('conv_mode').value;
    const val = parseFloat(document.getElementById('input_val').value);
    const reverse = document.getElementById('reverse_dir').checked;
    
    let result = 0;
    let unitFrom = "";
    let unitTo = "";
    let resultText = "";
    let historySummary = "";

    if (isNaN(val)) {
        resultText = "Please enter a number to convert.";
    } else {
        // --- 1. TEMPERATURE LOGIC (Special Case) ---
        if (mode === 'f_c') {
            if (!reverse) {
                // F to C
                result = (val - 32) * (5/9);
                unitFrom = "°F"; unitTo = "°C";
            } else {
                // C to F
                result = (val * 9/5) + 32;
                unitFrom = "°C"; unitTo = "°F";
            }
        } 
        // --- 2. STANDARD MULTIPLICATION LOGIC ---
        else {
            let factor = 0;
            
            // Define Imperial -> Metric Factors
            switch(mode) {
                case 'mi_km': factor = 1.60934; unitFrom = "mi"; unitTo = "km"; break;
                case 'ft_m': factor = 0.3048; unitFrom = "ft"; unitTo = "m"; break;
                case 'in_cm': factor = 2.54; unitFrom = "in"; unitTo = "cm"; break;
                case 'lbs_kg': factor = 0.453592; unitFrom = "lbs"; unitTo = "kg"; break;
                case 'oz_g': factor = 28.3495; unitFrom = "oz"; unitTo = "g"; break;
                case 'gal_l': factor = 3.78541; unitFrom = "gal"; unitTo = "L"; break;
                case 'fl_oz_ml': factor = 29.5735; unitFrom = "fl oz"; unitTo = "ml"; break;
            }

            if (!reverse) {
                // Imperial -> Metric
                result = val * factor;
            } else {
                // Metric -> Imperial
                result = val / factor;
                // Swap unit labels
                let temp = unitFrom; unitFrom = unitTo; unitTo = temp;
            }
        }

        // --- FORMATTING ---
        // Smart decimal places: if result is huge, 1 decimal. If tiny, 3 decimals.
        let displayResult = result.toLocaleString(undefined, { maximumFractionDigits: 3 });
        
        resultText = `
            <strong>Result:</strong> <span style="color:#4caf50; font-size:1.4em;">${displayResult} ${unitTo}</span><br>
            <small>${val} ${unitFrom} = ${displayResult} ${unitTo}</small>
        `;
        
        historySummary = `${val} ${unitFrom} -> ${displayResult} ${unitTo}`;
    }
"""

conv_latex = r"T_{(°C)} = (T_{(°F)} - 32) \times \frac{5}{9} \quad \bigg| \quad V_{metric} = V_{imperial} \times \text{Factor}"

conv_content = """
### The Every-Man's Converter

Whether you are following a European recipe, traveling abroad, or working on a car, the divide between Imperial (US) and Metric units is a constant hurdle. This tool is designed to be the only converter you need bookmarking.

### Mental Math Shortcuts
If you don't have this calculator handy, here are some "close enough" estimates:
* **Fahrenheit to Celsius:** Subtract 30 and divide by 2. (e.g., $80°F - 30 = 50$, $50 / 2 = 25°C$).
* **Miles to Kilometers:** Multiply by 1.6. A 5k run is 3.1 miles.
* **Pounds to Kg:** Divide by 2. (100 lbs is roughly 45-50 kg).

### Why do we have two systems?
The Imperial system evolved from ancient Roman units based on human anatomy (feet, thumbs/inches). The Metric system was designed during the French Revolution to be scientific and based on decimals (powers of 10).
"""

conv_vars = """
* $T$ is **Temperature**.
* $V$ is **Value** (Length, Weight, or Volume).
* **Factor** changes based on the unit (e.g., 1.609 for Miles to Km).
"""

# === GENERATE THE FILE ===
create_calculator(
    title="Ultimate Imperial to Metric Converter", 
    category="Everyday Tools", 
    description="The Swiss Army Knife of conversions. Instantly convert Length, Weight, Volume, and Temperature between US Imperial and Metric systems.",
    inputs_html=conv_inputs,
    calculation_js=conv_js,
    formula_latex=conv_latex,
    educational_content=conv_content,
    variable_definitions=conv_vars 
)