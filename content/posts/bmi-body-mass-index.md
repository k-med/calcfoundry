---
title: "BMI Body Mass Index"
date: 2025-12-08
categories: ["Health"]
summary: "Check if you are in a healthy weight range based on height and weight."
---

Check if you are in a healthy weight range based on height and weight.

{{< calculator >}}


<label>Weight (kg)</label>
<input type="number" id="w" value="70">
<label>Height (cm)</label>
<input type="number" id="h" value="175">
<button onclick="calcBMI()">Check BMI</button>
<div id="bmi_res" class="result-box">Result...</div>

<script>
function calcBMI() {
    let w = parseFloat(document.getElementById('w').value);
    let h = parseFloat(document.getElementById('h').value) / 100; // convert to m
    let bmi = w / (h * h);
    document.getElementById('bmi_res').innerHTML = `<strong>Your BMI:</strong> ${bmi.toFixed(1)}`;
}
</script>


{{< /calculator >}}

### How it Works
This tool uses the following mathematical principle:
$$
BMI = \frac{kg}{m^2}
$$
