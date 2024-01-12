from pyspark.sql import SparkSession
import sys
import os
import urllib3
import boto3
import json

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Suppress only the InsecureRequestWarning from urllib3 needed in this case
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class S3DataUploader:

    def __init__(self, bucket_name=None):
        """
        Initialize S3DataLoader with an S3 client using configured credentials.

        Parameters:
        - None
        """
        self.bucket_name = bucket_name
        self.client = boto3.client('s3')
        self.resource = boto3.resource('s3')

    def pyspark_df_json_upload(self,df,output_format,output_path):

        """
        df : pysaprk dataframe
        output_format : format of the transformed-data
        output_path : output data stored location in s3
        """
        df.repartition.write.format(output_format).mode("overwrite").save(output_path)


    def main(self,df,output_format,output_path):
        """
        Interacts with the user, reads S3 data, and converts to json and displays json data info.
        """
        # #destination
        # s3_key = input(f"Enter S3 key for the {file_name} file:")
        # json_data = self.convert_df_to_json(df)
        # #upload json data to s3
        # self.upload_json_data_to_s3(json_data,bucket_name,file_name,s3_key)
        self.pyspark_df_json_upload(df,output_format,output_path)
       

if __name__ == "__main__":

    spark = SparkSession.builder.appName("luminex").getOrCreate()
    input_data= r'xxx'
    df = spark.read.csv(input_data,header=True,inferSchema=True)
    output_format= 'json'
    output_path = r'xxx'
    data_uploader = S3DataUploader()
    data_uploader.main(df)