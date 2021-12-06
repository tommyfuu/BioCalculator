from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from numpy.lib.shape_base import split

from .models import Image
import random


class ColonyCounterForm(forms.ModelForm):
    # floor = forms.DecimalField(
    #     decimal_places=0, max_digits=10000, required=True, label=False
    # )
    # ceiling = forms.DecimalField(
    #     decimal_places=0, max_digits=10000, required=True, label=False
    # )
    class Meta:
        model = Image
        fields = ("title", "image")


from glob import glob
import os, json, random
import math

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.structures import BoxMode
import cv2


def agar_to_coco_format(
    img_dir,
    img_format,
    shape="polygon",
    destination_image_source_dir=None,
    class_distinguish=False,
    default_num_of_vertices=12,
):
    current_img_id = 0
    output_l = []
    class_dict = {}
    class_num = 0
    stepSize = 1 / default_num_of_vertices
    for filename in glob(str(img_dir + "/*." + img_format)):
        current_json_name = (
            "/".join(filename.split("/")[:-1])
            + "/"
            + filename.split("/")[-1].split(".")[0]
            + ".json"
        )
        with open(current_json_name) as f:
            imgs_anns = json.load(f)

        current_img_dict = {}
        current_img_annotations = []

        # iterate thru each annotation
        for annotation in imgs_anns["labels"]:
            if annotation["class"] not in class_dict.values():
                class_dict.update({annotation["class"]: class_num})
                class_num += 1
            if shape == "rectangle":
                segment = [
                    annotation["x"],
                    annotation["y"],
                    annotation["x"] + annotation["width"],
                    annotation["y"] + annotation["height"],
                ]
            elif shape == "polygon":
                a = annotation["x"] + annotation["width"] / 2
                b = annotation["y"] + annotation["height"] / 2
                r = (
                    annotation["width"] + annotation["height"]
                ) / 4  # only approximate!

                # Generated vertices
                segment = []

                t = 0
                while t < 2 * math.pi:
                    segment.append(r * math.cos(t) + a)
                    segment.append(r * math.sin(t) + b)
                    t += stepSize
            current_img_annotations.append(
                {
                    "bbox": [
                        annotation["x"],
                        annotation["y"],
                        annotation["x"] + annotation["width"],
                        annotation["y"] + annotation["height"],
                    ],
                    "bbox_mode": BoxMode.XYXY_ABS,
                    "category_id": list(class_dict.keys()).index(annotation["class"])
                    if class_distinguish
                    else 0,
                    "segmentation": [segment],
                }
            )

        # update source image directory in case files are moved to a different directory than initially processed
        if destination_image_source_dir != None:
            current_img_filename = os.path.join(
                destination_image_source_dir, filename.split("/")[-1]
            )
        else:
            current_img_filename = filename

        # generate outputs
        img = cv2.imread(filename)

        current_img_dict.update(
            {
                "annotations": current_img_annotations,
                "file_name": current_img_filename,
                "height": img.shape[0],
                "image_id": current_img_id,
                "width": img.shape[1],
            }
        )
        output_l.append(current_img_dict)
        current_img_id += 1

    # print(output_l)
    print(class_dict)
    if class_distinguish == False:
        class_dict = {"colony": sum(list(class_dict.values()))}

    # save to json
    # with open('./' + outputRoot + '.json', 'w') as outfile:
    #     json.dump(output_l, outfile)
    return output_l, class_dict


# load the saved model
# try to reuse it to make sure it still works
from detectron2.modeling import build_model

cfg = get_cfg()
cfg.MODEL.DEVICE = "cpu"
cfg.merge_from_file(
    model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
)
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
    "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
)
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1  # crucial for everything to function correctly!
cfg.MODEL.WEIGHTS = "./development/output/model_first.pth"
cfg.DATASETS.TEST = ("agar_val",)
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.2  # set the testing threshold for this model
predictor = DefaultPredictor(cfg)

DatasetCatalog.clear()
dirL = ["train", "val"]
prefix = "./homepage/AGAR_rearranged"
trainDirs = "agar_train"
for d in dirL:
    DatasetCatalog.register(
        "agar_" + d, lambda d=d: agar_to_coco_format(prefix + d, "jpg")[0]
    )
    MetadataCatalog.get("agar_" + d).set(
        thing_classes=list(agar_to_coco_format(prefix + d, "jpg")[1].keys())
    )
agar_metadata = MetadataCatalog.get("train")
dataset_dicts = agar_to_coco_format(
    "./homepage/AGAR_rearranged/val",
    "jpg",
)[0]
num = 1
from detectron2.utils.visualizer import ColorMode

print("LENGTH", len(dataset_dicts))
d = random.sample(dataset_dicts, 3)[1]
print("filename", d["file_name"])
im = cv2.imread(d["file_name"])


def run_model(img_src_dir):
    # dataset_dicts = agar_to_coco_format(
    #     "./homepage/media/users/%Y/%m/%d/",
    #     "jpg",
    # )[0]
    # im = cv2.imread(d["file_name"])
    print(img_src_dir)
    for root, dirs, files in os.walk(img_src_dir):
        for file in files:
            img_src = img_src_dir + file
    # img_src = random.choice(os.listdir(img_src_dir))
    im = cv2.imread(img_src)
    print("WHAT AAA", img_src)
    outputs = predictor(im)
    print("model outputs", outputs)
    v = Visualizer(
        im[:, :, ::-1],
        metadata=agar_metadata,
        scale=0.5,
        # remove the colors of unsegmented pixels. This option is only available for segmentation models
        instance_mode=ColorMode.IMAGE_BW,
    )

    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    im = cv2.resize(im, (500, 500), interpolation=cv2.INTER_AREA)
    out1 = out.get_image()[:, :, ::-1]
    out1 = cv2.resize(out1, (500, 500), interpolation=cv2.INTER_AREA)
    cv2.imwrite(
        "/Users/chenlianfu/Documents/Github/BioCalculator/homepage/colonyCountOutputs/testingResult.jpg",
        out.get_image()[:, :, ::-1],
    )

    # cv2.imwrite(
    #     "/Users/chenlianfu/Documents/Github/BioCalculator/homepage/colonyCountOutputs/testing"
    #     + img_src.split("/")[-1],
    #     out.get_image()[:, :, ::-1],
    # )

    # get top <10 x y coordinates, assuming that each colony is a circle
    pred_boxes = outputs["instances"].pred_boxes
    conf_levels = list(outputs["instances"].scores)
    if len(pred_boxes) > 10:
        pred_boxes = pred_boxes[:10]
    else:
        while len(pred_boxes) < 10:
            pred_boxes += "non existent"
            conf_levels += "non existent"
    # assuming it's a circle, calculate center
    # https://github.com/facebookresearch/detectron2/issues/1005
    box_center_xs = [0.5 * (box[0] + box[2]) for box in pred_boxes]
    box_center_ys = [0.5 * (box[1] + box[3]) for box in pred_boxes]

    while len(box_center_xs) < 10:
        box_center_xs += "non existent"
    while len(box_center_ys) < 10:
        box_center_ys += "non existent"
    # prep to save to webpage dict
    x_labels = ["x_1", "x_2", "x_3", "x_4", "x_5", "x_6", "x_7", "x_8", "x_9", "x_10"]
    y_labels = ["y_1", "y_2", "y_3", "y_4", "y_5", "y_6", "y_7", "y_8", "y_9", "y_10"]
    c_labels = ["c_1", "c_2", "c_3", "c_4", "c_5", "c_6", "c_7", "c_8", "c_9", "c_10"]
    x_dict = {x_labels[i]: box_center_xs[i] for i in range(10)}
    y_dict = {y_labels[i]: box_center_ys[i] for i in range(10)}
    c_dict = {c_labels[i]: conf_levels[i] for i in range(10)}
    return x_dict, y_dict, c_dict


# format is documented at https://detectron2.readthedocs.io/tutorials/models.html#model-output-format
# outputs = predictor(im)
# print("model outputs", outputs)
# v = Visualizer(
#     im[:, :, ::-1],
#     metadata=agar_metadata,
#     scale=0.5,
#     # remove the colors of unsegmented pixels. This option is only available for segmentation models
#     instance_mode=ColorMode.IMAGE_BW,
# )
# out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
# im = cv2.resize(im, (500, 500), interpolation=cv2.INTER_AREA)
# out1 = out.get_image()[:, :, ::-1]
# out1 = cv2.resize(out1, (500, 500), interpolation=cv2.INTER_AREA)
# cv2.imwrite("testing" + d["file_name"] + ".jpg", out.get_image()[:, :, ::-1])


def randomNumGenerator_1(floor, ceiling):
    """Given a floor and ceiling integer, generates a random
    number between those two integers"""

    return random.randint(floor, ceiling)
