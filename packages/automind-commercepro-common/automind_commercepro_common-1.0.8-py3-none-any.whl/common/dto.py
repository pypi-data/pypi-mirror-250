from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel, field_serializer


class VariantDTO(BaseModel):
    id: uuid.UUID
    ean: str
    is_active: bool
    discount_rate: float
    vat_rate: float


class OfferDTO(BaseModel):
    id: Optional[int] = None
    price: float
    quantity: int
    supplier_id: int
    variant_id: uuid.UUID
    supplier_sku: str
    vat_rate: float
    discount_rate: float
    expired_at: Optional[datetime] = None


class OfferPriceDTO(BaseModel):
    variant_id: uuid.UUID
    offer_id: int
    supplier_id: int
    supplier_sku: str
    offer_price: float
    offer_vat_rate: float
    offer_discount_rate: float
    offer_quantity: int
    price_id: Optional[int]
    price_price: Optional[float]
    price_discount_rate: Optional[float]
    price_vat_rate: Optional[float]
    price_is_locked: Optional[bool]


class PriceDTO(BaseModel):
    id: Optional[int] = None
    offer_id: int
    price: float
    vat_rate: float
    discount_rate: float
    is_locked: bool = False
    is_supplier_locked: bool = False


class PriceLockDTO(BaseModel):
    id: Optional[int] = None
    variant_id: uuid.UUID
    price: float
    discount_rate: float
    vat_rate: float


class SupplierLockDTO(BaseModel):
    supplier_id: int
    variant_id: uuid.UUID


class SupplierDTO(BaseModel):
    id: int
    name: str
    min_processing_days: int
    max_processing_days: int
    reliability: str
    is_internal: bool
    is_dropshipper: bool
    offers_url: str
    is_active: bool
    discount_rate: float
