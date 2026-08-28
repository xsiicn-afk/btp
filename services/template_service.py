from pathlib import Path
import json

from services.settings_service import SettingsService


class TemplateService:
    """
    Управление наборами шаблонов.

    Каждый профиль представляет собой папку:

    resources/templates/<профиль>/

    содержащую:

        spec_v2.xlsx
        pass.xls (или pass.xlsx)
        sticker.btw
        profile.json
    """

    def __init__(self):

        self.settings = SettingsService()

        self.templates_root = (
            Path("resources")
            / "templates"
        )

    # ---------------------------------------------------------

    def profiles(self) -> list[str]:
        """
        Возвращает список имён папок профилей.
        """

        if not self.templates_root.exists():
            return ["ByTop PE"]

        result = sorted(
            [
                folder.name
                for folder in self.templates_root.iterdir()
                if folder.is_dir()
            ]
        )

        if not result:
            result = ["ByTop PE"]

        return result

    # ---------------------------------------------------------

    def current_profile(self) -> str:

        profile = (
            self.settings.get_template_profile()
        )

        if not profile:
            profile = "ByTop PE"

        if profile not in self.profiles():
            profile = "ByTop PE"

        return profile

    # ---------------------------------------------------------

    def profile_path(self) -> Path:

        return (
            self.templates_root
            / self.current_profile()
        )

    # ---------------------------------------------------------

    def profile_info(
        self,
        profile: str | None = None,
    ) -> dict:
        """
        Читает profile.json указанного профиля.

        Если profile=None —
        используется текущий профиль.
        """

        if profile is None:
            profile = self.current_profile()

        info = {
            "name": profile,
            "model_prefix": f"Системный блок {profile}",
        }

        profile_json = (
            self.templates_root
            / profile
            / "profile.json"
        )

        if not profile_json.exists():
            return info

        try:

            data = json.loads(
                profile_json.read_text(
                    encoding="utf-8"
                )
            )

            if data.get("name"):
                info["name"] = data["name"]

            if data.get("model_prefix"):
                info["model_prefix"] = data["model_prefix"]

        except Exception:
            pass

        return info
    
    # ---------------------------------------------------------

    def display_name(self) -> str:
        """
        Красивое имя профиля.
        """

        return self.profile_info()["name"]

    # ---------------------------------------------------------

    def model_prefix(self) -> str:
        """
        Префикс названия изделия.
        """

        return self.profile_info()["model_prefix"]

    # ---------------------------------------------------------

    def spec(self) -> Path:

        profile = self.profile_path()

        new = profile / "spec_100x150.xlsx"

        if new.exists():
            return new

        old = profile / "spec_v2.xlsx"

        if old.exists():
            return old

        return new

    # ---------------------------------------------------------

    def passport(self) -> Path:

        profile = self.profile_path()

        xls = profile / "pass.xls"

        if xls.exists():
            return xls

        xlsx = profile / "pass.xlsx"

        if xlsx.exists():
            return xlsx

        return xls

    # ---------------------------------------------------------

    def sticker(self) -> Path:

        return (
            self.profile_path()
            / "sticker.btw"
        )