
# ICD Search Application - Flask Edition

This project is a sleek, modern, and server-side rendered web application for searching International Classification of Diseases (ICD) codes. It was systematically converted from a client-side React/TypeScript application to a traditional Flask/Jinja2 stack, preserving the original UI/UX while eliminating the need for a Node.js runtime environment.

## Table of Contents
1. [Tech Stack](#tech-stack)
2. [Project Structure](#project-structure)
3. [Systematic Build Process](#systematic-build-process)
    - [Step 1: Deconstruction & Analysis](#step-1-deconstruction--analysis)
    - [Step 2: HTML Template with Jinja2](#step-2-html-template-with-jinja2)
    - [Step 3: Centralized CSS Styling](#step-3-centralized-css-styling)
    - [Step 4: Minimalist Vanilla JavaScript](#step-4-minimalist-vanilla-javascript)
4. [Key Features & Design Choices](#key-features--design-choices)
5. [How to Integrate with Flask](#how-to-integrate-with-flask)

---

## Tech Stack

- **Backend**: Python with **Flask** (for routing and server logic).
- **Templating**: **Jinja2** (for dynamically rendering HTML on the server).
- **Frontend**:
    - **HTML5**: For semantic structure.
    - **CSS3**: For all styling, including a robust theming system using CSS variables.
    - **Vanilla JavaScript**: For lightweight client-side interactivity (theme switching).
- **Dependencies**: None (on the frontend).

---

## Project Structure

The application is organized into a standard Flask project structure to ensure separation of concerns.

```
/
├── static/
│   ├── css/
│   │   └── style.css       # All application styles
│   └── js/
│       └── main.js         # Client-side JavaScript logic
└── templates/
    └── web_app/
        └── templates/
            └── index.html  # Main Jinja2 template for the UI
└── app.py                  # (Example) Flask application entry point
```

---

## Systematic Build Process

The conversion from a React SPA to a server-rendered Flask application was performed in four systematic steps.

### Step 1: Deconstruction & Analysis

The first step was to analyze the original React application to understand its structure, state management, and component hierarchy.

- **Component Analysis**: The React components (`App.tsx`, `SearchInput.tsx`, `ResultsDisplay.tsx`, `ResultCard.tsx`) were reviewed to map out the complete UI structure.
- **State Identification**: React state managed by `useState` (`query`, `results`, `isLoading`, `error`, `theme`) was identified. In the new architecture, `query`, `results`, and `error` are managed by the Flask backend and passed to the template, while `theme` is managed by client-side JavaScript. `isLoading` is no longer needed as the page reloads on each search.
- **Logic Migration**: The API call logic in `services/geminiService.ts` was earmarked for migration to the Flask backend. The form submission, previously handled by a JavaScript `onSubmit` event, would be replaced by a standard HTML `<form>` submission.

### Step 2: HTML Template with Jinja2

The component-based JSX was consolidated into a single `index.html` file and enhanced with Jinja2 for dynamic rendering.

- **Structure Consolidation**: The JSX from all React components was translated into a single, semantic HTML structure within `index.html`.
- **SVG Inlining**: To reduce HTTP requests and simplify asset management, all SVG icons (`LogoIcon`, `SearchIcon`, theme icons, etc.) were embedded directly into the HTML.
- **Dynamic Content with Jinja2**: Jinja2 control structures were used to replicate the conditional rendering logic from React:
    - **Search Query**: The search input's value is populated with `value="{{ query or '' }}"` to preserve the query across submissions.
    - **Conditional Rendering**: An `{% if / elif / else %}` block in the results section handles all possible states:
        1. `{% if error %}`: Displays a generic error message.
        2. `{% elif results %}`: Iterates through the `results` list with `{% for result in results %}` and renders a result card for each item.
        3. `{% elif query %}`: Displays a "No Results Found" message if a search was made but yielded no results.
        4. `{% else %}`: Shows an initial welcome message prompting the user to start a search.

### Step 3: Centralized CSS Styling

All styling, previously defined with Tailwind CSS utility classes, was re-written into a single, maintainable `static/css/style.css` file.

- **CSS Theming**: A robust light/dark mode system was built using CSS variables (`:root`). The `html.dark` selector overrides these variables to apply the dark theme. This approach avoids style duplication and makes theme management trivial.
- **Style Replication**: The visual appearance of every element—from the search bar's focus ring to the result card's hover effect—was meticulously recreated using standard CSS properties.
- **Responsive Design**: Media queries (`@media`) were used to implement a responsive grid for the search results, ensuring the layout adapts seamlessly from mobile to desktop screens, matching the original breakpoints.

### Step 4: Minimalist Vanilla JavaScript

The client-side logic was distilled down to its essential function: theme switching.

- **Theme Toggle Logic**: The `static/js/main.js` script adds a click event listener to the theme toggle button. When clicked, it toggles the `dark` class on the `<html>` element.
- **Theme Persistence**: To remember the user's choice, the current theme (`'light'` or `'dark'`) is saved to `localStorage`.
- **Preventing FOUC**: A critical UX improvement was made by adding a tiny, blocking `<script>` in the `<head>` of `index.html`. This script runs *before* the page is rendered, reads the theme from `localStorage`, and applies the correct class to the `<html>` element instantly, preventing any "flash" of the wrong theme on page load.
- **Simplicity**: Complex React event handlers were removed. The search is triggered by a standard `method="get"` form submission, and input focus is handled natively with the `autofocus` attribute.

---

## Key Features & Design Choices

- **Server-Side Rendering**: The core design choice was to move all rendering logic to the server. This simplifies the frontend, removes the Node.js/build-step dependency, and improves initial page load performance.
- **Zero Frontend Dependencies**: The final application runs on native browser technologies (HTML, CSS, JS) without any external libraries or frameworks, making it extremely lightweight and fast.
- **Maintainable Theming**: Using CSS variables for theming is a modern, clean approach that makes it easy to adjust colors or add new themes in the future.
- **Progressive Enhancement**: The application is functional without JavaScript (search works via form submission). The JS only adds the non-essential theme toggle enhancement.

---

## How to Integrate with Flask

To run this frontend, you need a Flask backend that serves the `index.html` template.

A basic Flask route in `app.py` would look like this:

```python
from flask import Flask, render_template, request
# Assume a function 'get_search_results' exists that calls your data source (e.g., an API or database)
# from your_search_logic import get_search_results 

app = Flask(__name__, template_folder='templates/web_app')

@app.route('/')
def search_page():
    query = request.args.get('query', '')
    results = None
    error = None

    if query:
        try:
            # This function would contain the logic migrated from geminiService.ts
            results = get_search_results(query) 
        except Exception as e:
            error = "An error occurred while fetching results. Please try again later."
            print(f"Error: {e}")

    return render_template('templates/index.html', query=query, results=results, error=error)

if __name__ == '__main__':
    app.run(debug=True)
```
This setup properly wires the frontend templates and static files into a functional Flask application.
