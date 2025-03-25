from core.generator import Generator
from core.shifter import Shifter
from core.projector import run_projection
from core.align_faces import align_face

from utils import convert_image, get_img_bits, load_numpy
from PIL import Image
from settings import Config


class Controller:
    def __init__(self):
        self.generator = Generator()
        self.shifter = Shifter()
        self.w = None

    def generate_img_from_seed(self, seed, psi):
        """
        Generates bits of an image using seeded z vector and truncation psi
        """
        z = self.generator.get_z(seed)
        self.w = self.generator.get_w(z, psi)
        img = self.generator.get_img(self.w)
        img = convert_image(img, Config.gui.display_size)
        img_bits = get_img_bits(img)
        return img_bits

    def generate_img_from_z_vec(self, path, psi):
        """
        Generates bits of an image using a path to a z vector and truncation psi
        (also saves w vector)
        """
        z = load_numpy(path, device=Config.generation.device)
        self.w = self.generator.get_w(z, psi)
        img = self.generator.get_img(self.w)
        img = convert_image(img, Config.gui.display_size)
        img_bits = get_img_bits(img)
        return img_bits

    def generate_img_from_w_vec(self, path):
        """
        Generates bits of an image using a path to a w vector and truncation psi
        (also saves w vector)
        """
        self.w = load_numpy(path, device=Config.generation.device)
        img = self.generator.get_img(self.w)
        img = convert_image(img, Config.gui.display_size)
        img_bits = get_img_bits(img)
        return img_bits

    def trasnform_img(self, directions, psi):
        """
        Transforms saved w vector and generates new transformed image bits.

        Parameters
        ----------
        directions : dict
            dictionary where key is direction and value is shifting amount (i.e. 'age':5.0)
        psi : float
            truncation psi value.

        Returns
        -------
        img_bits : bytes
            transformed image bits
        """
        w_prime = self.generator.truncate_w(self.w, psi)
        for direction, amount in directions.items():
            w_prime = self.shifter(w_prime, direction, amount)
        img = self.generator.get_img(w_prime)
        img = convert_image(img, Config.gui.display_size)
        img_bits = get_img_bits(img)
        return img_bits

    def read_path(self, path):
        """
        Read an image from a path converts it to display size and converts it to bits
        """
        img = Image.open(path)
        img = img.resize(Config.gui.display_size)
        img_bits = get_img_bits(img)
        return img_bits

    def align(self, path):
        """
        Aligns the image using provided path and returns bits of aligned image and its path
        """
        aligned_path = align_face(path)
        aligned_bits = self.read_path(aligned_path)
        return aligned_bits, aligned_path

    def project(self, path):
        """
        Runs projection and returns bits of the generated image (also saves w vector)
        """
        img, self.w = run_projection(path, self.generator.G)
        img = convert_image(img, Config.gui.display_size)
        projected_bits = get_img_bits(img)
        return projected_bits
