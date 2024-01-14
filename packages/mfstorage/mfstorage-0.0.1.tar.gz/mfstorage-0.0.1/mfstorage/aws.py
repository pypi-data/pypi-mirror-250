import boto3
from datetime import datetime, timezone
from botocore.exceptions import ClientError

def bucket_key_from_docpath(docpath):
    """
    Extracts the bucket name and key (prefix) from a full S3 document path.

    :param docpath: Full S3 path (e.g., 's3://bucket-name/prefix')
    :return: Tuple of (bucket_name, key)
    """
    full_path = docpath.split("//")[-1]
    bucket_name = full_path.split("/")[0]
    key = "/".join(full_path.split("/")[1:])
    return bucket_name, key

def list_docs(docpath, start=None, end=None):
    """
    Lists documents in an S3 bucket that are within the specified date range.

    :param docpath: Full S3 path to the bucket and optional prefix
    :param start: Start date as a string (optional)
    :param end: End date as a string (optional)
    :return: List of file paths in the S3 bucket that meet the criteria
    """
    try:
        s3 = boto3.client("s3")
        bucket_name, prefix = bucket_key_from_docpath(docpath)
        kwargs = {"Bucket": bucket_name, "MaxKeys": 1000}
        if prefix:
            kwargs["Prefix"] = prefix

        # Convert string dates to datetime objects, if provided
        if start:
            start = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
        if end:
            end = datetime.fromisoformat(end).replace(tzinfo=timezone.utc)

        files_list = []
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(**kwargs):
            for content in page.get('Contents', []):
                last_modified = content.get("LastModified")
                if (start and last_modified < start) or (end and last_modified > end):
                    continue
                if content.get("Key")[-1] != "/":  # Skip directories/folders
                    files_list.append(f"s3://{bucket_name}/{content.get('Key')}")

        return files_list
    except ClientError as e:
        # Handle AWS client errors (e.g., authentication issues, access denied)
        print(f"An error occurred: {e}")
        return []
    except Exception as e:
        # Handle other exceptions (e.g., parsing date strings)
        print(f"An unexpected error occurred: {e}")
        return []

# Example Usage
docpath = 's3://mfs-hutch/cashreceipting/acquired_pdfs/prod/input_folder/'  # Replace with your full S3 path
start_date = '2024-01-01'  # Optional
end_date = ''  # Optional
listed_files = list_docs(docpath, start_date, end_date)
print(len(listed_files))
