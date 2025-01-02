from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey, EllipticCurvePublicKey
from cryptography.hazmat.primitives import serialization


class UsersDB:
    users_list = [{"user": "mario", "password": "mario1"}, {"user": "peach", "password": "peach1"}]
    user_private_keys = []  # Danh sách lưu thông tin private key
    user_public_keys = []   # Danh sách lưu thông tin public key

    def read_db(self, user_name: str, password: str) -> bool:
        """Kiểm tra thông tin đăng nhập"""
        for user in self.users_list:
            if user["user"] == user_name and user["password"] == password:
                return True
        return False

    def write_db(self, user_name: str, password: str) -> bool:
        """Thêm người dùng mới vào cơ sở dữ liệu"""
        self.users_list.append({"user": user_name, "password": password})
        return True

    def write_private_key(self, user_name: str, private_key: EllipticCurvePrivateKey) -> bool:
        """Lưu khóa bí mật vào cơ sở dữ liệu"""
        self.user_private_keys.append({"user": user_name, "private_key": private_key})
        return True

    def read_private_key(self, user_name: str) -> EllipticCurvePrivateKey:
        """Đọc khóa bí mật của người dùng"""
        for key_data in self.user_private_keys:
            if key_data["user"] == user_name:
                return key_data["private_key"]
        return None

    def write_public_key(self, user_name: str, public_key: EllipticCurvePublicKey) -> bool:
        """Lưu khóa công khai vào cơ sở dữ liệu"""
        self.user_public_keys.append({"user": user_name, "public_key": public_key})
        return True

    def read_public_key(self, user_name: str) -> EllipticCurvePublicKey:
        """Đọc khóa công khai của người dùng"""
        for key_data in self.user_public_keys:
            if key_data["user"] == user_name:
                return key_data["public_key"]
        return None
