from detectron2.config import CfgNode as CN
from projects.CenterNet.centernet import add_centernet_config


def add_sgt_config(cfg: CN):
    _C = cfg
    add_centernet_config(_C)
    _C.MODEL.WEIGHTS = ""

    # Loss
    _C.MODEL.SGT = CN()
    _C.MODEL.SGT.INFERENCE_GT = False

    _C.MODEL.DETECTOR = CN({"ENABLED": True})
    _C.MODEL.DETECTOR.META_ARCHITECTURE = "CenterNet"
    _C.MODEL.DETECTOR.WEIGHTS = ""
    _C.MODEL.DETECTOR.FREEZE = False

    _C.MODEL.TRACKER = CN({"ENABLED": True})
    _C.MODEL.TRACKER.META_ARCHITECTURE = "GraphTracker"
    _C.MODEL.TRACKER.WEIGHTS = ""
    _C.MODEL.TRACKER.CUT_DET_GRAD = True
    _C.MODEL.TRACKER.INIT_DET_THRESH = 0.5

    _C.MODEL.TRACKER.LABEL_ASSIGNMENT = CN()
    _C.MODEL.TRACKER.LABEL_ASSIGNMENT.TRAIN_BY_GT = False
    _C.MODEL.TRACKER.LABEL_ASSIGNMENT.METRIC = 'iou' # 'distance' | 'iou'
    _C.MODEL.TRACKER.LABEL_ASSIGNMENT.MIN_IOU = 0.5
    _C.MODEL.TRACKER.LABEL_ASSIGNMENT.MIN_WH_RATIO = 0.25
    _C.MODEL.TRACKER.LABEL_ASSIGNMENT.FILL_GT_FLAG = False
    _C.MODEL.TRACKER.LABEL_ASSIGNMENT.REPLACE_POLICY = 'random' # '' | 'reverse' | 'random'

    _C.MODEL.TRACKER.MANAGER = CN()
    _C.MODEL.TRACKER.MANAGER.HISTORY_LEN = 30 # number of frames if not using FPS
    _C.MODEL.TRACKER.MANAGER.HISTORY_BY_FPS = True
    _C.MODEL.TRACKER.MANAGER.MIN_LEN_BY_FPS = False
    _C.MODEL.TRACKER.MANAGER.MIN_TRACKLET_LEN = 10
    _C.MODEL.TRACKER.MANAGER.MIN_TRACKLET_SEC = 0.333

    _C.MODEL.TRACKER.SMOOTH_FEAT = CN()
    _C.MODEL.TRACKER.SMOOTH_FEAT.FLAG = True
    _C.MODEL.TRACKER.SMOOTH_FEAT.ALPHA = 0.9
    _C.MODEL.TRACKER.SMOOTH_FEAT.WEIGHT_BY_SCORE = False

    _C.MODEL.TRACKER.SECOND_MATCH = CN()
    _C.MODEL.TRACKER.SECOND_MATCH.FLAG = True
    _C.MODEL.TRACKER.SECOND_MATCH.IOU_THRESH = 0.5
    _C.MODEL.TRACKER.SECOND_MATCH.RECOVERY_FLAG = False

    ## GNN
    _C.MODEL.TRACKER.GNN = CN()
    _C.MODEL.TRACKER.GNN.GRAPH = CN()
    _C.MODEL.TRACKER.GNN.GRAPH.PREV_DET_PROPOSAL_FLAG = True
    _C.MODEL.TRACKER.GNN.GRAPH.ATTR = ['iou', 'sim', 'dist'] # 'iou' | 'sim' | 'dist'
    _C.MODEL.TRACKER.GNN.GRAPH.TOPK = 10
    _C.MODEL.TRACKER.GNN.TOPK_DET_FLAG = True
    _C.MODEL.TRACKER.GNN.TOPK_DET = 100
    _C.MODEL.TRACKER.GNN.DET_LOW_THRESH = 0.1
    _C.MODEL.TRACKER.GNN.N_ITER = 3

    ## GNN - Message Passing Network with edge attribute
    ## NODE MODEL
    _C.MODEL.TRACKER.GNN.NODE_MODEL = CN()
    _C.MODEL.TRACKER.GNN.NODE_MODEL.UPDATE = CN()
    _C.MODEL.TRACKER.GNN.NODE_MODEL.UPDATE.IN_DIM = 256
    _C.MODEL.TRACKER.GNN.NODE_MODEL.UPDATE.FC_DIMS = []
    _C.MODEL.TRACKER.GNN.NODE_MODEL.UPDATE.DROPOUT_P = 0.0
    _C.MODEL.TRACKER.GNN.NODE_MODEL.UPDATE.AGG_FUNC = 'mean' # 'sum' over-smoothing
    _C.MODEL.TRACKER.GNN.NODE_MODEL.UPDATE.REATTACH = False
    _C.MODEL.TRACKER.GNN.NODE_MODEL.UPDATE.SKIP_CONN = False
    _C.MODEL.TRACKER.GNN.NODE_MODEL.UPDATE.TMPNN_FLAG = False
    _C.MODEL.TRACKER.GNN.NODE_MODEL.UPDATE.SHARED_FLAG = False
    _C.MODEL.TRACKER.GNN.NODE_MODEL.UPDATE.SELF_LOOP = False

    ## Node Classifier
    cfg.MODEL.TRACKER.GNN.NODE_MODEL.CLASSIFY = CN()
    cfg.MODEL.TRACKER.GNN.NODE_MODEL.CLASSIFY.FLAG = False
    cfg.MODEL.TRACKER.GNN.NODE_MODEL.CLASSIFY.INF_THRESH = 0.5
    cfg.MODEL.TRACKER.GNN.NODE_MODEL.CLASSIFY.DEEP_LOSS = False
    cfg.MODEL.TRACKER.GNN.NODE_MODEL.CLASSIFY.FOCAL_ALPHA = 0.25
    cfg.MODEL.TRACKER.GNN.NODE_MODEL.CLASSIFY.FOCAL_GAMMA = 2.0
    cfg.MODEL.TRACKER.GNN.NODE_MODEL.CLASSIFY.LOSS_WEIGHT = 1.0
    cfg.MODEL.TRACKER.GNN.NODE_MODEL.CLASSIFY.FC_DIMS = [64, 64]
    cfg.MODEL.TRACKER.GNN.NODE_MODEL.CLASSIFY.DROPOUT_P = 0.0

    ## EDGE MODEL
    _C.MODEL.TRACKER.GNN.EDGE_MODEL = CN()
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.ENCODE = CN()
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.ENCODE.EDGE_ATTR = ['xy_diff', 'wh_ratio', 'iou', 'cos_sim'] # ['iou', 'cos_sim']
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.ENCODE.DIRECTIONAL_EDGE_ATTR = True
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.ENCODE.IN_DIM = 6
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.ENCODE.FC_DIMS = []
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.ENCODE.OUT_DIM = 16
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.ENCODE.DROPOUT_P = 0.0
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.UPDATE = CN()
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.UPDATE.IN_DIM = 6
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.UPDATE.FC_DIMS = []
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.UPDATE.DROPOUT_P = 0.0
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.UPDATE.REATTACH = False
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.UPDATE.SKIP_CONN = False
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.UPDATE.SELF_LOOP = False

    ## Edge Classifier
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.CLASSIFY = CN()
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.CLASSIFY.LOSS_WEIGHT = 1.
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.CLASSIFY.IN_DIM = 16
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.CLASSIFY.FC_DIMS = []
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.CLASSIFY.DROPOUT_P = 0.0
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.CLASSIFY.INF_THRESH = 0.5
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.CLASSIFY.FOCAL_ALPHA = 0.25
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.CLASSIFY.FOCAL_GAMMA = 2.0
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.CLASSIFY.DEEP_LOSS = False
    _C.MODEL.TRACKER.GNN.EDGE_MODEL.CLASSIFY.EXCLUDE_INIT_LOSS = True
