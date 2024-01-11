# import gzip
# import json
#
# input_file_path = '/Users/rupalitripathi/IdeaProjects/testing-platform-python-client/raga/examples/assets/hr_20k/embedding_store_hr_0.gzip'
# output_directory = '/Users/rupalitripathi/IdeaProjects/testing-platform-python-client/raga/examples/assets/chunksgzip/'
#
# # Define the number of datapoints per chunk
# chunk_size = 100
#
# def read_json_gzip(file_path):
#     with gzip.open(file_path, 'rt', encoding='utf-8') as file:
#         data = [json.loads(line) for line in file]
#     return data
#
# def write_json_gzip(file_path, data):
#     with gzip.open(file_path, 'wt', encoding='utf-8') as file:
#         for item in data:
#             file.write(json.dumps(item) + '\n')
#
# # Read the original file
# original_data = read_json_gzip(input_file_path)
#
# # Divide into chunks
# chunks = [original_data[i:i + chunk_size] for i in range(0, len(original_data), chunk_size)]
#
# # Save each chunk to a new file
# for i, chunk in enumerate(chunks):
#     output_file_path = f'{output_directory}chunk_{i}.gzip'
#     write_json_gzip(output_file_path, chunk)
#
# print(f'File divided into {len(chunks)} chunks.')

import gzip
import json

gzip_file_path = '/Users/rupalitripathi/IdeaProjects/testing-platform-python-client/raga/examples/assets/hr_20k/embedding_store_hr_0.gzip'
json_output_file_path = 'output.json'

def convert_gzip_to_json(gzip_file_path, json_output_file_path):
    with gzip.open(gzip_file_path, 'rt', encoding='utf-8') as gzip_file:
        data = json.load(gzip_file)

    with open(json_output_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2)  # Optional: indent for pretty printing

# Convert Gzip to JSON
convert_gzip_to_json(gzip_file_path, json_output_file_path)