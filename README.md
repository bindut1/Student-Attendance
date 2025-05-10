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

## Project Structure

- `accounts/`: User account management
- `attendance/`: Attendance record management
- `courses/`: Course and schedule management
- `face_recognition/`: Facial recognition functionality
- `core/`: Core functionalities and helpers
- `static/`: Static files (CSS, JS)
- `templates/`: HTML templates
- `student_attendance/`: Project settings

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [Cloudinary](https://cloudinary.com/)
