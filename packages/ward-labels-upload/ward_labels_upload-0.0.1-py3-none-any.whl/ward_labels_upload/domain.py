from pydantic import BaseModel


class Label(BaseModel):
    """ Represents a label for a given blockchain address.
    
    Attributes:
        address (str): The blockchain address.
        label (str): The label for the address. (e.g. "Binance")
        description (str): A description for the label. (e.g. "Binance 14)
    """
    address: str
    label: str
    description: str