normal_button_style = '''
QPushButton {
    color: rgb(131, 56, 236);
    background-color: white;
    border: 2px solid rgb(131, 56, 236);
    border-radius: 20px
}
QPushButton:hover {
    background-color: rgb(224, 206, 250);
}
QPushButton:disabled {
    color: rgb(205, 139, 240);
    background-color: rgb(244, 244, 244);
    border: 2px solid rgb(205, 139, 240);
    border-radius: 20px
}
'''

checkable_button_style = '''
QPushButton {
    color: rgb(131, 56, 236);
    background-color: white;
    border: 2px solid rgb(131, 56, 236);
    border-radius: 20px
}
QPushButton:hover {
    background-color: rgb(224, 206, 250);
}
QPushButton:checked {
    color: white;
    background-color: rgb(131, 56, 236);
    border: 2px solid white;
}
'''

small_button_style = '''
QPushButton {
    color: rgb(131, 56, 236);
    background-color: white;
    border: 2px solid rgb(131, 56, 236);
    border-radius: 10px
}
QPushButton:hover {
    background-color: rgb(224, 206, 250);
}
'''

dialog_button_box_button_style = '''
QDialogButtonBox.QPushButton {
    color: rgb(131, 56, 236);
    background-color: white;
    border: 2px solid rgb(131, 56, 236);
    border-radius: 5px
}
QDialogButtonBox.QPushButton:hover {
    background-color: rgb(224, 206, 250);
}
'''

dialog_style = '''
QDialog {
    background: white;
    border: 1px solid rgb(131, 56, 236);
    border-radius: 10px;
}
'''

main_window_style = '''
QMainWindow {
    background: white;
    border: 2px solid rgb(131, 56, 236);
    border-radius: 10px;
}
'''

message_box_style = '''
QMessageBox {
    background-color: white
}
'''
