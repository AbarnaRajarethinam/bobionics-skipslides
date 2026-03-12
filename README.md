# **Bobionics-skipslides**

**SkipSlides** is an **AI-powered tool** that converts code repositories into **ready-to-present slides**. It analyzes your project files and generates a **structured presentation** explaining the **purpose, architecture, and workflow** of your code.

---

### **Current Features**

#### **1. Upload System**

Users can upload their project files as a **ZIP archive**. The system stores and extracts the repository so it can be analyzed.

* **Accepted formats:** `.zip`
* **Automatic extraction:** Uploaded archives are extracted into a unique project directory.
* **File filtering:** Irrelevant directories such as `venv`, `node_modules`, and other dependency folders are ignored during scanning.
* **Output locations:**

  * Uploaded files are temporarily stored in **`uploads/`**
  * Extracted repositories are stored in **`extracted/`**

This prepares the project files for repository analysis.

---

#### **2. Repository Analysis**

After extraction, the system scans the uploaded repository to identify the **most relevant project files**.

Each file is assigned a **relevance score** based on several signals:

* **Documentation files** (`README.md`)
* **Entry points** (`main.py`, `app.py`, `run.py`, `server.py`)
* **Machine learning indicators** (`model`, `train`, `predict`, `inference`)
* **Dependency and configuration files** (`requirements.txt`, `environment.yml`, `package.json`)
* **File types** (`.ipynb`, `.py`, `.js`, `.ts`)
* **Repository structure signals** (files located in `src/`, `model/`, `training/`, or the project root)

The scanner then ranks the files and selects the **Top N most relevant files** for further processing.

To improve performance when scanning large repositories, common dependency directories are ignored, including:

```
node_modules
venv
__pycache__
.git
dist
build
coverage
.next
```

---

#### **3. Important File Extraction**

Once the most relevant files are identified, the system reads their **full contents** and prepares them in a structured format.

Example output:

```
[
  {
    "filename": "README.md",
    "content": "full file contents..."
  },
  {
    "filename": "main.py",
    "content": "full file contents..."
  }
]
```

This structured data is returned by the `/upload` endpoint and will later be used by the **AI slide generation pipeline**.

For development purposes, the backend also prints **debug information in the terminal**, including:

* file scores
* selected top files
* short previews of file contents

This allows developers to understand how the repository analysis system prioritizes files.

*Future updates* will include **automatic recognition of main project files**, **AI-powered summarization**, and **slide generation**.

---

### **How to Run**

**1. Using the Shell Script and Docker**

* **Start or reopen the container:**
  If `requirements.txt` hasn’t changed, just reopen the container using Docker. If it **has changed**, rebuild the container:

  ```bash
  docker-compose build
  docker-compose up -d
  ```

* **Run the app:**
  Inside the container, run:

  ```bash
  bash run.sh
  ```

  The app will start a local server at **[http://localhost:8000](http://localhost:8000)**.

* **Run tests:**
  To check tests, run:

  ```bash
  python -m pytest -v
  ```

  This executes all tests in the **`tests/`** folder to ensure the upload system and repo analysis are working correctly.

> This workflow allows you to quickly restart the app without rebuilding the container every time, unless dependencies change.

---

### **Development Notes**

This document is updated **incrementally** as new features are implemented. Current focus:

* **Upload and extraction system**
* **Repo analysis** (file filtering, identifying key files)
* **AI-based project summarization** (*coming soon*)
* **Slide generation pipeline** (*coming soon*)

---

### **Contributing**

When adding new features:

1. **Update this document** with a summary of your feature.
2. Add **tests** to the `tests/` folder.
3. **Commit changes** following the feature naming convention.
4. Include any **Docker-related updates** if the feature requires new dependencies.

---

### **Directory Structure**

* **`extracted/`** — Extracted uploaded project files
* **`uploads/`** — Temporary storage for uploaded zip files
* **`src/`** — Backend code (app, repo analysis, upload handler, etc.)
* **`frontend/`** — Frontend templates
* **`tests/`** — Unit and integration tests
* **`run.sh`** — Script to run the app locally
* **`requirements.txt`** — Python dependencies
* **`docker-compose.yml`** — Docker setup for running the app in a container

---

### **Future Features**

* **AI-powered project summaries**
* **PowerPoint slide generation**
* **Architecture diagram visualization**
* **GitHub repo input option**
* **Demo explanation / presentation script generation**

---

