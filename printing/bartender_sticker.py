from datetime import datetime
from pathlib import Path

import pythoncom
import win32com.client

from models.label_model import LabelModel


class BarTenderSticker:
    """
    Печать производственной этикетки
    через BarTender COM Automation.
    """

    def __init__(
        self,
        template: str,
        bartender: str | None = None,
    ):

        self.template = Path(template)

        self.bartender = (
            Path(bartender)
            if bartender
            else None
        )

        self._app = None
        self._format = None
        self._com_initialized = False

        if not self.template.exists():

            raise FileNotFoundError(
                f"Не найден шаблон BarTender: "
                f"{self.template}"
            )

    # ---------------------------------------------------------

    def _initialize_com(self):

        if self._com_initialized:
            return

        pythoncom.CoInitialize()

        self._com_initialized = True

    # ---------------------------------------------------------

    def _uninitialize_com(self):

        if not self._com_initialized:
            return

        try:

            pythoncom.CoUninitialize()

        finally:

            self._com_initialized = False

    # ---------------------------------------------------------

    def _start_bartender(self):

        if self._app is not None:
            return

        self._initialize_com()

        try:

            self._app = (
                win32com.client.Dispatch(
                    "BarTender.Application"
                )
            )

            self._app.Visible = False

        except Exception:

            self._app = None

            self._uninitialize_com()

            raise

    # ---------------------------------------------------------

    def _open_template(self):

        if self._format is not None:
            return

        self._start_bartender()

        template_path = str(
            self.template.resolve()
        )

        try:

            self._format = (
                self._app.Formats.Open(
                    template_path,
                    False,
                    "",
                )
            )

        except Exception:

            self._format = None

            raise

    # ---------------------------------------------------------

    @staticmethod
    def _text(
        value,
    ) -> str:

        if value is None:
            return ""

        return str(value)

    # ---------------------------------------------------------

    @staticmethod
    def _format_date(
        value,
    ) -> str:
        """
        Преобразует дату производства
        в формат месяц/год для наклейки.

        Например:

            29.07.2026 -> 07.2026
            2026-07-29 -> 07.2026
            29/07/2026 -> 07.2026
        """

        if value is None:
            return ""

        value = str(value).strip()

        if not value:
            return ""

        formats = (
            "%d.%m.%Y",
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%d-%m-%Y",
        )

        for date_format in formats:

            try:

                parsed = datetime.strptime(
                    value,
                    date_format,
                )

                return parsed.strftime(
                    "%m.%Y"
                )

            except ValueError:
                continue

        return value

    # ---------------------------------------------------------

    def _set_value(
        self,
        name: str,
        value,
    ):

        value = self._text(
            value
        )

        self._format.SetNamedSubStringValue(
            name,
            value,
        )

    # ---------------------------------------------------------

    def _fill(
        self,
        label: LabelModel,
    ):

        self._set_value(
            "TITLE",
            getattr(
                label,
                "model_name",
                "",
            ),
        )

        self._set_value(
            "SERIAL",
            label.serial,
        )

        self._set_value(
            "ARTICLE",
            label.article_code,
        )

        self._set_value(
            "DATE",
            self._format_date(
                label.date
            ),
        )

        # ---------------------------------------------------------

    def print(
        self,
        label: LabelModel,
        printer_name: str | None = None,
    ):

        self._open_template()

        self._fill(
            label
        )

        if printer_name:

            try:

                self._format.Printer = (
                    printer_name
                )

            except Exception:
                pass

        result = self._format.PrintOut(
            False,
            False,
        )

        return result

    # ---------------------------------------------------------

    def close(self):

        if self._format is not None:

            try:

                self._format.Close(
                    1,
                )

            except Exception:
                pass

            finally:

                self._format = None

        if self._app is not None:

            try:

                self._app.Quit(
                    1,
                )

            except Exception:
                pass

            finally:

                self._app = None

        self._uninitialize_com()

    # ---------------------------------------------------------

    def __enter__(self):

        return self

    # ---------------------------------------------------------

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):

        self.close()

    # ---------------------------------------------------------

    def __del__(self):

        try:

            self.close()

        except Exception:
            pass