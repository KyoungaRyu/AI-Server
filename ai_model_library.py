# -*- coding: utf-8 -*-
"""ai_model_library

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A1D4H-g5E-Nd_DlkfWT-cbytel6j8yXw
"""

import os
import torch
import torchvision
from torch import nn
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader
from torchtext import data
from torchtext.data import TabularDataset
import numpy as np
import pandas as pd