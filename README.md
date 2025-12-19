# Gemini Web AI

This is a simple web application that uses AI to generate images from text prompts. It's built with Flask and provides a web interface to enter prompts and view the generated images.

## About The Project

This project allows users to:
* Register and log in to a personal account.
* Enter text prompts to generate images.
* View a history of their generated images.

The backend is built with Flask, and the frontend uses vanilla JavaScript, HTML, and CSS.

## Getting Started

Follow these steps to get a local copy up and running.

### Prerequisites

*   Python 3.10 or newer. You can download it from [python.org](https://www.python.org/downloads/).
*   `pip` (Python's package installer), which comes with modern Python installations.

### Installation

1.  **Clone the repository:**
    If you have Git installed, you can clone the repository. Otherwise, you can download the source code as a ZIP file from GitHub.
    ```sh
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**
    It's highly recommended to use a virtual environment to keep the project's dependencies isolated.

    *   **On macOS and Linux:**
        ```sh
        python3 -m venv .venv
        source .venv/bin/activate
        ```

    *   **On Windows:**
        ```sh
        python -m venv .venv
        .venv\Scripts\activate
        ```

3.  **Install the dependencies:**
    With your virtual environment activated, install the required Python packages.
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the application:**
    ```sh
    python app.py
    ```

2.  **Access the web interface:**
    Open your web browser and navigate to:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

3.  **Register and generate:**
    *   You will be redirected to the login page. Click on "Register" to create a new account.
    *   After logging in, you can start entering prompts to generate images.

## Making Changes

If you want to modify or extend the application, here are the key files to look at:

*   `app.py`: This is the core of the application. It contains all the backend logic, including user authentication, prompt handling, and communication with the image generation API.
*   `templates/`: This directory contains the HTML files.
    *   `index.html`: The main page where users enter prompts and see images.
    *   `login.html`: The login and registration page.
*   `static/`: This directory contains the static assets for the frontend.
    *   `css/style.css`: The stylesheet for the application.
    *   `js/main.js`: The JavaScript code that handles user interactions on the frontend, like making API calls to the backend.

After making any changes to the Python code (`app.py`), you will need to stop the Flask server (with `Ctrl+C` in the terminal) and restart it to see the changes. Changes to frontend files (HTML, CSS, JS) should be visible after a simple browser refresh.
