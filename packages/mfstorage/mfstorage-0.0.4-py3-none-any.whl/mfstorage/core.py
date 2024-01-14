import arrow
from pydantic import (
    BaseModel,
    computed_field,
)


class Metadata(BaseModel):
    bucket: str
    pipe: str
    folder: str
    environment: str = "prod"
    timezone: str = 'UTC'

    class ConfigDict:
        arbitrary_types_allowed = True

    @computed_field
    def bucket_path(self) -> str:
        return f"s3://{self.bucket}"

    @computed_field
    def pipe_path(self) -> str:
        return f"s3://{self.bucket}/{self.pipe}"

    @computed_field
    def folder_path(self) -> str:
        return f"{self.bucket_path}/{self.pipe}/{self.folder}/{self.environment}"

    @computed_field
    def input_path(self) -> str:
        return f"{self.folder_path}/input_folder"

    @computed_field
    def output_path(self) -> str:
        return f"{self.folder_path}/output_folder"

    @computed_field
    def skip_path(self) -> str:
        return f"{self.folder_path}/skip_folder"

    @computed_field
    def archive_input_path(self) -> str:
        return f"{self.folder_path}/archive_input_folder"

    @computed_field
    def archive_output_path(self) -> str:
        return f"{self.folder_path}/archive_output_folder"

    @computed_field
    def archive_skip_path(self) -> str:
        return f"{self.folder_path}/archive_skip_folder"

    @computed_field
    def today(self) -> str:
        return arrow.now(self.timezone).format("YYYY-MM-DD")

    @computed_field
    def now(self) -> str:
        return arrow.now(self.timezone).isoformat()

    @computed_field
    def now_prefix(self) -> str:
        return arrow.now(self.timezone).format("YYYYMMDDHHmmss")
