from raga import *
import pandas as pd
import datetime
import json
import ast
import random


def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp


def replace_url(s3_url):
    parts = s3_url.split("/")
    object_key = "/".join(parts[3:])
    http_url = f"https://raga-engineering.s3.us-east-2.amazonaws.com/{object_key}"
    return http_url


# label_to_classname = {
#     # 0: "no_data",
#     1: "water",
#     2: "trees",
#     3: "grass",
#     4: "flooded vegetation",
#     5: "crops",
#     6: "scrub",
#     7: "built_area",
#     8: "bare_ground",
#     9: "snow_or_ice",
#     10: "clouds",
#     11: "no_data",
# }
# label_to_classname = {
#     0: "Unlabeled",
#     1: "Ego vehicle",
#     2: "Rectification border",
#     3: "Out of roi (region of interest)",
#     4: "Static",
#     5: "Dynamic",
#     6: "Ground",
#     7: "Road",
#     8: "Sidewalk",
#     9: "Parking",
#     10: "Rail track",
#     11: "Building",
#     12: "Wall",
#     13: "Fence",
#     14: "Guard rail",
#     15: "Bridge",
#     16: "Tunnel",
#     17: "Pole",
#     18: "Polegroup",
#     19: "Traffic light",
#     20: "Traffic sign",
#     21: "Vegetation",
#     22: "Terrain",
#     23: "Sky",
#     24: "Person",
#     25: "Rider",
#     26: "Car",
#     27: "Truck",
#     28: "Bus",
#     29: "Caravan",
#     30: "Trailer",
#     31: "Train",
#     32: "Motorcycle",
#     33: "Bicycle",
#     34: "License plate",
# }

# label_to_classname = {
#     0: "no data",
#     1: "water",
#     2: "vegetation",
#     3: "builtup",
#     4: "barren",
# }

# label_to_classname = {
#     0: "road",
#     1: "sidewalk",
#     2: "building",
#     3: "wall",
#     4: "fence",
#     5: "pole",
#     6: "traffic light",
#     7: "traffic sign",
#     8: "vegetation",
#     9: "terrain",
#     10: "sky",
#     11: "person",
#     12: "rider",
#     13: "car",
#     14: "truck",
#     15: "bus",
#     16: "train",
#     17: "motorcycle",
#     18: "bicycle",
# }


# label_to_classname = {
#     0: "road",
#     1: "sidewalk",
#     2: "building",
#     3: "wall",
#     4: "fence",
#     5: "pole",
#     6: "traffic light",
#     7: "traffic sign",
#     8: "vegetation",
#     9: "terrain",
#     10: "sky",
#     11: "person",
#     12: "rider",
#     13: "car",
#     14: "truck",
#     15: "bus",
#     16: "train",
#     17: "motorcycle",
#     18: "bicycle",
# }

label_to_classname = {
    0: "background",  # vegetation, terrain, sky, pole, sidewalk
    1: "vehicles",  # car, truck, bus, train, motorcycle, bicycle
    2: "road",  # road
    3: "people",  # person, rider
    4: "traffic",  # "traffic light, traffic sign"
    5: "building",  # building, wall, fence
}

# bdd
# label_to_classname = {
#     1: "pedestrian",
#     2: "rider",
#     3: "car",
#     4: "truck",
#     5: "bus",
#     6: "train",
#     7: "motorcycle",
#     8: "bicycle",
#     9: "traffic light",
#     10: "traffic sign",
# }


def csv_parser(csv_path):
    data_frame = pd.read_csv(csv_path)
    data_frame["ImageId"] = data_frame["id"].apply(lambda x: x)
    data_frame["ImageUri"] = data_frame["image_path"].apply(lambda x: x)
    data_frame["TimeOfCapture"] = data_frame.apply(
        lambda row: TimeStampElement(get_timestamp_x_hours_ago(row.name)), axis=1
    )
    # data_frame["Reflection"] = data_frame.apply(
    #     lambda row: random.choice(["Yes", "No"]), axis=1
    # )
    # data_frame["Overlap"] = data_frame.apply(
    #     lambda row: random.choice(["Yes", "No"]), axis=1
    # )
    # data_frame["CameraAngle"] = data_frame.apply(
    #     lambda row: random.choice(["Yes", "No"]), axis=1
    # )

    data_frame["Annotations"] = data_frame["label_path"].apply(lambda x: x)
    data_frame["ModelAInference"] = data_frame["model_path"].apply(lambda x: x)
    data_frame["MistakeScores"] = data_frame["MistakeScores"]
    data_frame["ImageEmbedding"] = data_frame["ImageEmbedding"]

    # data_frame["MistakeScores"] = data_frame["MistakeScores"].apply(
    #     lambda x: ast.literal_eval(x)
    # )
    # data_frame["ImageEmbedding"] = data_frame["ImageEmbedding"].apply(
    #     lambda x: json.loads(x.replace("'", '"'))
    # )
    return data_frame


pd_data_frame = csv_parser(
    # "/home/ubuntu/1.1Tdisk/DatasetUpload/cityscapes/cityscape_train_null_1_mistake_score.csv"
    "/Users/rupalitripathi/IdeaProjects/testing-platform-python-client/raga/examples/assets/cityscape_val_fma.csv"
)


schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("ImageUri", ImageUriSchemaElement())
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement())

schema.add(
    "Annotations",
    TIFFSchemaElement(label_mapping=label_to_classname, schema="tiff", model="GT"),
)
schema.add(
    "ModelAInference",
    TIFFSchemaElement(label_mapping=label_to_classname, schema="tiff", model="modelA"),
)
schema.add("ImageEmbedding", ImageEmbeddingSchemaElement(ref_col_name="ImageEmbedding"))
schema.add(
    "MistakeScores",
    MistakeScoreSchemaElement(ref_col_name="Annotations"),
)

run_name = f"loader_cityscapes_train-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# satsure-prod
test_session = TestSession(
    project_name="testingProject", run_name=run_name, profile="dev1"
)

cred = DatasetCreds(region="us-east-2")

# 1. Loading the image URLs
# create test_ds object of Dataset instance
dataset_name = "cityscape_rupali"
test_ds = Dataset(
    test_session=test_session,
    name=dataset_name,
    type=DATASET_TYPE.IMAGE,
    data=pd_data_frame,
    schema=schema,
    creds=cred,
    temp=False,
)

# load to server
# pd_data_frame.to_csv(
#     f"/home/ubuntu/1.1Tdisk/DatasetUpload/cityscapes/{dataset_name}_before_embedding.csv"
# )
test_ds.load()

# 2. Generation of embeddings and uploading it
# model_exe_fun = ModelExecutorFactory().get_model_executor(
#     test_session=test_session,
#     model_name="Satsure Embedding Model",
#     version="0.1.1",
#     wheel_path="/home/ubuntu/1000GB/Embedding-Generator-Package/dist/raga_models-0.1.2-cp310-cp310-linux_x86_64.whl",
# )

# df = model_exe_fun.execute(
#     init_args={"device": "cuda:0"},
#     execution_args={
#         "input_columns": {"img_paths": "ImageUri"},
#         "output_columns": {"embedding": "ImageEmbedding"},
#         "column_schemas": {
#             "embedding": ImageEmbeddingSchemaElement(model="Satsure Embedding Model")
#         },
#     },
#     data_frame=test_ds,
# )

# df.to_csv(
#     f"/home/ubuntu/1.1Tdisk/DatasetUpload/super_resolution/{dataset_name}_after_lr_embedding_1.csv"
# )
# # test_ds.load()


# # # 3. Test labellling Consistency and add Mistake Score
# model_exe_fun = ModelExecutorFactory().get_model_executor(
#     test_session=test_session,
#     model_name="Satsure Mistake Score Model",
#     version="0.1.1",
#     wheel_path="/home/ubuntu/300GB/SatSure/annotation_quality/annotation_consistency/autoencoder-based/package/dist/raga_models-0.1.7.32-py3-none-any.whl",
# )

# df = model_exe_fun.execute(
#     init_args={
#         "device": "cpu",
#         "image_folders": [
#             "/home/ubuntu/1.1Tdisk/DatasetUpload/cityscape_train_images_half/image"
#         ],
#         "annotation_folders": [
#             "/home/ubuntu/1.1Tdisk/DatasetUpload/cityscape_val_data_inc_div/train_images/train_label_images"
#         ],
#     },
#     execution_args={
#         "input_columns": {"img_paths": "ImageUri"},
#         "output_columns": {"mistake_score": "MistakeScores"},
#         "column_schemas": {
#             "mistake_score": MistakeScoreSchemaElement(ref_col_name="Annotations")
#         },
#     },
#     data_frame=test_ds,
# )
# df.to_csv(
#     "/home/ubuntu/1.1Tdisk/DatasetUpload/cityscapes/cityscape_train_null_1_mistake_score.csv"
# )

# # test_ds.load()
