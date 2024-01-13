from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated


class File(BaseModel):
    """
    This class represents a file that is stored in the database.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    file_name_for_docstore: Annotated[str | None, Field(None, title="File Name For Docstore")]
    folder_name_for_docstore: Annotated[str | None, Field(None, title="Folder Name For Docstore")]
    file: Annotated[bytes, Field(title="File")]
