from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Annotated

from ..enum.ablesende_rolle import AblesendeRolle
from ..enum.ablesungsstatus import Ablesungsstatus
from ..enum.mengeneinheit import Mengeneinheit
from ..enum.messwertstatus import Messwertstatus
from ..enum.wertermittlungsverfahren import Wertermittlungsverfahren


class Verbrauch(BaseModel):
    """
    Abbildung eines zeitlich abgegrenzten Verbrauchs

    .. raw:: html

        <object data="../_static/images/bo4e/com/Verbrauch.svg" type="image/svg+xml"></object>

    .. HINT::
        `Verbrauch JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Verbrauch.json>`_
    """

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
    id: Annotated[str | None, Field(None, alias="_id", title=" Id")]
    einheit: Mengeneinheit | None = None
    enddatum: Annotated[datetime | None, Field(None, title="Enddatum")]
    obis_kennzahl: Annotated[str | None, Field(None, alias="obisKennzahl", title="Obiskennzahl")]
    startdatum: Annotated[datetime | None, Field(None, title="Startdatum")]
    wert: Annotated[float | str | None, Field(None, title="Wert")]
    wertermittlungsverfahren: Wertermittlungsverfahren | None = None
    ablesegrund: Annotated[str | None, Field(None, title="Ablesegrund")]
    ablesebeschreibung: Annotated[str | None, Field(None, title="Ablesebeschreibung")]
    periodenverbrauch: Annotated[float | str | None, Field(None, title="Periodenverbrauch")]
    periodenverbrauch_ursprung: Annotated[
        str | None, Field(None, alias="periodenverbrauchUrsprung", title="Periodenverbrauchursprung")
    ]
    ableser: AblesendeRolle | None = None
    status: Ablesungsstatus | None = None
    energiegehalt_gas: Annotated[float | str | None, Field(None, alias="energiegehaltGas", title="Energiegehaltgas")]
    energiegehalt_gas_gueltig_von: Annotated[
        datetime | None, Field(None, alias="energiegehaltGasGueltigVon", title="Energiegehaltgasgueltigvon")
    ]
    energiegehalt_gas_gueltig_bis: Annotated[
        datetime | None, Field(None, alias="energiegehaltGasGueltigBis", title="Energiegehaltgasgueltigbis")
    ]
    umwandlungsfaktor_gas: Annotated[
        float | str | None, Field(None, alias="umwandlungsfaktorGas", title="Umwandlungsfaktorgas")
    ]
    umwandlungsfaktor_gas_gueltig_von: Annotated[
        datetime | None, Field(None, alias="umwandlungsfaktorGasGueltigVon", title="Umwandlungsfaktorgasgueltigvon")
    ]
    umwandlungsfaktor_gas_gueltig_bis: Annotated[
        datetime | None, Field(None, alias="umwandlungsfaktorGasGueltigBis", title="Umwandlungsfaktorgasgueltigbis")
    ]
    messwertstatus: Messwertstatus | None = None
