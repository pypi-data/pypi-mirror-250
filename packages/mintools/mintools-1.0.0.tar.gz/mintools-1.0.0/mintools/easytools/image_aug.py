import cv2


def clahe(img, clipLimit=2.0, tileGridSize=(8, 8)):
    b, g, r = cv2.split(img)
    clahe_op = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
    b, g, r = clahe_op.apply(b), clahe_op.apply(g), clahe_op.apply(r)
    img_clahe = cv2.merge([b, g, r])
    return img_clahe
