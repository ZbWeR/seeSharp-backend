import os
import cv2
import numpy as np
import face_recognition as fc
from app.utils import generate_unique_id, singleton


def resize_image(image, target_height=480):
    """
    调整图片大小。
    """
    height, width = image.shape[:2]
    scale = target_height / height
    return cv2.resize(image, (int(width * scale), int(height * scale)))


@singleton
class FaceManager:

    def __init__(self, known_faces_dir=None):
        if known_faces_dir is not None:
            self.known_faces_dir = known_faces_dir
            self.known_faces = self._load_known_faces()

    def _load_known_faces(self):
        """
        从指定目录加载已知人脸的编码和对应名称。

        返回:
            dict: 包含两个列表的字典，分别为已知人脸的编码（"encodings"）和对应的名称（"names"）。
        """
        known_face_encodings = []
        known_face_names = []
        legal_file_types = (".jpg", ".jpeg", ".png")

        # 目录不存在则创建
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)

        for file in os.listdir(self.known_faces_dir):
            if file.lower().endswith(legal_file_types):
                file_path = os.path.join(self.known_faces_dir, file)
                face_encoding = self._extract_face_encoding(file_path)
                if face_encoding is not None:
                    known_face_encodings.append(face_encoding)
                    known_face_names.append(os.path.splitext(file)[0])
        print("✔️ loaded known faces.")
        return {"encodings": known_face_encodings, "names": known_face_names}

    def _extract_face_encoding(self, image_path):
        """
        从给定的图片路径中提取人脸编码。如果图片中包含多张人脸，只提取第一张。
        """
        try:
            face_image = fc.load_image_file(image_path)
            return fc.face_encodings(face_image)[0]
        except Exception as e:
            print(f"❌ failed to extract face encoding: {e}")
            return None

    def _save_face(self, blob_data, face_name):
        """
        将二进制人脸数据保存为图片文件，并返回文件路径。
        """
        image = cv2.imdecode(np.frombuffer(blob_data, np.uint8), cv2.IMREAD_COLOR)
        resized_image = resize_image(image)
        image_filename = f"{face_name}.jpg"
        image_path = os.path.join(self.known_faces_dir, image_filename)
        cv2.imwrite(image_path, resized_image)
        return image_path

    def add_new_face(self, blob_data, file_name):
        """
        添加新的人脸至已知人脸列表。
        """
        face_name = os.path.splitext(file_name)[0]
        image_path = self._save_face(blob_data, face_name)
        face_encoding = self._extract_face_encoding(image_path)
        if face_encoding is not None:
            self.known_faces["encodings"].append(face_encoding)
            self.known_faces["names"].append(face_name)
            return True
        else:
            # 删除无效图片
            if os.path.exists(image_path):
                os.remove(image_path)
            return False

    def recognize_face(self, blob_data):
        """
        根据输入的人脸数据识别该人脸是否为已知人脸，并返回匹配的名称。
        """
        # 保存未知人脸图片并提取编码
        unique_name = generate_unique_id("unknown")
        unknown_image_path = self._save_face(blob_data, unique_name)
        unknown_encoding = self._extract_face_encoding(unknown_image_path)
        # 删除临时图片
        if os.path.exists(unknown_image_path):
            os.remove(unknown_image_path)
        # 查找匹配的已知人脸
        if unknown_encoding is not None:
            matches = self._find_matches(unknown_encoding)
            if matches:
                return matches
        return None

    def _find_matches(self, unknown_encoding):
        """
        在已知人脸列表中查找与给定未知人脸编码相匹配的人脸。
        """
        results = fc.compare_faces(self.known_faces["encodings"], unknown_encoding)
        matches = []
        for i, (match, name) in enumerate(zip(results, self.known_faces["names"])):
            if match:
                matches.append(name)
        return matches

    def get_known_faces(self):
        """
        返回已知人脸的名称列表。
        """
        return self.known_faces["names"]
