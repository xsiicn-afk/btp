from printing.excel_com import ExcelCom
from models.label_model import LabelModel

label = LabelModel()

label.title = "ЭпикумЛаб Тест"
label.serial = "260700001"
label.model_name = "ЭпикумЛаб Office i5-12400"
label.article = "101345"
label.date = "08.07.2026"

excel = ExcelCom()

excel.open("resources/templates/Спецификация.xlsx")

excel.write_label(label)

excel.save_as("test.xlsx")

excel.close()

print("OK")