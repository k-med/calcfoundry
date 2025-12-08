# 🧮 CalcFoundry

> **The Open Source Calculation Library** \> *Accurate. Transparent. Private.*

**CalcFoundry** is a high-performance, static web library of useful calculators and tools. Unlike ad-heavy generic calculator sites, CalcFoundry is built on **Hugo**, ensuring it is blazing fast, and runs entirely in the browser—meaning your financial or health data never leaves your device.

We don't just give you the answer; we show you the math behind it.

-----

## 🚀 Key Features

  * **⚡ Blazing Fast:** Built on Hugo (Static Site Generator) with the minimal PaperMod theme.
  * **🔒 Privacy First:** All calculations happen via client-side JavaScript. No server-side processing.
  * **📚 Educational:** Every calculator includes a "Math Behind It" section with LaTeX-rendered formulas.
  * **💾 Local History:** Calculators automatically save your recent history to your browser's LocalStorage.
  * **Python-Generated:** Content is programmatically generated via Python scripts to ensure mathematical precision and code consistency.

-----

## 📚 The Library

CalcFoundry covers a wide spectrum of disciplines. Current tools include:

| Category | Tool | Description |
| :--- | :--- | :--- |
| **Finance** | **Investment Growth** | Visualize the "Eighth Wonder of the World" (Compound Interest) with monthly contributions. |
| **Math** | **Universal Percentage** | Calculate increases, decreases, and "X is what % of Y" instantly. |
| **Statistics** | **Survey Sample Size** | Determine required respondents using Cochran’s Formula with Finite Population Correction. |
| **Health** | **BMI Calculator** | Calculate Body Mass Index with support for both Imperial (lbs/ft) and Metric (kg/cm) systems. |

-----

## 🛠️ How It Works (The Generator Pattern)

CalcFoundry uses a unique **Python-to-Markdown** workflow. Instead of writing error-prone HTML and JavaScript manually inside Markdown files, we use Python scripts to generate the Hugo content.

### 1\. The Python Script

We define the inputs, the JavaScript logic, and the LaTeX formulas in a Python script (e.g., `gen_investment.py`).

### 2\. The Generation

Running the script creates a standardized Markdown file in `content/posts/` containing:

  * Hugo Frontmatter (Title, Date, Categories).
  * The Calculator UI (HTML).
  * The Logic (Embedded JS).
  * The Explainer (LaTeX Math).

### 3\. The Build

Hugo compiles these files into the static website.

-----

## 💻 Local Development

Follow these steps to run CalcFoundry locally:

### Prerequisites

  * [Hugo](https://gohugo.io/installation/) (Extended version recommended)
  * Python 3.x

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/k-med/calcfoundry.git
    cd calcfoundry
    ```

2.  **Initialize the theme (PaperMod):**

    ```bash
    git submodule update --init --recursive
    ```

3.  **Generate the Calculators:**
    Run the Python generators to populate your content folder.

    ```bash
    python tools/gen_investment.py
    python tools/gen_percentage_calculator.py
    python tools/gen_survey_sample_size_calculator.py
    python tools/gen_bmi_calc.py
    ```

4.  **Run the Hugo Server:**

    ```bash
    hugo server -D
    ```

    Navigate to `http://localhost:1313/` to see the site.

-----

## 🤝 Contributing

We welcome fellow polymaths\! To add a new calculator:

1.  Duplicate one of the existing generator scripts (e.g., `gen_percentage_calculator.py`).
2.  Update the **Inputs HTML**, **Calculation JS**, and **LaTex Formula**.
3.  Run the script to generate the new Markdown file.
4.  Submit a Pull Request.

**Note:** Please ensure all mathematical formulas are cited or derived from standard academic sources.

-----

## 📄 License

This project is open source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

-----

*Generated with ❤️ by the CalcFoundry Page Generator.*