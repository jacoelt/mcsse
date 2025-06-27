import os
import time


PATH = os.path.join(os.path.dirname(__file__), "files")


def secure_string_for_filename(s: str) -> str:
    """Replace characters that are not allowed in filenames with underscores."""
    return (
        "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in s).strip()
        + ".cache"
    )


class Cache:
    def __init__(self, expire_after_sec: int = None):
        self.expire_after = expire_after_sec

        if not os.path.exists(PATH):
            os.makedirs(PATH)

    def _get_file_path(self, key):
        """Generate a secure file path for the given key."""
        key = secure_string_for_filename(key)
        return os.path.join(PATH, f"{key}")

    def get(self, key, default=None, ignore_expiry=False):
        file_path = self._get_file_path(key)

        if not os.path.exists(file_path):
            return default

        created_at = os.path.getmtime(file_path)
        if (
            not ignore_expiry
            and self.expire_after
            and time.time() - created_at > self.expire_after
        ):
            return default

        with open(file_path, "r", encoding="utf-8") as file:
            value = file.read()

        return value

    def set(self, key, value):
        if not isinstance(value, str):
            raise ValueError("Value must be a string")

        file_path = self._get_file_path(key)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(value)

    def delete(self, key):
        file_path = self._get_file_path(key)

        if os.path.exists(file_path):
            os.remove(file_path)

    def clear(self):
        for file_name in os.listdir(PATH):
            file_path = os.path.join(PATH, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
