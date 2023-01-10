from pydantic import BaseModel
from datetime import date
from enum import Enum


class StatusTypeEnum(str, Enum):
    all = "all"
    completed = "completed"
    pending = "pending"
    suspended = "refunded"
    refunded = "refunded"


class PayinTypeEnum(str, Enum):
    poli = "poli_aus"
    bank_transfer = "bank_transfer_aus"
    wallet = "wallet_aus"
    pay_id = "poli_payid"


class Transaction(BaseModel):
    from_: date
    to: date
