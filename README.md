# Student Attendance System

A comprehensive web application for managing student attendance using facial recognition technology. This system helps educational institutions to efficiently track student attendance through an automated face recognition process.

## Features

### For Students
- User-friendly dashboard with personal information
- View daily class schedule
- Attendance via facial recognition 
- View attendance history
- Update personal information
- Upload facial images for recognition training

### For Instructors
- View teaching schedule
- View student attendance records by course
- Search student information
- Generate attendance reports
- Manage personal information

## Technology Stack

- **Backend**: Django 5.1.7
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: MySQL
- **Face Recognition**: External API service
- **Storage**: Cloudinary (for image storage)

## Prerequisites

- Python 3.8+
- MySQL
- Cloudinary account

## Installation

1. Clone the repository:
```bash
https://github.com/bindut1/Student-Attendance.git
cd Student-Attendance
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
./venv/bin/activate  
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root directory with the following variables:
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

5. Configure the database in `student_attendance/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'student_attendance',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

6. Create the MySQL database:
```bash
mysql -u root -p
CREATE DATABASE student_attendance CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit
```

7. Run migrations:
```bash
python manage.py migrate
```

8. Create a superuser:
```bash
python manage.py createsuperuser
```

9. Run the development server:
```bash
python manage.py runserver
```

10. Access the application at http://127.0.0.1:8000/

## Project Structure

- `accounts/`: User account management
- `attendance/`: Attendance record management
- `courses/`: Course and schedule management
- `face_recognition/`: Facial recognition functionality
- `core/`: Core functionalities and helpers
- `static/`: Static files (CSS, JS)
- `templates/`: HTML templates
- `student_attendance/`: Project settings

## Usage

### Admin
- Access the admin panel at http://127.0.0.1:8000/admin/
- Create courses, instructors, and student accounts

### Student
- Log in with your credentials
- View your schedule
- Use the camera icon to mark attendance using facial recognition
- View your attendance history

### Instructor
- Log in with your credentials
- View your teaching schedule
- View and monitor student attendance for your courses

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [Cloudinary](https://cloudinary.com/)
