from enum import Enum


class AlertType(Enum):
    UNKNOWN = "UNKNOWN"
    AIR = "AIR"
    ARTILLERY = "ARTILLERY"
    URBAN_FIGHTS = "URBAN_FIGHTS"
    CHEMICAL = "CHEMICAL"
    NUCLEAR = "NUCLEAR"
    INFO = "INFO"


ALERT_TYPE_UA = {
    AlertType.ARTILLERY: "Загроза артобстрілу",
    AlertType.URBAN_FIGHTS: "Загроза вуличних боїв",
    AlertType.CHEMICAL: "Хімічна загроза",
    AlertType.NUCLEAR: "Радіаційна загроза",
    AlertType.INFO: "ЗМІ повідомляють про вибухи",
}

ALERT_TYPE_EN = {
    AlertType.ARTILLERY: "The threat of artillery fire",
    AlertType.URBAN_FIGHTS: "The threat of street fighting",
    AlertType.CHEMICAL: "Chemical threat",
    AlertType.NUCLEAR: "Nuclear threat",
    AlertType.INFO: "Media reports about explosions",
}
