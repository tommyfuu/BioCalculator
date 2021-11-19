from detectron2.data.catalog import Metadata
from detectron2.utils.visualizer import Visualizer
import random
__author__ = "Tom Fu"
__version__ = "1.0"

from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.structures import BoxMode
import os
import json
from glob import glob
import cv2
import math


def agar_to_coco_format(img_dir, img_format, shape="polygon", destination_image_source_dir=None, class_distinguish=False, default_num_of_vertices=12):
    current_img_id = 0
    output_l = []
    class_dict = {}
    class_num = 0
    stepSize = 1 / default_num_of_vertices

    for filename in glob(str(img_dir + '/*.' + img_format)):
        current_json_name = "/".join(filename.split(
            '/')[:-1]) + "/" + filename.split('/')[-1].split('.')[0] + '.json'
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
                segment = [annotation["x"], annotation["y"], annotation["x"]
                           + annotation["width"], annotation["y"] + annotation["height"]]
            elif shape == "polygon":
                a = annotation["x"] + annotation["width"] / 2
                b = annotation["y"] + annotation["height"] / 2
                r = (annotation["width"] + annotation["height"]) / 4  # only approximate!

                # Generated vertices
                segment = []

                t = 0
                while t < 2 * math.pi:
                    segment.append(r * math.cos(t) + a)
                    segment.append(r * math.sin(t) + b)
                    t += stepSize

                print("continue segmenting")
            current_img_annotations.append({
                'bbox': [annotation["x"], annotation["y"], annotation["x"] + annotation["width"], annotation["y"] + annotation["height"]],
                'bbox_mode': BoxMode.XYXY_ABS,
                'category_id': list(class_dict.keys()).index(annotation["class"]) if class_distinguish else 0,
                'segmentation': [segment]
            })

        # update source image directory in case files are moved to a different directory than initially processed
        if destination_image_source_dir != None:
            current_img_filename = os.path.join(
                destination_image_source_dir, filename.split('/')[-1])
        else:
            current_img_filename = filename

        # generate outputs
        img = cv2.imread(filename)

        current_img_dict.update({'annotations': current_img_annotations,
                                 'file_name': current_img_filename,
                                 'height': img.shape[0],
                                 'image_id': current_img_id,
                                 'width': img.shape[1]})
        output_l.append(current_img_dict)
        current_img_id += 1

    # print(output_l)
    print(class_dict)
    if class_distinguish == False:
        class_dict = {'colony': sum(list(class_dict.values()))}

    # save to json
    # with open('./' + outputRoot + '.json', 'w') as outfile:
    #     json.dump(output_l, outfile)
    return output_l, class_dict


# img = cv2.imread(img)
source_dir_path = '/Users/chenlianfu/Documents/Github/detectron2/AGAR_representative/lower-resolution'
output_l, class_dict = agar_to_coco_format(
    source_dir_path, 'jpg')

# DatasetCatalog.register("agar_low", agar_to_coco_format(
#     source_dir_path, 'jpg', outputRoot='low_res')[0])
# MetadataCatalog.get("agar_low").set(thing_classes=class_dict.values())
# agar_metadata = MetadataCatalog.get("agar_low")
agar_metadata = Metadata()
agar_metadata.set(thing_classes=list(class_dict.keys()))

d = output_l[3]
img = cv2.imread(d["file_name"])
visualizer = Visualizer(img[:, :, ::-1], metadata=agar_metadata, scale=0.5)
print(visualizer)
print(d)
out = visualizer.draw_dataset_dict(d)
print(out.get_image().shape)
print(out.get_image())
print("AAAAAH")
print(out.get_image()[:, :, ::-1].shape)
print(out.get_image()[:, :, ::-1])
# cv2.imshow('', out.get_image()[:, :, ::-1])
cv2.imwrite('./testing_training.jpg', out.get_image()[:, :, ::-1])
