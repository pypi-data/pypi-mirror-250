from raga import *
import datetime

# run_name = "put_run_name"
run_name = f"QA_Drift_SS-Rupali-v5-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name= run_name, profile="dev1")
rules = DriftDetectionRules()
rules.add(type="anomaly_detection", dist_metric="Mahalanobis", _class="ALL", threshold=25)
#train_dataset_name="grasslands-v4",
#field_dataset_name="barrenlands-v4",
edge_case_detection = data_drift_detection(test_session=test_session,
                                           test_name="Drift-detection-test",
                                           train_dataset_name="grasslands-v4",
                                           field_dataset_name="barrenlands-v4",
                                           train_embed_col_name="ImageEmbedding",
                                           field_embed_col_name = "ImageEmbedding",
                                           output_type = "semantic_segmentation",
                                           level = "image",
                                           rules = rules)
#raga dev data sample-grasslands-final-v2,sample-barrenlands-final
# add payload into test_session object
test_session.add(edge_case_detection)
#run added test
test_session.run()