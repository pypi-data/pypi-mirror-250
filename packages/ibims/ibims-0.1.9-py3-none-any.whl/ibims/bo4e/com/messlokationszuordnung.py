from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.arithmetische_operation import ArithmetischeOperation


class Messlokationszuordnung(BaseModel):
    """
    Mit dieser Komponente werden Messlokationen zu Marktlokationen zugeordnet.
    Dabei kann eine arithmetische Operation (Addition, Subtraktion, Multiplikation, Division) angegeben werden,
    mit der die Messlokation zum Verbrauch der Marktlokation beiträgt.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Messlokationszuordnung.svg" type="image/svg+xml"></object>

    .. HINT::
        `Messlokationszuordnung JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Messlokationszuordnung.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    arithmetik: ArithmetischeOperation | None = None
    gueltig_bis: Annotated[datetime | None, Field(None, alias="gueltigBis", title="Gueltigbis")]
    gueltig_seit: Annotated[datetime | None, Field(None, alias="gueltigSeit", title="Gueltigseit")]
    messlokations_id: Annotated[str | None, Field(None, alias="messlokationsId", title="Messlokationsid")]
