---
title: "Return on Investment Calculator"
date: 2025-12-08
categories: ["Business"]
summary: "Instantly calculate the percentage return on any investment."
---

Instantly calculate the percentage return on any investment.

{{< calculator >}}


<label>Total Investment ($)</label>
<input type="number" id="inv" value="5000">
<label>Returned Amount ($)</label>
<input type="number" id="ret" value="6500">
<button onclick="calcROI()">Calculate ROI</button>
<div id="roi_res" class="result-box">Result...</div>

<script>
function calcROI() {
    let i = parseFloat(document.getElementById('inv').value);
    let r = parseFloat(document.getElementById('ret').value);
    let res = ((r - i) / i) * 100;
    document.getElementById('roi_res').innerHTML = `<strong>ROI:</strong> ${res.toFixed(2)}%`;
}
</script>


{{< /calculator >}}

### How it Works
This tool uses the following mathematical principle:
$$
ROI = \frac{Current Value - Cost of Investment}{Cost of Investment} \times 100
$$
