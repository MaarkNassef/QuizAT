# QuizAT

## Project Overview

**QuizAT** is a Django-based project designed to facilitate the management of quizzes, groups, and user accounts. It comprises several interconnected apps, each serving a specific purpose to enhance the overall functionality of the system.

### Apps Overview:

1. **groups**: Manages group creation, membership, invitations, and related functionalities.
2. **accounts**: Handles user authentication and registration.
3. **main**: Provides the main dashboard functionality, displaying relevant information based on the user's role.
4. **quizzes**: Facilitates the creation, management, and grading of quizzes associated with specific groups.

## Setup Instructions

### Steps:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/MaarkNassef/QuizAT
```

2. Navigate to the project directory:

```bash
cd mysite
```

3. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

4. Perform database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser to access the Django admin interface:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Access the application by navigating to `http://localhost:8000` in your web browser.

## App-Specific Details

### 1. Groups App

- **Views**: Manages group creation, detail view, deletion, invitations, membership, and related functionalities.

### 2. Accounts App

- **Views**: Handles user registration and authentication.

### 3. Main App

- **Views**: Provides the main dashboard functionality, displaying relevant information based on the user's role.

### 4. Quizzes App

- **Views**: Manages quiz creation, detail view, question management, grading, and related functionalities. Additionally, teachers can download CSV files containing quiz grades.

## Contributors

- [Mark Nassef](https://github.com/MaarkNassef)

## License

This project is licensed under the [MIT License](LICENSE).
