AI-Powered LinkedIn Post Generator
====================================

**Overview**
------------
**LinkedIn Post Generator** is an AI-powered tool that helps you craft **engaging, authentic, and professional LinkedIn posts** effortlessly. It uses **Llama3-70B via Groq's API** to generate content based on **chosen topics, lengths, and languages**, ensuring consistency and creativity in your online presence.

**Features**
------------
✅ **Smart Topic Selection** – Choose from a curated list of **professional categories**.\
✅ **Adjustable Post Length** – Generate **short, medium, or long-form** content based on your needs.\
✅ **Multilingual Support** – Create posts in **English and Hinglish** with natural flow.\
✅ **Few-Shot Learning** – Integrated with **example-based learning** for improved tone and relevance.\
✅ **Streamlined UI** – Built with **Streamlit** for ease of use and quick interaction.\
✅ **Custom Preprocessing** – Includes tools for **metadata extraction**, **tag standardization**, and **data preparation**.

**Installation & Setup**
------------------------
**1. Clone the Repository**

```bash
git clone https://github.com/maybemnv/LinkedIn-Post-Generator.git
cd linkedin-post-generator
```

**2. Install Required Packages**

```bash
pip install -r requirements.txt
```

**3. Configure API Key**

Create a `.env` file in the root directory and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

**Usage**
---------
Run the application with:

```bash
streamlit run main.py
```

**How to Use:**
1. Select a **topic** from the dropdown.
2. Choose the **desired length** (short, medium, or long).
3. Pick your **preferred language** (English or Hinglish).
4. Click **"Generate"** to receive your custom LinkedIn post.

**Advanced Data Processing**
---------------------------
Prepare more training data using the preprocessing script:

```bash
python preprocessing.py --input data/raw_posts.json --output data/processed_posts.json
```

This will:
* Extract post metadata
* Standardize tags for consistency
* Format examples for few-shot learning

**Contributing**
---------------
Contributions and suggestions are welcome! Please ensure any changes are clean, well-documented, and tested.
