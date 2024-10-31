from PyQt6.QtWidgets import QApplication
def copyText(text:str):
    app=QApplication
    clicknoard=app.clipboard()
    clicknoard.setText(text)
def paste()->str:
    app=QApplication
    clickboard=app.clipboard()
    return clickboard.text()