import PySimpleGUI as sg
from settings import Config
from controller import Controller
from .layouts.interface import main_layout
from .layouts.project import projection_layout

sg.theme(Config.gui.theme_name)


def projection_window(controller):
    """
    Runs a projection given a file path and displays the projected image.

    This function initializes a new window for the projection process and
    continuously listens for events such as button clicks. When the "Submit"
    button is clicked, it reads the file path, aligns the image, runs the
    projection, and displays the projected image in the GUI window. Once
    the projection is finished, it shows a popup message and closes the
    window.

    Parameters
    ----------
    controller : controller.Controller
        The controller class instance to interact with the GUI.

    Returns
    -------
    projected_img_bits : numpy array
        The image bits of the projected image.
    """
    project_window = sg.Window("Running projection", projection_layout)
    while True:
        event, values = project_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, "EXIT"):
            break
        elif event == "Submit":
            original_img_bits = controller.read_path(values["FILE"])
            project_window["ORIGINAL"].update(data=original_img_bits)
            project_window.refresh()
            aligned_img_bits, aligned_path = controller.align(values["FILE"])
            project_window["ALIGNED"].update(data=aligned_img_bits)
            project_window.refresh()
            projected_img_bits = controller.project(aligned_path)
            project_window["PROJECTED"].update(data=projected_img_bits)
            project_window.refresh()
            sg.popup_ok("Projection has finished", keep_on_top=True)
            break
    project_window.close()
    return projected_img_bits


def main():
    """
    Main function to handle the GUI for generating and transforming images using different methods.

    This function initializes the main window for the GUI and continuously listens for events
    such as button clicks. Depending on the event, it performs actions like generating images 
    from seed, z vector, w vector, or running a projection. It also handles transformations 
    and resets based on slider inputs, updating the GUI elements accordingly.

    Events handled:
    - "SEED": Generates an image using a provided seed value.
    - "Z_VEC": Generates an image using a z vector from a file.
    - "W_VEC": Generates an image using a w vector from a file.
    - "PROJECT": Runs a projection and displays the projected image.
    - "TRANSFORM": Applies transformations to the image based on slider values.
    - "RESET": Resets the transformations and hides modified image elements.

    The function ensures the visibility and data of GUI components are updated as per the actions taken.
    """

    window_main = sg.Window("Generator", main_layout)
    controller = Controller()

    while True:
        event, values = window_main.read()

        print(event, values)
        if event in (sg.WIN_CLOSED, "EXIT"):
            break

        elif event in ("SEED", "Z_VEC", "W_VEC", "PROJECT"):
            if event == "SEED":
                seed = int(sg.popup_get_text("Enter z seed: ", title="input"))
                generated_img_bits = controller.generate_img_from_seed(seed, values["PSI"])
            elif event == "Z_VEC":
                path = sg.popup_get_file("Enter the path to z vector", title="input")
                generated_img_bits = controller.generate_img_from_z_vec(path, values["PSI"])
            elif event == "W_VEC":
                path = sg.popup_get_file("Enter the path to w vector", title="input")
                generated_img_bits = controller.generate_img_from_w_vec(path)
            elif event == "PROJECT":
                generated_img_bits = projection_window(controller)

            # update visibility
            window_main["ORIGINAL_CAPTION"].update(visible=True)
            window_main["ORIGINAL_IMAGE"].update(visible=True)
            window_main["SLIDERS"].update(visible=True)
            # update data
            window_main["ORIGINAL_IMAGE"].update(data=generated_img_bits)

        elif event == "TRANSFORM":
            directions = {key: values[key] for key in Config.gui.vector_names}
            bits = controller.trasnform_img(directions, values["PSI"])

            # update visibility
            window_main["MODIFIED_CAPTION"].update(visible=True)
            window_main["MODIFIED_IMAGE"].update(visible=True)
            # update data
            window_main["MODIFIED_IMAGE"].update(data=bits)

        elif event == "RESET":
            for name in Config.gui.vector_names:
                window_main[name].Update(value=0)
            window_main["MODIFIED_CAPTION"].update(visible=False)
            window_main["MODIFIED_IMAGE"].update(visible=False)

    window_main.close()
