import torch
import pickle
import numpy as np
from settings import Config

import sys
sys.path.append('stylegan2-ada-pytorch')


class Generator:
    def __init__(self, pickle_path=Config.generation.model_path, device=Config.generation.device):
        """
        Initialize a generator object

        Parameters
        ----------
        pickle_path : str, optional
            The path to the pre-trained model pickle. Default is
            `Config.generation.model_path`.
        device : str or torch.device, optional
            The device to use for the generator. Default is
            `Config.generation.device`.

        Notes
        -----
        The generator is set to evaluation mode upon initialization.
        """
        self.device = device
        with open(pickle_path, 'rb') as f:
            self.G = pickle.load(f)['G_ema'].to(device)
            self.G.eval()

    def truncate_w(self, w, truncation_psi=1):
        """
        Parameters
        ----------
        w : torch.tensor
            The latent code to be truncated
        truncation_psi : float, optional
            The truncation factor, between 0 and 1. Lower values result in a more
            drastic truncation. Default is 1 (no truncation).

        Returns
        -------
        w_trunc : torch.tensor
            The truncated latent code
        """
        w_avg = self.G.mapping.w_avg
        w = truncation_psi*(w - w_avg) + w_avg
        return w

    def get_z(self, seed):
        """
        Generates a latent vector z from a given seed

        Parameters
        ----------
        seed : int
            random seed

        Returns
        -------
        z : latent vector
        """
        z = np.random.RandomState(seed).randn(1, self.G.z_dim)
        return z

    def get_w(self, z, truncation_psi=1):
        """
        Generates latent vector w from latent vector z and applies truncation

        Parameters
        ----------
        z : latent vector
        truncation_psi : float, optional
            truncation psi, by default 1

        Returns
        -------
        w : latent vector
        """
        z = torch.tensor(z).to(self.device)
        with torch.no_grad():
            w = self.G.mapping(z, None)
            w = self.truncate_w(w, truncation_psi)
        return w

    def get_img(self, w):
        """
        Generates an image from a latent vector w

        Parameters
        ----------
        w : latent vector

        Returns
        -------
        img : tensor
            generated image
        """
        with torch.no_grad():
            img = self.G.synthesis(w, noise_mode='const', force_fp32=True)[0]
        return img
