document.addEventListener('DOMContentLoaded', function () {
    if (!document.querySelector('link[href*="font-awesome"]')) {
        const fontAwesome = document.createElement('link');
        fontAwesome.rel = 'stylesheet';
        fontAwesome.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css';
        document.head.appendChild(fontAwesome);
    }

    const cameraModal = new bootstrap.Modal(document.getElementById('cameraModal'));
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const capturedImage = document.getElementById('capturedImage');
    const captureBtn = document.getElementById('captureBtn');
    const submitBtn = document.getElementById('submitBtn');
    const retakeBtn = document.getElementById('retakeBtn');
    const statusMessage = document.getElementById('status-message');

    let stream = null;
    let currentCourseId = null;

    function layViTriNguoiDung() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error("Trình duyệt không hỗ trợ định vị"));
                return;
            }

            navigator.geolocation.getCurrentPosition(
                (position) => {
                    resolve({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude
                    });
                },
                (error) => {
                    switch (error.code) {
                        case error.PERMISSION_DENIED:
                            reject(new Error("Người dùng từ chối cho phép định vị"));
                            break;
                        case error.POSITION_UNAVAILABLE:
                            reject(new Error("Thông tin vị trí không khả dụng"));
                            break;
                        case error.TIMEOUT:
                            reject(new Error("Yêu cầu vị trí đã hết thời gian"));
                            break;
                        default:
                            reject(new Error("Lỗi không xác định"));
                            break;
                    }
                },
                { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
            );
        });
    }

    document.querySelectorAll('.open-camera-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            currentCourseId = this.dataset.course;
            openCamera();
            cameraModal.show();
        });
    });

    function openCamera() {
        navigator.mediaDevices.getUserMedia({ video: true, audio: false })
            .then(function (mediaStream) {
                stream = mediaStream;
                video.srcObject = mediaStream;
                video.play();

                capturedImage.style.display = 'none';
                video.style.display = 'block';
                captureBtn.classList.remove('d-none');
                submitBtn.classList.add('d-none');
                retakeBtn.classList.add('d-none');
                statusMessage.classList.add('d-none');
            })
            .catch(function (err) {
                console.log("Error accessing camera: " + err);
                statusMessage.textContent = "Không thể truy cập camera. Vui lòng kiểm tra quyền truy cập.";
                statusMessage.classList.remove('d-none');
                statusMessage.classList.remove('alert-info');
                statusMessage.classList.add('alert-danger');
            });
    }

    captureBtn.addEventListener('click', function () {
        const context = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        capturedImage.src = canvas.toDataURL('image/png');
        capturedImage.style.display = 'block';
        video.style.display = 'none';

        captureBtn.classList.add('d-none');
        submitBtn.classList.remove('d-none');
        retakeBtn.classList.remove('d-none');
    });

    retakeBtn.addEventListener('click', function () {
        capturedImage.style.display = 'none';
        video.style.display = 'block';
        captureBtn.classList.remove('d-none');
        submitBtn.classList.add('d-none');
        retakeBtn.classList.add('d-none');
    });

    submitBtn.addEventListener('click', async function () {
        statusMessage.textContent = "Đang xử lý...";
        statusMessage.classList.remove('d-none');
        statusMessage.classList.add('alert-info');

        let currentAccountId = null;
        const pathname = window.location.pathname;
        const pathParts = pathname.split('/');

        const studentIndex = pathParts.indexOf('student');
        if (studentIndex !== -1 && pathParts.length > studentIndex + 1) {
            currentAccountId = pathParts[studentIndex + 1];
        }
        const imageData = canvas.toDataURL('image/png');
        try {
            const viTri = await layViTriNguoiDung();

            fetch('/face_recognition/api/facial_recognition/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    image: imageData,
                    account_id: currentAccountId,
                    course_id: currentCourseId,
                    latitude: viTri.latitude,
                    longitude: viTri.longitude
                })
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok: ' + response.status);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        statusMessage.textContent = `Điểm danh thành công! Xin chào ${data.student_name || 'bạn'}`;
                        statusMessage.classList.remove('alert-info', 'alert-danger');
                        statusMessage.classList.add('alert-success');

                        setTimeout(() => {
                            cameraModal.hide();
                            location.reload();
                        }, 2000);
                    } else {
                        statusMessage.textContent = data.message || "Không nhận diện được khuôn mặt. Vui lòng thử lại.";
                        statusMessage.classList.remove('alert-info', 'alert-success');
                        statusMessage.classList.add('alert-danger');
                    }
                })
                .catch(error => {
                    statusMessage.textContent = "Lỗi kết nối: " + error.message;
                    statusMessage.classList.remove('alert-info', 'alert-success');
                    statusMessage.classList.add('alert-danger');
                    console.error('Error:', error);
                });
        } catch (error) {
            statusMessage.textContent = "Lỗi lấy vị trí: " + error.message + ". Vui lòng bật định vị và cho phép truy cập.";
            statusMessage.classList.remove('alert-info', 'alert-success');
            statusMessage.classList.add('alert-danger');
            console.error('Geolocation Error:', error);
        }
    });

    document.getElementById('cameraModal').addEventListener('hidden.bs.modal', function () {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

});