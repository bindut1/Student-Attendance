from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from face_recognition.services.ai_service import AIService
from django.views.decorators.http import require_POST
import json
from attendance.models import Course, Attendance, Account
from datetime import datetime
import math
from django.shortcuts import redirect
from django.contrib import messages

@require_POST
def upload_training_images(request, account_id):
    ai_service = AIService()
    try:
        image_files = request.FILES.getlist("images")
        if not image_files:
            messages.error(request, "Không có ảnh nào được gửi.")
            return redirect("accounts:student_info")  

        response = ai_service.send_images(account_id, image_files)
        if response.get("message"):
            messages.success(request, "Đã tải lên và xử lý khuôn mặt thành công.")
        else:
            error_message = response.get("error", "Lỗi không xác định")
            messages.error(request, f"Gửi ảnh thất bại: {error_message}")

        return redirect("accounts:student_info") 
    except Exception as e:
        messages.error(request, f"Lỗi khi gửi ảnh: {str(e)}")
        return redirect("accounts:student_info")  


# Hàm tính khoảng cách giữa hai tọa độ sử dụng công thức Haversine
def tinh_khoang_cach(lat1, lon1, lat2, lon2):
    """Tính khoảng cách giữa hai tọa độ theo mét"""
    # Bán kính Trái Đất tính theo mét
    R = 6371000

    # Chuyển đổi sang radian
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Độ chênh lệch
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Công thức Haversine
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance


@require_POST
def verify_face_for_attendance(request):
    ai_service = AIService()

    try:
        data = json.loads(request.body)
        image_data = data.get("image")
        course_id = data.get("course_id")

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        account_id = data.get(
            "account_id",
            (
                request.user.account_id
                if hasattr(request, "user") and request.user.is_authenticated
                else None
            ),
        )

        if not image_data:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Thiếu dữ liệu: cần cung cấp ảnh khuôn mặt",
                }
            )

        if not account_id:
            return JsonResponse(
                {"success": False, "message": "Không có thông tin tài khoản người dùng"}
            )

        if latitude is not None and longitude is not None:
            bach_khoa_lat = 16.073844
            bach_khoa_lon = 108.149409

            khoang_cach_toi_da = 3000

            khoang_cach = tinh_khoang_cach(
                float(latitude), float(longitude), bach_khoa_lat, bach_khoa_lon
            )
            print("Khoang cach: ", khoang_cach)

            if khoang_cach > khoang_cach_toi_da:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Điểm danh thất bại: Bạn không ở trong khuôn viên trường",
                        "distance": khoang_cach,
                        "max_allowed": khoang_cach_toi_da,
                    }
                )

        recognition_result = ai_service.verify_face(image_data, account_id)
        print("Recognition result:", recognition_result)

        if (recognition_result.get("message") is True) or (
            recognition_result.get("success") is True
        ):
            try:
                student = Account.objects.get(account_id=account_id)
                course = Course.objects.get(course_id=course_id)
                current_time = datetime.now().time()
                current_date = datetime.now().date()

                attendance_id = f"{student.account_id}_{course.course_id}_{current_date.strftime('%Y%m%d')}"

                if Attendance.objects.filter(attendance_id=attendance_id).exists():
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "Đã điểm danh thành công trước đó",
                            "student_name": student.full_name,
                            "already_attended": True,
                        }
                    )

                attendance = Attendance(
                    attendance_id=attendance_id,
                    student=student,
                    course=course,
                    check_in_date=current_date,
                    check_in_time=current_time,
                    check_in_latitude=latitude,
                    check_in_longitude=longitude,
                )
                attendance.save()

                return JsonResponse(
                    {
                        "success": True,
                        "message": "Điểm danh thành công",
                        "student_name": student.full_name,
                        "already_attended": False,
                    }
                )

            except Account.DoesNotExist:
                return JsonResponse(
                    {
                        "success": False,
                        "message": f"Không tìm thấy sinh viên với ID: {account_id}",
                    }
                )
            except Course.DoesNotExist:
                return JsonResponse(
                    {
                        "success": False,
                        "message": f"Không tìm thấy khóa học với ID: {course_id}",
                    }
                )
            except Exception as e:
                return JsonResponse(
                    {"success": False, "message": f"Lỗi khi lưu điểm danh: {str(e)}"}
                )
        else:
            error_message = recognition_result.get(
                "error", "Không nhận diện được khuôn mặt"
            )
            return JsonResponse({"success": False, "message": error_message})

    except Exception as e:
        return JsonResponse({"success": False, "message": f"Lỗi: {str(e)}"})
