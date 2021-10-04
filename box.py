# test
# box color
class Box:
    isObjectInPosition = False

    def objectDetected(self):
        boxColor = (102, 204, 102) if self.isObjectInPosition else (0, 0, 255)
