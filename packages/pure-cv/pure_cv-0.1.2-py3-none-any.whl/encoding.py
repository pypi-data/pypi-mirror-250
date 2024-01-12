import base64
import cv2 as cv
import numpy as np
import ramda as R

@R.curry
def b64encode(img: cv.Mat, format: str = ".png") -> str:
    """Encode `img` into a Base64 string"""
    _, encoded = cv.imencode(format, img)
    return base64.urlsafe_b64encode(encoded).decode("utf-8")

def b64decode(b64img: str) -> cv.Mat:
    b = base64.urlsafe_b64decode(b64img)
    arr = np.frombuffer(b, np.uint8)
    return cv.imdecode(arr, -1)
