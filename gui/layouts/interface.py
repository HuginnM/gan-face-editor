import FreeSimpleGUI as sg
from settings import Config
from .sliders import sliders
sg.theme(Config.gui.theme_name)

right_column = [[sg.Text("Select the generation method:")],
                [sg.Button("seed", key="SEED"),
                 sg.Button("z vector", key="Z_VEC"),
                 sg.Button("w vector", key="W_VEC"),
                 sg.Button("project", key="PROJECT")],
                [sg.Slider((0, 1), orientation="h", resolution=.01,
                           default_value=1, size=(25, 15), key="PSI"), sg.Text("truncation psi")],
                [sg.Column(sliders, visible=False, key="SLIDERS", scrollable=True, vertical_scroll_only=True, size=(None, 400))]]

left_column = [
    [sg.Text("GAN Face Editor", font=('Helvetica', 16, 'bold'), pad=((0, 0), (0, 10)))],
    [sg.Text("Original generated image", key="ORIGINAL_CAPTION", visible=False)],
    [sg.Image(key="ORIGINAL_IMAGE", size=Config.gui.display_size, visible=False)],
    [sg.Text("Modified image", key="MODIFIED_CAPTION", visible=False)],
    [sg.Image(key="MODIFIED_IMAGE", size=Config.gui.display_size, visible=False)]
]

main_layout = [[sg.Column(left_column),
                sg.Column(right_column)]]
