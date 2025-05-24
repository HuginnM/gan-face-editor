import FreeSimpleGUI as sg
from settings import Config
sg.theme(Config.gui.theme_name)

sliders = [[sg.Slider(Config.gui.shift_range, orientation="h", resolution=.01,
                      default_value=0.0, size=(25, 15), key=f"{name}"),
            sg.Text(name, size=(17, 1))] for name in Config.gui.vector_names]
sliders += [[sg.Button("Transform", key="TRANSFORM"),
             sg.Button("Reset", key="RESET")]]
