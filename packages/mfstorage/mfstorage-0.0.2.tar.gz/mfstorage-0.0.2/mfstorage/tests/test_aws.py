# test_aws.py

from datetime import datetime, timezone

from unittest.mock import patch
from mfstorage.aws import bucket_key_from_docpath, list_docs

def test_bucket_key_from_docpath():
    # Test with a standard path
    assert bucket_key_from_docpath('s3://my-bucket/my-folder/my-file.txt') == ('my-bucket', 'my-folder/my-file.txt')

    # Test with no prefix
    assert bucket_key_from_docpath('s3://my-bucket/') == ('my-bucket', '')

    # Test with a deeply nested path
    assert bucket_key_from_docpath('s3://my-bucket/folder1/folder2/file.txt') == ('my-bucket', 'folder1/folder2/file.txt')

    # Test with an invalid path (should design the function to handle this case as needed)
    # assert bucket_key_from_docpath('invalid-path') == (None, None)

@patch('mfstorage.aws.boto3.client')
def test_list_docs(mock_s3_client):
    # Mock S3 response
    mock_s3_client.return_value.get_paginator.return_value.paginate.return_value = [
        {
            'Contents': [
                {'Key': 'my-folder/my-file-1.txt', 'LastModified': datetime(2023, 1, 15, tzinfo=timezone.utc)},
                {'Key': 'my-folder/my-file-2.txt', 'LastModified': datetime(2023, 1, 20, tzinfo=timezone.utc)},
            ]
        }
    ]

    # Test filtering by dates
    result = list_docs('s3://my-bucket/my-folder', '2023-01-10', '2023-01-18')
    assert result == ['s3://my-bucket/my-folder/my-file-1.txt']

    # Test with no date filters
    result = list_docs('s3://my-bucket/my-folder')
    assert result == ['s3://my-bucket/my-folder/my-file-1.txt', 's3://my-bucket/my-folder/my-file-2.txt']
