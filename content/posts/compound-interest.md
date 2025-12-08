---
title: "Compound Interest Calculator"
date: 2025-12-08
categories: ["Finance"]
summary: "Calculate the future value of your investment with compound interest."
---

Calculate how your money grows over time.

{{< calculator >}}

<label>Principal Amount ($)</label>
<input type="number" id="principal" value="1000">

<label>Annual Interest Rate (%)</label>
<input type="number" id="rate" value="5">

<label>Time (Years)</label>
<input type="number" id="years" value="10">

<button onclick="calculateInterest()">Calculate Growth</button>

<div id="result" class="result-box">
    Result will appear here...
</div>

<script>
    function calculateInterest() {
        const p = parseFloat(document.getElementById('principal').value);
        const r = parseFloat(document.getElementById('rate').value) / 100;
        const t = parseFloat(document.getElementById('years').value);
        
        const amount = p * Math.pow((1 + r), t);
        
        document.getElementById('result').innerHTML = 
            `<strong>Future Value:</strong> $${amount.toFixed(2)}`;
    }
</script>

{{< /calculator >}}

### Formula Used
This tool uses the standard compound interest formula:
$$A = P(1 + r)^t$$