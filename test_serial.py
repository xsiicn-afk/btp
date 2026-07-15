from services.serial_number_generator import SerialNumberGenerator

generator = SerialNumberGenerator()

print("Текущий номер:", generator.current())
print("Новый номер:", generator.next())
print("Следующий номер:", generator.next())