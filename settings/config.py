import torch


class Generation:
    default_psi = 0.75
    model_path = "models/ffhq.pkl"
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


class Projection:
    generation_dir = "generated/"
    alignment_dir = "input_imgs/"
    alignment_model = 'models/shape_predictor_68_face_landmarks.dat'
    num_steps = 100
    save_video = True
    seed = 305


class Shifting:
    vectors_path = "vectors/"
    extension = ".npy"


class GUIConfig:
    theme_name = "DarkTeal9"
    display_size = (400, 400)
    shift_range = (-10, 10)
    vector_names = (
        "age",
        "eye_distance",
        "eye_eyebrow_distance",
        "eye_ratio",
        "eyes_open",
        "gender",
        "lip_ratio",
        "mouth_open",
        "mouth_ratio",
        "nose_mouth_distance",
        "nose_ratio",
        "nose_tip",
        "pitch",
        "roll",
        "smile",
        "yaw",
    )


class Config:
    generation = Generation
    shifting = Shifting
    gui = GUIConfig
    projection = Projection