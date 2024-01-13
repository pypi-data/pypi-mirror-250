from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.messwertstatus import Messwertstatus
from ..enum.messwertstatuszusatz import Messwertstatuszusatz


class Zeitreihenwert(BaseModel):
    """
    Abbildung eines Zeitreihenwertes bestehend aus Zeitraum, Wert und Statusinformationen.

    .. raw:: html

        <object data="../_static/images/bo4e/com/Zeitreihenwert.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zeitreihenwert JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Zeitreihenwert.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    datum_uhrzeit_bis: Annotated[datetime | None, Field(None, alias="datumUhrzeitBis", title="Datumuhrzeitbis")]
    datum_uhrzeit_von: Annotated[datetime | None, Field(None, alias="datumUhrzeitVon", title="Datumuhrzeitvon")]
    status: Messwertstatus | None = None
    statuszusatz: Messwertstatuszusatz | None = None
    wert: Annotated[float | str | None, Field(None, title="Wert")]
