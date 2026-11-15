import json
from pathlib import Path
from typing import Any


class JsonStore:
    """Small JSON storage layer that can later be swapped for MongoDB repositories."""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.users_path = data_dir / "users.json"
        self.careers_path = data_dir / "careers.json"

    def _read_json(self, path: Path, default: Any) -> Any:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            self._write_json(path, default)
            return default

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
                return data if data is not None else default
        except json.JSONDecodeError:
            return default

    def _write_json(self, path: Path, data: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    def read_users(self) -> list[dict[str, Any]]:
        return self._read_json(self.users_path, [])

    def write_users(self, users: list[dict[str, Any]]) -> None:
        self._write_json(self.users_path, users)

    def read_careers(self) -> dict[str, Any]:
        return self._read_json(self.careers_path, {})

    def find_user_by_email(self, email: str) -> dict[str, Any] | None:
        return next((user for user in self.read_users() if user["email"] == email), None)

    def find_user_by_id(self, user_id: str) -> dict[str, Any] | None:
        return next((user for user in self.read_users() if user["id"] == user_id), None)

    def save_user(self, updated_user: dict[str, Any]) -> None:
        users = self.read_users()
        for index, user in enumerate(users):
            if user["id"] == updated_user["id"]:
                users[index] = updated_user
                self.write_users(users)
                return
        users.append(updated_user)
        self.write_users(users)


store = JsonStore(Path(__file__).resolve().parents[1] / "data")
