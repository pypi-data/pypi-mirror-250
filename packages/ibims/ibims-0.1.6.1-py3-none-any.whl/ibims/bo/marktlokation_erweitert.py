"""
extension of the official BO4E marktlokation
"""
from typing import Literal, Optional

from bo4e.bo.marktlokation import Marktlokation

from ibims.enum import Marktgebiet, MesstechnischeEinordnung, Regelzone
from ibims.enum.profiltyp import Profiltyp
from ibims.enum.prognosegrundlage import Prognosegrundlage


class MarktlokationErweitert(Marktlokation):
    """
    extension of the official BO4E marktlokation
    """

    messtechnische_einordnung: MesstechnischeEinordnung
    uebertragungsnetzgebiet: Optional[Regelzone]
    """
    uebertragungsnetzgebiet is for electricity
    """
    marktgebiet: Optional[Marktgebiet]
    """
    the gas equivalnt for uebertragungsnetzgebiet, where the Marktgebietscode is set
    """
    variant: Literal["Z14", "Z15"]
    """
        gridUsageBilling.variant (Netznutzungsabrechnungsvariante)
            Z14: WorkPriceBasicPrice (Arbeitspreis/Grundpreis)
            Z15: WorkPricePerformancePrice (Arbeitspreis/Leistungspreis)
    """
    community_id: str
    prognose_grundlage: Optional[Prognosegrundlage] = None
    """
    forecast type of a market location, ZA6: "Prognose auf Basis von Werten", ZC0: "Prognose auf Basis von Profilen"
    """
    prognose_grundlage_detail: Optional[Profiltyp] = None
    """
    forecast detail of a market location, E02: SLP/SEP, E14: TLP/TEP, Z36: TEP mit Referenzmessung
    """
