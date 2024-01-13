from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.zeiteinheit import Zeiteinheit


class Zeitraum(BaseModel):
    """
    Diese Komponente wird zur Abbildung von Zeiträumen in Form von Dauern oder der Angabe von Start und Ende verwendet.
    Es muss daher eine der drei Möglichkeiten angegeben sein:
    - Einheit und Dauer oder
    - Zeitraum: Startdatum bis Enddatum oder
    - Zeitraum: Startzeitpunkt (Datum und Uhrzeit) bis Endzeitpunkt (Datum und Uhrzeit)

    .. raw:: html

        <object data="../_static/images/bo4e/com/Zeitraum.svg" type="image/svg+xml"></object>

    .. HINT::
        `Zeitraum JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Zeitraum.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    dauer: Annotated[float | str | None, Field(None, title="Dauer")]
    einheit: Zeiteinheit | None = None
    enddatum: Annotated[datetime | None, Field(None, title="Enddatum")]
    endzeitpunkt: Annotated[datetime | None, Field(None, title="Endzeitpunkt")]
    startdatum: Annotated[datetime | None, Field(None, title="Startdatum")]
    startzeitpunkt: Annotated[datetime | None, Field(None, title="Startzeitpunkt")]
