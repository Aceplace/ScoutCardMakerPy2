import traceback

import xlrd as xl
from tkinter import *
from misc.exceptions import ExportException


def get_script_from_excel_file(root, file_name):

    try:
        work_book = xl.open_workbook(file_name)

        if work_book.nsheets == 1:
            sheet = work_book.sheet_by_index(0)
        else:
            sheet_name = ChooseExcelSheetDialog(root, work_book.sheet_names()).show()
            sheet = work_book.sheet_by_name(sheet_name)

        plays = []
        for index in range(1, sheet.nrows):
            row_values = sheet.row_values(index)
            play_info = {}
            play_info['Number'] = int(row_values[0])
            play_info['Hash'] = row_values[1]
            play_info['Dnd'] = row_values[2]
            play_info['Formation'] = row_values[3]
            play_info['Play'] = row_values[4]
            play_info['Defense'] = row_values[5]
            play_info['Note'] = row_values[6]
            play_info['Card Maker Formation'] = row_values[7].strip().upper()
            play_info['Card Maker Defense'] = row_values[8].strip().upper()
            plays.append(play_info)
    except IOError as e:
        raise ExportException(str(e))
    except Exception:
        traceback.print_exc()
        raise ExportException('Excel sheet incorrectly formatted.')

    return plays


class ChooseExcelSheetDialog(Toplevel):
    def __init__(self, root, sheet_names):
        Toplevel.__init__(self, root)

        Label(self, text='Choose Sheet').pack()
        for sheet_name in sheet_names:
            button = Button(self, text=sheet_name)
            button.pack()
            button.bind('<Button-1>',self.choose_sheet)

    def choose_sheet(self, event):
        self.chosen_sheet = event.widget.cget('text')
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.wait_window()
        return self.chosen_sheet

