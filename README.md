# AI Website Generator

**AI Website Generator** is an AI-powered tool that helps you generate structured website layouts with multilingual support. Built with Streamlit and Gemini (Google AI), the app allows users to choose a visual style or input a project description and receive AI-generated JSON layouts for modern websites.

## 🌐 Interface Language Support

- 🇷🇺 Russian (Русский)
- 🇬🇧 English (English)
- 🇷🇴 Romanian (Română)

> The app interface is available in the three languages above.

⚠️ **Note:** AI content generation currently works **only in English**. Multilingual content generation (Russian, Romanian) is **under development**.

## ✨ What It Does

- Generates website layout structure in **JSON format**
- Lets you choose a **color palette**, number of pages, and visual style
- Accepts a **project description** or allows generation from a visual style alone
- Uses **Gemini AI** to create concise, human-like text for each section (in English)

### Output Example

The output is a structured `JSON` layout for a modern website, including:
- Project overview
- Pages and sections
- Suggested layouts, color palettes, and text

This structure can later be used to generate real HTML/CSS or feed into a visual website builder.

---

## 🔑 Gemini API Key Required

To use the generator, you must provide your [Gemini API key](https://ai.google.dev/).

### How to enter the Gemini key

1. When you launch the app, use the **left sidebar** to enter your key in the **"Enter your Gemini API Key"** field.
2. Your key will be used only during your current session and is not saved.

> 🔐 Keep your API key secure. Never commit it to GitHub or share it publicly.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/devxmxina/ai-website-generator.git
cd ai-website-generator
```

### 2. Create a virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
### 4. Run the app

```bash
streamlit run main.py
```
> Go to http://localhost:8501 in your browser.
