# -*- coding: utf-8 -*-

# Max-Planck-Gesellschaft zur Förderung der Wissenschaften e.V. (MPG) is
# holder of all proprietary rights on this computer program.
# You can only use this computer program if you have closed
# a license agreement with MPG or you get the right to use the computer
# program from someone who is authorized to grant you that right.
# Any use of the computer program without a valid license is prohibited and
# liable to prosecution.
#
# Copyright©2019 Max-Planck-Gesellschaft zur Förderung
# der Wissenschaften e.V. (MPG). acting on behalf of its Max Planck Institute
# for Intelligent Systems. All rights reserved.
#
# Contact: ps-license@tuebingen.mpg.de

import argparse
import os.path as osp
from yacs.config import CfgNode as CN

# CONSTANTS
# You may modify them at will
SMPL_DATA_DIR = 'data/vibe_data'
AMASS_DIR = 'data/amass'
INSTA_DIR = 'data/insta_variety'
MPII3D_DIR = 'data/mpi_inf_3dhp'
THREEDPW_DIR = 'data/3dpw'
PENNACTION_DIR = 'data/penn_action'
POSETRACK_DIR = 'data/posetrack'
VIBE_DATA_DIR = 'data/vibe_data'
H36M_DIR = 'data/h36m'
VPARE_DATA_DIR = 'data/vpare_data'

# Configuration variables
cfg = CN()

cfg.OUTPUT_DIR = 'results'
cfg.EXP_NAME = 'default'
cfg.DEBUG = True
cfg.DEVICE = 'cuda'
cfg.LOGDIR = ''
cfg.NUM_WORKERS = 8
cfg.DEBUG_FREQ = 1000
cfg.SEED_VALUE = -1
cfg.DEBUG_VID = []

cfg.CUDNN = CN()
cfg.CUDNN.BENCHMARK = True
cfg.CUDNN.DETERMINISTIC = False
cfg.CUDNN.ENABLED = True

cfg.TRAIN = CN()
# cfg.TRAIN.DATASETS_2D = ['Insta']
cfg.TRAIN.DATASETS_2D = []
cfg.TRAIN.DATASETS_3D = ['MPII3D']
cfg.TRAIN.DATASET_EVAL = []
cfg.TRAIN.BATCH_SIZE = 32
cfg.TRAIN.DATA_2D_RATIO = 0.5
cfg.TRAIN.START_EPOCH = 0
cfg.TRAIN.END_EPOCH = 5
cfg.TRAIN.PRETRAINED_REGRESSOR = ''
cfg.TRAIN.PRETRAINED = ''
cfg.TRAIN.RESUME = ''
cfg.TRAIN.NUM_ITERS_PER_EPOCH = 1000
cfg.TRAIN.LR_PATIENCE = 5

cfg.TRAIN.MODE = 0
cfg.TRAIN.VALID_MODE = 0

# <====== generator optimizer
cfg.TRAIN.GEN_OPTIM = 'Adam'
cfg.TRAIN.GEN_LR = 1e-4
cfg.TRAIN.GEN_WD = 1e-4
cfg.TRAIN.GEN_MOMENTUM = 0.9

# <====== motion discriminator optimizer
cfg.TRAIN.MOT_DISCR = CN()
cfg.TRAIN.MOT_DISCR.OPTIM = 'SGD'
cfg.TRAIN.MOT_DISCR.LR = 1e-2
cfg.TRAIN.MOT_DISCR.WD = 1e-4
cfg.TRAIN.MOT_DISCR.MOMENTUM = 0.9
cfg.TRAIN.MOT_DISCR.UPDATE_STEPS = 1
cfg.TRAIN.MOT_DISCR.FEATURE_POOL = 'concat'
cfg.TRAIN.MOT_DISCR.HIDDEN_SIZE = 1024
cfg.TRAIN.MOT_DISCR.NUM_LAYERS = 1
cfg.TRAIN.MOT_DISCR.ATT = CN()
cfg.TRAIN.MOT_DISCR.ATT.SIZE = 1024
cfg.TRAIN.MOT_DISCR.ATT.LAYERS = 1
cfg.TRAIN.MOT_DISCR.ATT.DROPOUT = 0.1

cfg.DATASET = CN()
cfg.DATASET.SEQLEN = 20
cfg.DATASET.OVERLAP = 0.5

cfg.LOSS = CN()
cfg.LOSS.KP_2D_W = 60.
cfg.LOSS.KP_3D_W = 30.
cfg.LOSS.SHAPE_W = 0.001
cfg.LOSS.POSE_W = 1.0
cfg.LOSS.E_MOTION_LOSS_W = 2.0
cfg.LOSS.D_MOTION_LOSS_R = 1.0 # loss weight ratio D/G 
#<====== angular loss
cfg.LOSS.ANGULAR_W = 0.

cfg.MODEL = CN()

cfg.MODEL.TEMPORAL_TYPE = 'gru'

# GRU model hyperparams
cfg.MODEL.TGRU = CN()
cfg.MODEL.TGRU.NUM_LAYERS = 1
cfg.MODEL.TGRU.ADD_LINEAR = False
cfg.MODEL.TGRU.RESIDUAL = False
cfg.MODEL.TGRU.HIDDEN_SIZE = 2048
cfg.MODEL.TGRU.BIDIRECTIONAL = False

# Vpare model params
cfg.MODEL.USE_PART_ATT = False
cfg.MODEL.PRETRAINED_PARE = osp.join(VPARE_DATA_DIR, 'pare_w_3dpw_checkpoint.ckpt')
cfg.MODEL.BACKBONE_CKPT = osp.join(VPARE_DATA_DIR, 'hrnet_w32.pth.tar')
cfg.MODEL.USE_POSE_TGRU = False
cfg.MODEL.USE_SC_TGRU = False
cfg.MODEL.PART = CN()
cfg.MODEL.PART.USE_GRAD = False
# GRNet model params
cfg.MODEL.USE_MAX_ENCODER = False
cfg.MODEL.POST_ENCODE = False # whether to use reduced feature map for encoding
cfg.MODEL.GRID_ALIGN_Attn = False
cfg.MODEL.NEW_PART_Attn = False

def get_cfg_defaults():
    """Get a yacs CfgNode object with default values for my_project."""
    # Return a clone so that the defaults will not be altered
    # This is for the "local variable" use pattern
    return cfg.clone()


def update_cfg(cfg_file):
    cfg = get_cfg_defaults()
    cfg.merge_from_file(cfg_file)
    return cfg.clone()


def parse_args(args=None):
    if args is None:
        parser = argparse.ArgumentParser()
        parser.add_argument('--cfg', type=str, help='cfg file path')

        args = parser.parse_args()
        print(args, end='\n\n')
    
    cfg_file = args.cfg
    if args.cfg is not None:
        cfg = update_cfg(args.cfg)
    else:
        cfg = get_cfg_defaults()

    return cfg, cfg_file