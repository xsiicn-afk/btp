from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen

from models.label_model import LabelModel


class LabelRenderer:
    """
    Универсальный рендерер спецификации.

    Все размеры вычисляются относительно области печати,
    поэтому Preview, PDF и принтер будут выглядеть одинаково.
    """

    def render(
        self,
        painter: QPainter,
        rect: QRectF,
        label: LabelModel,
    ):

        painter.save()

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        painter.fillRect(rect, QColor("white"))

        border = max(1.0, rect.width() * 0.002)

        painter.setPen(QPen(Qt.black, border))
        painter.drawRect(rect)

        margin = rect.width() * 0.04

        work = rect.adjusted(
            margin,
            margin,
            -margin,
            -margin,
        )

        title_font = max(12, int(work.width() * 0.028))
        header_font = max(9, int(work.width() * 0.020))
        text_font = max(8, int(work.width() * 0.018))
        small_font = max(7, int(work.width() * 0.015))

        row_height = work.height() * 0.060
        section_gap = work.height() * 0.020

        y = work.top()

        # -------------------------------------------------
        # Заголовок
        # -------------------------------------------------

        painter.setFont(QFont("Arial", title_font, QFont.Bold))

        painter.drawText(
            QRectF(
                work.left(),
                y,
                work.width(),
                row_height,
            ),
            Qt.AlignCenter,
            label.title,
        )

        y += row_height + section_gap

        painter.setFont(QFont("Arial", header_font))

        painter.drawText(
            QRectF(work.left(), y, work.width(), row_height),
            Qt.AlignLeft | Qt.AlignVCenter,
            f"Модель: {label.model_name}",
        )

        y += row_height

        painter.drawText(
            QRectF(work.left(), y, work.width(), row_height),
            Qt.AlignLeft | Qt.AlignVCenter,
            f"Серийный номер: {label.serial}",
        )

        y += row_height

        painter.drawText(
            QRectF(work.left(), y, work.width(), row_height),
            Qt.AlignLeft | Qt.AlignVCenter,
            f"Артикул: {label.article}",
        )

        y += row_height

        painter.drawText(
            QRectF(work.left(), y, work.width(), row_height),
            Qt.AlignLeft | Qt.AlignVCenter,
            f"Дата производства: {label.date}",
        )

        y += row_height

        painter.drawLine(
            work.left(),
            y,
            work.right(),
            y,
        )

        y += section_gap

        # -------------------------------------------------
        # Заголовок спецификации
        # -------------------------------------------------

        painter.setFont(QFont("Arial", header_font, QFont.Bold))

        painter.drawText(
            QRectF(
                work.left(),
                y,
                work.width(),
                row_height,
            ),
            Qt.AlignCenter,
            "СПЕЦИФИКАЦИЯ",
        )

        y += row_height + section_gap

        left_width = work.width() * 0.28
        right_width = work.width() - left_width

        # -------------------------------------------------
        # Комплектующие
        # -------------------------------------------------

        for title, value in label.specification:

            if not value:
                continue

            painter.setFont(QFont("Arial", text_font, QFont.Bold))

            painter.drawText(
                QRectF(
                    work.left(),
                    y,
                    left_width,
                    row_height,
                ),
                Qt.AlignLeft | Qt.AlignTop,
                title,
            )

            painter.setFont(QFont("Arial", text_font))

            text_rect = QRectF(
                work.left() + left_width,
                y,
                right_width,
                row_height * 2,
            )

            painter.drawText(
                text_rect,
                Qt.AlignLeft | Qt.TextWordWrap,
                value,
            )

            y += row_height * 1.5

        painter.drawLine(
            work.left(),
            y,
            work.right(),
            y,
        )

        y += section_gap

        painter.setFont(QFont("Arial", small_font))

        painter.drawText(
            QRectF(
                work.left(),
                y,
                work.width(),
                row_height,
            ),
            Qt.AlignCenter,
            "ByTop Production Suite",
        )

        painter.restore()