from ctypes import *
import cv2
import os

from files.logger import logger


class ObjectDetect:

    def __init__(self):
        self.thresh = 0.25
        self.dark_net_path = "files/object/darknet.so"
        self.config_path = "files/object/cfg/yolo-obj.cfg"
        self.weight_path = "files/object/backup/yolo-obj_7800.weights"
        self.meta_path = "files/object/data/obj.data"

        self.net_main = None
        self.meta_main = None
        self.alt_names = None
        self.lib = None
        self.make_image = None
        self.get_network_boxes = None
        self.make_network_boxes = None
        self.free_detections = None
        self.free_ptrs = None
        self.network_predict = None
        self.load_net = None
        self.load_net_custom = None
        self.reset_rnn = None
        self.do_nms_obj = None
        self.do_nms_sort = None
        self.free_image = None
        self.letterbox_image = None
        self.load_meta = None
        self.predict = None
        self.rgbgr_image = None
        self.predict_image = None

        self.init()

    def array_to_image(self, arr):
        import numpy as np
        # need to return old values to avoid python freeing memory
        arr = arr.transpose(2, 0, 1)
        c = arr.shape[0]
        h = arr.shape[1]
        w = arr.shape[2]
        arr = np.ascontiguousarray(arr.flat, dtype=np.float32) / 255.0
        data = arr.ctypes.data_as(POINTER(c_float))
        im = IMAGE(w, h, c, data)
        return im, arr

    def detect(self, image, hier_thresh=.5, nms=.45):
        """
        Performs the meat of the detection
        """
        net = self.net_main
        meta = self.meta_main
        custom_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        custom_image = cv2.resize(custom_image,
                                  (self.lib.network_width(self.net_main), self.lib.network_height(self.net_main)),
                                  interpolation=cv2.INTER_LINEAR)
        # custom_image = scipy.misc.imread(image)
        im, arr = self.array_to_image(custom_image)  # you should comment line below: free_image(im)
        num = c_int(0)
        pnum = pointer(num)
        self.predict_image(net, im)
        dets = self.get_network_boxes(net, im.w, im.h, self.thresh, hier_thresh, None, 0, pnum, 0)
        num = pnum[0]
        if nms:
            self.do_nms_sort(dets, num, meta.classes, nms)
        res = []
        for j in range(num):
            for i in range(meta.classes):
                if dets[j].prob[i] > 0:
                    b = dets[j].bbox
                    if self.alt_names is None:
                        nameTag = meta.names[i]
                    else:
                        nameTag = self.alt_names[i]

                    res.append((nameTag, dets[j].prob[i], (b.x, b.y, b.w, b.h)))
        res = sorted(res, key=lambda x: -x[1])
        # free_image(im)
        self.free_detections(dets, num)
        return res

    def perform_detect(self, image):
        # Do the detection
        detections = self.detect(image)
        return detections

    def init(self):
        has_gpu = True
        self.lib = CDLL(self.dark_net_path, RTLD_GLOBAL)
        self.lib.network_width.argtypes = [c_void_p]
        self.lib.network_width.restype = c_int
        self.lib.network_height.argtypes = [c_void_p]
        self.lib.network_height.restype = c_int

        self.predict = self.lib.network_predict
        self.predict.argtypes = [c_void_p, POINTER(c_float)]
        self.predict.restype = POINTER(c_float)

        if has_gpu:
            set_gpu = self.lib.cuda_set_device
            set_gpu.argtypes = [c_int]

        self.make_image = self.lib.make_image
        self.make_image.argtypes = [c_int, c_int, c_int]
        self.make_image.restype = IMAGE

        self.get_network_boxes = self.lib.get_network_boxes
        self.get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int,
                                           POINTER(c_int), c_int]
        self.get_network_boxes.restype = POINTER(DETECTION)

        self.make_network_boxes = self.lib.make_network_boxes
        self.make_network_boxes.argtypes = [c_void_p]
        self.make_network_boxes.restype = POINTER(DETECTION)

        self.free_detections = self.lib.free_detections
        self.free_detections.argtypes = [POINTER(DETECTION), c_int]

        self.free_ptrs = self.lib.free_ptrs
        self.free_ptrs.argtypes = [POINTER(c_void_p), c_int]

        self.network_predict = self.lib.network_predict
        self.network_predict.argtypes = [c_void_p, POINTER(c_float)]

        self.reset_rnn = self.lib.reset_rnn
        self.reset_rnn.argtypes = [c_void_p]

        self.load_net = self.lib.load_network
        self.load_net.argtypes = [c_char_p, c_char_p, c_int]
        self.load_net.restype = c_void_p

        self.load_net_custom = self.lib.load_network_custom
        self.load_net_custom.argtypes = [c_char_p, c_char_p, c_int, c_int]
        self.load_net_custom.restype = c_void_p

        self.do_nms_obj = self.lib.do_nms_obj
        self.do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

        self.do_nms_sort = self.lib.do_nms_sort
        self.do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

        self.free_image = self.lib.free_image
        self.free_image.argtypes = [IMAGE]

        self.letterbox_image = self.lib.letterbox_image
        self.letterbox_image.argtypes = [IMAGE, c_int, c_int]
        self.letterbox_image.restype = IMAGE

        self.load_meta = self.lib.get_metadata
        self.lib.get_metadata.argtypes = [c_char_p]
        self.lib.get_metadata.restype = METADATA

        self.load_image = self.lib.load_image_color
        self.load_image.argtypes = [c_char_p, c_int, c_int]
        self.load_image.restype = IMAGE

        self.rgbgr_image = self.lib.rgbgr_image
        self.rgbgr_image.argtypes = [IMAGE]

        self.predict_image = self.lib.network_predict_image
        self.predict_image.argtypes = [c_void_p, IMAGE]
        self.predict_image.restype = POINTER(c_float)

        assert 0 < self.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
        if not os.path.exists(self.config_path):
            raise ValueError("Invalid config path `" + os.path.abspath(self.config_path) + "`")
        if not os.path.exists(self.weight_path):
            raise ValueError("Invalid weight path `" + os.path.abspath(self.weight_path) + "`")
        if not os.path.exists(self.meta_path):
            raise ValueError("Invalid data file path `" + os.path.abspath(self.meta_path) + "`")

        self.net_main = self.load_net_custom(self.config_path.encode("ascii"), self.weight_path.encode("ascii"), 0,
                                             1)  # batch size = 1
        self.meta_main = self.load_meta(self.meta_path.encode("ascii"))

        # In Python 3, the metafile default access craps out on Windows (but not Linux)
        # Read the names file and create a list to feed to detect
        try:
            with open(self.meta_path) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents, re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            names_list = namesFH.read().strip().split("\n")
                            self.alt_names = [x.strip() for x in names_list]
                except TypeError:
                    pass
        except Exception:
            pass

        logger.info("Initialized Object Detection...")


class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]


class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]


class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]