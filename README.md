# NC3 E-Learning Platform

## Description

Welcome to the E-Learning Project repository! This Django-based project provides an extensive platform for online learning management. It integrates various features essential for e-learning systems including user management, course creation, and interactive learning tools.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.11
- PostgreSQL
- Poetry for dependency management

## Installation

Follow these steps to get your development environment running:

### 1. Clone the Repository

```bash
git clone https://github.com/NC3-LU/eLearning.git
cd eLearning
```

### 2. Initialize and Update Submodules

The project uses a Git submodule to manage the template. Initialize and update the submodule with the following commands:

```bash
git submodule init theme
git submodule update
```

### 3. Install Dependencies with Poetry

```bash
poetry install
```

### 4. Activate the Poetry Environment

```bash
poetry shell
```

### 5. Setup PostgreSQL Database

```bash
sudo -u postgres createdb $DB_NAME
sudo -u postgres psql -c "alter user $DB_USER with encrypted password '$DB_PASSWORD';" > /dev/null
sudo -u postgres psql -c "grant all privileges on database $DB_NAME to $DB_USER;" > /dev/null
```

Replace $DB_NAME with your database name, $DB_USER with your database username, and $DB_PASSWORD with your database password.

### 6. Configure the Project

Modify the config.py or config_dev.py file in the eLearning directory with your database settings and other configurations:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'elearning_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 7. Install Node Packages

```bash
npm install
```

### 8. Run Migrations

```bash
python manage.py migrate
```

### 9. Start the Development Server

```bash
python manage.py runserver
```

The development server will start at `http://127.0.0.1:8000/`.

## Usage

Once you have set up the project, you can:

- Access the admin panel at `http://127.0.0.1:8000/admin`.
- Create and manage courses and users through the admin panel.

## License

This software is licensed under the [GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html).
