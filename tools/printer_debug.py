import win32print


def show_printers():

    print("=" * 70)
    print("ПРИНТЕРЫ WINDOWS")
    print("=" * 70)

    default = win32print.GetDefaultPrinter()

    print(f"\nПринтер по умолчанию:\n{default}\n")

    flags = (
        win32print.PRINTER_ENUM_LOCAL |
        win32print.PRINTER_ENUM_CONNECTIONS
    )

    printers = win32print.EnumPrinters(flags)

    for printer in printers:

        #
        # Структура:
        # (flags, description, name, comment)
        #

        name = printer[2]

        print("-" * 70)
        print(name)

        try:

            handle = win32print.OpenPrinter(name)

            info = win32print.GetPrinter(handle, 2)

            print("Driver :", info["pDriverName"])
            print("Port   :", info["pPortName"])
            print("Share  :", info["pShareName"])

            win32print.ClosePrinter(handle)

        except Exception as e:

            print(e)

    print("\n" + "=" * 70)


if __name__ == "__main__":

    show_printers()