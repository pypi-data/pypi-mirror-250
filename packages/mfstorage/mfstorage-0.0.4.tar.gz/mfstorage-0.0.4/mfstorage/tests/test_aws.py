# test_aws.py

from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from mfstorage.aws import (
    bucket_key_from_docpath,
    get_docpaths_to_process,
    get_output_docnames,
    list_docs,
)


def test_bucket_key_from_docpath():
    # Test with a standard path
    assert bucket_key_from_docpath("s3://my-bucket/my-folder/my-file.txt") == (
        "my-bucket",
        "my-folder/my-file.txt",
    )

    # Test with no prefix
    assert bucket_key_from_docpath("s3://my-bucket/") == ("my-bucket", "")

    # Test with a deeply nested path
    assert bucket_key_from_docpath("s3://my-bucket/folder1/folder2/file.txt") == (
        "my-bucket",
        "folder1/folder2/file.txt",
    )


@patch("mfstorage.aws.boto3.client")
def test_list_docs(mock_s3_client):
    # Mock S3 response
    mock_s3_client.return_value.get_paginator.return_value.paginate.return_value = [
        {
            "Contents": [
                {
                    "Key": "my-folder/my-file-1.txt",
                    "LastModified": datetime(2023, 1, 15, tzinfo=timezone.utc),
                },
                {
                    "Key": "my-folder/my-file-2.txt",
                    "LastModified": datetime(2023, 1, 20, tzinfo=timezone.utc),
                },
            ]
        }
    ]

    # Test filtering by dates
    result = list_docs("s3://my-bucket/my-folder", "2023-01-10", "2023-01-18")
    assert result == ["s3://my-bucket/my-folder/my-file-1.txt"]

    # Test with no date filters
    result = list_docs("s3://my-bucket/my-folder")
    assert result == [
        "s3://my-bucket/my-folder/my-file-1.txt",
        "s3://my-bucket/my-folder/my-file-2.txt",
    ]


class MockMetadata:
    def __init__(self, input_path):
        self.input_path = input_path


@pytest.fixture
def mock_metadata():
    return MockMetadata(input_path="s3://mybucket/input_folder")


@patch("mfstorage.aws.list_docs")
def test_get_output_docnames(mock_list_docs, mock_metadata):
    # Setup mock return values for list_docs
    mock_list_docs.side_effect = [
        [
            "s3://mybucket/skip_folder/doc1.txt",
            "s3://mybucket/skip_folder/doc2.txt",
        ],  # First call return
        [],  # Second call return
    ]

    # Call the function with mock metadata
    result = get_output_docnames(mock_metadata)
    assert result == ["doc1.txt", "doc2.txt"]


# @patch("mfstorage.aws.list_docs")
# def test_get_docpaths_to_process(mock_list_docs, mock_metadata):
#     # Setup mock return values for list_docs for each call
#     mock_list_docs.side_effect = [
#         ["s3://mybucket/output_folder/doc1.txt"],  # First call return for output folder
#         ["s3://mybucket/input_folder/doc1.txt", "s3://mybucket/input_folder/doc3.txt"],  # Second call return for input folder
#     ]
#     print(mock_metadata.input_path)
#     # Call the function with mock metadata
#     result = get_docpaths_to_process(mock_metadata)

#     # Assert based on the expected result
#     assert result == ["s3://mybucket/input_folder/doc3.txt"]
