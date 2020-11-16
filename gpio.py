class _GPIO:
    def __init__(self):
        self.pins = [0,0,0,0,0,0,0,0]
    # Я внес изменение
    def output(self, pinId, level):
        if pinId < 0 or pinId > 7:
            print("Недопустимый номер светодиода:", pinId)
            return
        # А вот ещё одно изменение
        if 0 > level < 1:
            print("Недопустимый уровень светодиода:", level)
            return

        self.pins[pinId] = level
        print(self.pins)

GPIO = _GPIO()
