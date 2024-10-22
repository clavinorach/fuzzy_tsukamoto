# Fuzzy Tsukamoto Production System Web App

Welcome to the Fuzzy Tsukamoto Production System Web App! This application implements the Fuzzy Tsukamoto method to calculate production levels based on demand and stock levels using fuzzy logic principles. The web app is built using Python and Streamlit, providing an intuitive user interface to interact with the fuzzy logic system.

## Features

- 📊 Input Parameters: Easily input minimum and maximum values for demand, stock, and production.
- ⚙️ Fuzzy Tsukamoto Calculation: Automatically calculate production based on fuzzy membership functions.
- 📈 Graphs and Visualization: Visualize the membership functions of demand, stock, and production.
- 💡 Responsive Design: A modern, dark-themed UI with responsive and interactive elements.
- 📱 Web Interface: Access the app via any browser on desktop or mobile.

## Technology Stack


- **Language**: Python
- **Frontend**: Streamlit for interactive web components and visualization
- **Libraries**:
  - `matplotlib`: For plotting demand, stock, and production graphs
  - `numpy`: For numerical calculations
  - `streamlit`: For building the interactive web interface

## Installation

Follow these steps to get the project up and running:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fuzzy-tsukamoto-webapp.git
cd fuzzy-tsukamoto-webapp
```

### 2. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Copy the .env File
Copy the .env.example file to create a new .env file:
```bash
streamlit run fuzzy_tsukamoto_app.py
```

### 4. Run the app
Run the Streamlit web app:
```bash
php artisan key:generate
```

### 5. Open the app in your web browser at http://localhost:8501
