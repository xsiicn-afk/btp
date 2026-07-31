import win32print


def installed_printers() -> list[str]:
    """
    Возвращает список установленных принтеров.
    """

    result = []

    flags = (
        win32print.PRINTER_ENUM_LOCAL
        | win32print.PRINTER_ENUM_CONNECTIONS
    )

    for printer in win32print.EnumPrinters(flags):

        #
        # Структура:
        # (flags, description, name, comment)
        #

        result.append(printer[2])

    result.sort()

    return result


# ---------------------------------------------------------


def default_printer() -> str:

    try:

        return win32print.GetDefaultPrinter()

    except Exception:

        return ""


# ---------------------------------------------------------


def excel_printer_name(
    printer_name: str,
) -> str | None:
    """
    Преобразует обычное имя принтера
    в строку, которую понимает Excel.

    Например

        Xerox Phaser 3160

    →

        Xerox Phaser 3160 on USB001:
    """

    if not printer_name:

        return None

    flags = (
        win32print.PRINTER_ENUM_LOCAL
        | win32print.PRINTER_ENUM_CONNECTIONS
    )

    for printer in win32print.EnumPrinters(flags):

        name = printer[2]

        if name != printer_name:
            continue

        try:

            handle = win32print.OpenPrinter(name)

            info = win32print.GetPrinter(
                handle,
                2,
            )

            win32print.ClosePrinter(handle)

            port = info["pPortName"]

            return f"{name} on {port}:"

        except Exception:

            return None

    return None

#---------------------------------------------------------
import contextlib


# ---------------------------------------------------------


def set_default_printer(
    printer_name: str,
) -> bool:

    try:

        win32print.SetDefaultPrinter(
            printer_name
        )

        return True

    except Exception:

        return False


# ---------------------------------------------------------


@contextlib.contextmanager
def temporary_default_printer(
    printer_name: str,
):

    old_printer = default_printer()

    changed = False

    try:

        if (
            printer_name
            and printer_name != old_printer
        ):

            changed = set_default_printer(
                printer_name
            )

        yield

    finally:

        if (
            changed
            and old_printer
        ):

            set_default_printer(
                old_printer
            )
