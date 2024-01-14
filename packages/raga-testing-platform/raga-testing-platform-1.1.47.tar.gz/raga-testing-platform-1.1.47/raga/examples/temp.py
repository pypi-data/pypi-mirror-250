from raga import TestSession, OcrAnomalyRules, ocr_anomaly_test_analysis

run_name = f"3_Product_OCR_Outlier_testing"
project_name = "testingProject"

test_session = TestSession(project_name=project_name,run_name=run_name, profile="dev1")
rules = OcrAnomalyRules()
rules.add(type="anomaly_detection", dist_metric="DistanceMetric", threshold=0.2)



ocr_test = ocr_anomaly_test_analysis(test_session=test_session,
                                     dataset_name = "mychen_ocr_selfserve2",
                                     test_name = "ocr_anomaly_detection",
                                     model = "nanonet_model",
                                     type = "ocr",
                                     output_type="anomaly_detection",
                                     rules = rules)

test_session.add(ocr_test)

test_session.run()