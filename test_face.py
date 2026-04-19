import face_recognition
import cv2

def load_and_encode_opencv_image(path):
    try:
        # Load with OpenCV (BGR format), convert to RGB
        bgr_image = cv2.imread(path)
        if bgr_image is None:
            print("❌ Failed to load image.")
            return

        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

        print(f"✅ OpenCV image shape: {rgb_image.shape}, dtype: {rgb_image.dtype}, contiguous: {rgb_image.flags['C_CONTIGUOUS']}")

        # Try face encoding
        encodings = face_recognition.face_encodings(rgb_image)
        if not encodings:
            print("❌ No faces found in the image.")
        else:
            print("✅ Face encoding generated successfully.")

    except Exception as e:
        print(f"❌ Exception occurred: {e}")

load_and_encode_opencv_image("known_face_fixed.jpg")

