import PySimpleGUI as sg
from settings import Config

sg.theme(Config.gui.theme_name)

projection_layout = [
    [sg.Text("Choose a file for projection"),
     sg.In(size=(40, 1), enable_events=True, key="FILE"),
     sg.FileBrowse(),
     sg.Submit()],
    [sg.Column([[sg.Image(key="ORIGINAL", size=Config.gui.display_size)],
                [sg.Text("Original Image")]]),
     sg.Column([[sg.Image(key="ALIGNED", size=Config.gui.display_size)],
                [sg.Text("Aligned Image")]]),
     sg.Column([[sg.Image(key="PROJECTED", size=Config.gui.display_size)],
                [sg.Text("Projected Image")]])]
]
