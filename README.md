# Wizard's Codex

Wizard's Codex is an interactive platform designed to teach machine learning concepts in an engaging, wizard-themed environment. Aimed at making ML accessible to beginners, the project uses mini-games, challenges, and a captivating storyline to simplify complex concepts like data preprocessing, regression, and classification. Players take on the role of young wizards learning the art of machine learning to solve magical challenges and uncover mysteries.

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript, Three.js  
- **Backend:** Python (Django framework)  
- **Machine Learning:** Scikit-learn, TensorFlow  

## Installation

### Prerequisites

- Python 3.7+
- Node.js (for frontend dependency management)
- Git

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/NavySaw23/Wizards-Codex
   cd Wizards-codex
   cd WizCode
   ```

2. Set up the virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use env\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   npm install  # For frontend dependencies
   ```

4. Run migrations and start the server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
