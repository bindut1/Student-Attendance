from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, recipient_list, from_email=None):
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL
    
    try:
        sent = send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )
        return sent > 0
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_absence_warning_email(student, course):
    subject = f"Cảnh cáo vắng mặt môn học {course.course_name}"
    message = f"Chào {student.full_name},\n\nBạn đã vắng mặt quá 3 buổi học trong môn {course.course_name}. Vui lòng liên hệ giảng viên để giải quyết.\n\nTrân trọng."
    recipient_list = [student.email]
    
    return send_email(subject, message, recipient_list)
