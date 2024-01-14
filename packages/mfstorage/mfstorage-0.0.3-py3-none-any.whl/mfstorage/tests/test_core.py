import arrow

from dateutil.parser import parse

from mfstorage.core import Metadata

def test_bucket_path():
    metadata = Metadata(bucket="mybucket", pipe="mypipe", folder="myfolder", timezone="UTC")
    assert metadata.bucket_path == "s3://mybucket"

def test_pipe_path():
    metadata = Metadata(bucket="mybucket", pipe="mypipe", folder="myfolder", timezone="UTC")
    assert metadata.pipe_path == "s3://mybucket/mypipe"

def test_folder_path():
    metadata = Metadata(bucket="mybucket", pipe="mypipe", folder="myfolder", environment="dev", timezone="UTC")
    assert metadata.folder_path == "s3://mybucket/mypipe/myfolder/dev"

def test_input_path():
    metadata = Metadata(bucket="mybucket", pipe="mypipe", folder="myfolder", timezone="UTC")
    assert metadata.input_path == "s3://mybucket/mypipe/myfolder/prod/input_folder"

def test_output_path():
    metadata = Metadata(bucket="mybucket", pipe="mypipe", folder="myfolder", timezone="UTC")
    assert metadata.output_path == "s3://mybucket/mypipe/myfolder/prod/output_folder"

def test_skip_path():
    metadata = Metadata(bucket="mybucket", pipe="mypipe", folder="myfolder", timezone="UTC")
    assert metadata.skip_path == "s3://mybucket/mypipe/myfolder/prod/skip_folder"

def test_today():
    timezone = "UTC"
    metadata = Metadata(bucket="mybucket", pipe="mypipe", folder="myfolder", timezone=timezone)
    expected_date = arrow.now(timezone).format("YYYY-MM-DD")
    assert metadata.today == expected_date

def test_now():
    timezone = "UTC"
    metadata = Metadata(bucket="mybucket", pipe="mypipe", folder="myfolder", timezone=timezone)
    try:
        parse(metadata.now)
        parsed = True
    except ValueError:
        parsed = False
    assert parsed  # This asserts that the string is a valid date-time format


def test_now_prefix():
    timezone = "UTC"
    metadata = Metadata(bucket="mybucket", pipe="mypipe", folder="myfolder", timezone=timezone)
    expected_prefix = arrow.now(timezone).format("YYYYMMDDHHmmss")
    assert metadata.now_prefix == expected_prefix

