# **Bobionics-skipslides**

**SkipSlides** is an **AI-powered tool** that converts code repositories into **ready-to-present slides**. It analyzes your project files and generates a **structured presentation** explaining the **purpose, architecture, and workflow** of your code.

---

### **Current Features**

**1. Upload System**
Users can upload their project files as a **ZIP** or folder. The system extracts the files and prepares them for analysis.

* **Accepted formats:** `.zip`
* **Automatic extraction:** The system scans the uploaded directory and organizes files for further processing.
* **File filtering:** Ignores irrelevant directories like `venv`, `node_modules`, etc.
* **Output:** Extracted files are stored in **`extracted/`**, and temporary uploads are stored in **`uploads/`**.

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

