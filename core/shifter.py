import os
from settings import Config
from utils import load_numpy


class Shifter:
    def __init__(self, vectors_dir=Config.shifting.vectors_path, ext=Config.shifting.extension):
        """
        Constructor for Shifter class.

        This class is used to shift latent vectors in different directions.

        Parameters
        ----------
        vectors_dir : str, optional
            directory where shift vectors are stored. Default is
            `Config.shifting.vectors_path`.
        ext : str, optional
            extension of shift vector files. Default is
            `Config.shifting.extension`.

        Attributes
        ----------
        fnames : list
            filenames of shift vectors
        vectors : dict
            dictionary of shift vectors. Keys are the names of the vectors
            without the extension, and values are tensors of shape (1, 512)
            containing the shift vectors. The tensors are placed on the device
            specified in `Config.generation.device`.
        """
        self.fnames = [file for file in os.listdir(vectors_dir) if file.endswith(ext)]
        self.vectors = {}
        for file in self.fnames:
            path = os.path.join(vectors_dir, file)
            name = file.replace(ext, '')
            vec = load_numpy(path, device=Config.generation.device)
            vec = vec.unsqueeze(0)
            self.vectors[name] = vec

    def __call__(self, w, direction, amount):
        """
        Shifts the given latent vector w in the given direction by the given amount.

        Parameters
        ----------
        w : torch.Tensor
            Latent vector to shift. Shape should be (1, 512).
        direction : str
            Name of shift vector to use. The name should match one of the keys in the
            self.vectors dictionary.
        amount : float
            Amount to shift. This value is multiplied by the shift vector and added to
            the latent vector.

        Returns
        -------
        w : torch.Tensor
            Shifted latent vector. Shape is (1, 512).
        """
        vec = self.vectors[direction]
        vec_scaled = vec * amount
        w = w + vec_scaled
        return w
