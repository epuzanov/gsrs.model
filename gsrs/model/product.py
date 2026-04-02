from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Union

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_serializer, field_validator


class ProductBaseModel(BaseModel):
    """Base model for GSRS product payloads."""

    model_config = ConfigDict(
        extra='forbid',
        populate_by_name=True,
        json_encoders={datetime: lambda value: int(value.timestamp() * 1000)},
    )

    createdBy: Union[str, None] = Field(
        default=None,
        alias='createdBy',
        title='Created By',
        description='User that created the product record.',
    )
    modifiedBy: Union[str, None] = Field(
        default=None,
        alias='modifiedBy',
        title='Modified By',
        description='User that last modified the product record.',
    )
    creationDate: Union[datetime, None] = Field(
        default=None,
        alias='creationDate',
        title='Creation Date',
        description='Creation date of the product record.',
    )
    lastModifiedDate: Union[datetime, None] = Field(
        default=None,
        alias='lastModifiedDate',
        title='Last Modified Date',
        description='Last modified date of the product record.',
    )
    internalVersion: Union[int, None] = Field(
        default=None,
        alias='internalVersion',
        title='Internal Version',
        description='Internal version number of the product record.',
    )
    id: Union[int, None] = Field(
        default=None,
        alias='id',
        title='Identifier',
        description='Internal numeric identifier for the record.',
    )

    @field_validator('creationDate', 'lastModifiedDate', mode='before')
    @classmethod
    def _parse_unix_timestamp(cls, value):
        if isinstance(value, (int, float)):
            timestamp = value / 1000 if value > 10_000_000_000 else value
            return datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return value

    def model_dump(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        return super().model_dump(*args, **kwargs)

    def model_dump_json(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        return super().model_dump_json(*args, **kwargs)


class ProductTermAndPart(ProductBaseModel):
    """Product term and part detail."""

    productTerm: Union[str, None] = Field(
        default=None,
        alias='productTerm',
        title='Product Term',
        description='Product term.',
    )
    productTermPart: Union[str, None] = Field(
        default=None,
        alias='productTermPart',
        title='Product Term Part',
        description='Product term part.',
    )


class ProductCode(ProductBaseModel):
    """Product code detail."""

    productCode: Union[str, None] = Field(
        default=None,
        alias='productCode',
        title='Product Code',
        description='Product code.',
    )
    productCodeType: Union[str, None] = Field(
        default=None,
        alias='productCodeType',
        title='Product Code Type',
        description='Product code type.',
    )
    dailyMedUrl: Union[str, None] = Field(
        default=None,
        alias='_dailyMedUrl',
        title='DailyMed URL',
        description='DailyMed URL when provided by the source payload.',
    )


class ProductCompanyCode(ProductBaseModel):
    """Company code detail."""

    companyCode: Union[str, None] = Field(
        default=None,
        alias='companyCode',
        title='Company Code',
        description='Company code.',
    )
    companyCodeType: Union[str, None] = Field(
        default=None,
        alias='companyCodeType',
        title='Company Code Type',
        description='Company code type.',
    )


class ProductCompany(ProductBaseModel):
    """Company associated with a product provenance."""

    companyName: Union[str, None] = Field(
        default=None,
        alias='companyName',
        title='Company Name',
        description='Company name.',
    )
    companyAddress: Union[str, None] = Field(
        default=None,
        alias='companyAddress',
        title='Company Address',
        description='Company address.',
    )
    companyCity: Union[str, None] = Field(
        default=None,
        alias='companyCity',
        title='Company City',
        description='Company city.',
    )
    companyState: Union[str, None] = Field(
        default=None,
        alias='companyState',
        title='Company State',
        description='Company state.',
    )
    companyZip: Union[str, None] = Field(
        default=None,
        alias='companyZip',
        title='Company ZIP',
        description='Company ZIP or postal code.',
    )
    companyCountry: Union[str, None] = Field(
        default=None,
        alias='companyCountry',
        title='Company Country',
        description='Company country.',
    )
    companyGpsLatitude: Union[str, None] = Field(
        default=None,
        alias='companyGpsLatitude',
        title='Company GPS Latitude',
        description='Company GPS latitude.',
    )
    companyGpsLongitude: Union[str, None] = Field(
        default=None,
        alias='companyGpsLongitude',
        title='Company GPS Longitude',
        description='Company GPS longitude.',
    )
    companyGpsElevation: Union[str, None] = Field(
        default=None,
        alias='companyGpsElevation',
        title='Company GPS Elevation',
        description='Company GPS elevation.',
    )
    companyRole: Union[str, None] = Field(
        default=None,
        alias='companyRole',
        title='Company Role',
        description='Role of the company.',
    )
    companyPublicDomain: Union[str, None] = Field(
        default=None,
        alias='companyPublicDomain',
        title='Company Public Domain',
        description='Public-domain indicator for the company.',
    )
    startMarketingDate: Union[datetime, None] = Field(
        default=None,
        alias='startMarketingDate',
        title='Start Marketing Date',
        description='Start marketing date.',
    )
    endMarketingDate: Union[datetime, None] = Field(
        default=None,
        alias='endMarketingDate',
        title='End Marketing Date',
        description='End marketing date.',
    )
    companyProductId: Union[str, None] = Field(
        default=None,
        alias='companyProductId',
        title='Company Product ID',
        description='Company product identifier.',
    )
    companyDocumentId: Union[str, None] = Field(
        default=None,
        alias='companyDocumentId',
        title='Company Document ID',
        description='Company document identifier.',
    )
    provenanceDocumentId: Union[str, None] = Field(
        default=None,
        alias='provenanceDocumentId',
        title='Provenance Document ID',
        description='Provenance document identifier.',
    )
    productCompanyCodes: Union[List[ProductCompanyCode], None] = Field(
        default=None,
        alias='productCompanyCodes',
        title='Product Company Codes',
        description='Product company codes.',
    )

    @field_validator('endMarketingDate', 'startMarketingDate', mode='before')
    @classmethod
    def _parse_date_string(cls, value):
        if isinstance(value, str):
            # Attempt to parse the date string
            for fmt in ('%Y-%m-%d', '%m/%d/%Y'):
                try:
                    return datetime.strptime(value, fmt).astimezone(timezone.utc)
                except ValueError:
                    continue
        return value

    @field_serializer('endMarketingDate', 'startMarketingDate', when_used='always')
    def _serialize_date_string(self, value: Union[datetime, None]):
        if value is None:
            return None
        return value.strftime('%d/%m/%Y')


class ProductDocumentation(ProductBaseModel):
    """Documentation associated with a product provenance."""

    documentId: Union[str, None] = Field(
        default=None,
        alias='documentId',
        title='Document ID',
        description='Document identifier.',
    )
    documentType: Union[str, None] = Field(
        default=None,
        alias='documentType',
        title='Document Type',
        description='Document type.',
    )
    setIdVersion: Union[str, None] = Field(
        default=None,
        alias='setIdVersion',
        title='Set ID Version',
        description='Set ID version.',
    )
    effectiveTime: Union[str, None] = Field(
        default=None,
        alias='effectiveTime',
        title='Effective Time',
        description='Effective time.',
    )
    jurisdictions: Union[str, None] = Field(
        default=None,
        alias='jurisdictions',
        title='Jurisdictions',
        description='Jurisdictions covered by the document.',
    )


class ProductIndication(ProductBaseModel):
    """Product indication detail."""

    indication: Union[str, None] = Field(
        default=None,
        alias='indication',
        title='Indication',
        description='Indication.',
    )
    indicationText: Union[str, None] = Field(
        default=None,
        alias='indicationText',
        title='Indication Text',
        description='Indication text.',
    )
    indicationCode: Union[str, None] = Field(
        default=None,
        alias='indicationCode',
        title='Indication Code',
        description='Indication code.',
    )
    indicationCodeType: Union[str, None] = Field(
        default=None,
        alias='indicationCodeType',
        title='Indication Code Type',
        description='Indication code type.',
    )
    indicationGroup: Union[str, None] = Field(
        default=None,
        alias='indicationGroup',
        title='Indication Group',
        description='Indication group.',
    )
    indicationSource: Union[str, None] = Field(
        default=None,
        alias='indicationSource',
        title='Indication Source',
        description='Indication source.',
    )
    indicationSourceType: Union[str, None] = Field(
        default=None,
        alias='indicationSourceType',
        title='Indication Source Type',
        description='Indication source type.',
    )
    indicationSourceUrl: Union[str, None] = Field(
        default=None,
        alias='indicationSourceUrl',
        title='Indication Source URL',
        description='Indication source URL.',
    )


class ProductName(ProductBaseModel):
    """Localized or provenance-specific product name."""

    productName: Union[str, None] = Field(
        default=None,
        alias='productName',
        title='Product Name',
        description='Product name.',
    )
    productNameType: Union[str, None] = Field(
        default=None,
        alias='productNameType',
        title='Product Name Type',
        description='Product name type.',
    )
    language: Union[str, None] = Field(
        default=None,
        alias='language',
        title='Language',
        description='Language of the product name.',
    )
    displayName: Union[bool, None] = Field(
        default=None,
        alias='displayName',
        title='Display Name',
        description='Whether the name is the display name.',
    )
    productTermAndParts: Union[List[ProductTermAndPart], None] = Field(
        default=None,
        alias='productTermAndParts',
        title='Product Term And Parts',
        description='Product term and part entries.',
    )


class ProductManufacturer(ProductBaseModel):
    """Manufacturer for a manufactured item."""

    manufacturerName: Union[str, None] = Field(
        default=None,
        alias='manufacturerName',
        title='Manufacturer Name',
        description='Manufacturer name.',
    )
    manufacturerRole: Union[str, None] = Field(
        default=None,
        alias='manufacturerRole',
        title='Manufacturer Role',
        description='Manufacturer role.',
    )
    manufacturerCode: Union[str, None] = Field(
        default=None,
        alias='manufacturerCode',
        title='Manufacturer Code',
        description='Manufacturer code.',
    )
    manufacturerCodeType: Union[str, None] = Field(
        default=None,
        alias='manufacturerCodeType',
        title='Manufacturer Code Type',
        description='Manufacturer code type.',
    )
    manufacturedItemCode: Union[str, None] = Field(
        default=None,
        alias='manufacturedItemCode',
        validation_alias=AliasChoices('manufacturedItemCode', 'manufactureItemCode'),
        title='Manufactured Item Code',
        description='Manufactured item code.',
    )
    manufacturedItemCodeType: Union[str, None] = Field(
        default=None,
        alias='manufacturedItemCodeType',
        validation_alias=AliasChoices('manufacturedItemCodeType', 'manufactureItemCodeType'),
        title='Manufactured Item Code Type',
        description='Manufactured item code type.',
    )


class ProductIngredient(ProductBaseModel):
    """Ingredient present in a product lot."""

    applicantIngredName: Union[str, None] = Field(
        default=None,
        alias='applicantIngredName',
        title='Applicant Ingredient Name',
        description='Applicant ingredient name.',
    )
    substanceKey: Union[str, None] = Field(
        default=None,
        alias='substanceKey',
        title='Substance Key',
        description='Referenced substance key.',
    )
    substanceKeyType: Union[str, None] = Field(
        default=None,
        alias='substanceKeyType',
        title='Substance Key Type',
        description='Substance key type.',
    )
    basisOfStrengthSubstanceKey: Union[str, None] = Field(
        default=None,
        alias='basisOfStrengthSubstanceKey',
        title='Basis of Strength Substance Key',
        description='Basis of strength substance key.',
    )
    basisOfStrengthSubstanceKeyType: Union[str, None] = Field(
        default=None,
        alias='basisOfStrengthSubstanceKeyType',
        title='Basis of Strength Substance Key Type',
        description='Basis of strength substance key type.',
    )
    average: Union[float, None] = Field(
        default=None,
        alias='average',
        title='Average',
        description='Average amount.',
    )
    low: Union[float, None] = Field(
        default=None,
        alias='low',
        title='Low',
        description='Low amount.',
    )
    manufacturer: Union[str, None] = Field(
        default=None,
        alias='manufacturer',
        title='Manufacturer',
        description='Manufacturer reference.',
    )
    ingredLotNo: Union[str, None] = Field(
        default=None,
        alias='ingredLotNo',
        title='Ingredient Lot Number',
        description='Ingredient lot number.',
    )
    ingredientType: Union[str, None] = Field(
        default=None,
        alias='ingredientType',
        title='Ingredient Type',
        description='Ingredient type.',
    )
    ingredientFunction: Union[str, None] = Field(
        default=None,
        alias='ingredientFunction',
        title='Ingredient Function',
        description='Ingredient function.',
    )
    unit: Union[str, None] = Field(
        default=None,
        alias='unit',
        title='Unit',
        description='Unit of measure.',
    )
    releaseCharacteristic: Union[str, None] = Field(
        default=None,
        alias='releaseCharacteristic',
        title='Release Characteristic',
        description='Release characteristic.',
    )
    notes: Union[str, None] = Field(
        default=None,
        alias='notes',
        title='Notes',
        description='Ingredient notes.',
    )
    grade: Union[str, None] = Field(
        default=None,
        alias='grade',
        title='Grade',
        description='Ingredient grade.',
    )
    ingredientLocation: Union[str, None] = Field(
        default=None,
        alias='ingredientLocation',
        title='Ingredient Location',
        description='Ingredient location.',
    )
    ingredientLocationText: Union[str, None] = Field(
        default=None,
        alias='ingredientLocationText',
        title='Ingredient Location Text',
        description='Ingredient location text.',
    )
    confidentialityCode: Union[str, None] = Field(
        default=None,
        alias='confidentialityCode',
        title='Confidentiality Code',
        description='Confidentiality code.',
    )
    originalNumeratorNumber: Union[str, None] = Field(
        default=None,
        alias='originalNumeratorNumber',
        title='Original Numerator Number',
        description='Original numerator number.',
    )
    originalNumeratorUnit: Union[str, None] = Field(
        default=None,
        alias='originalNumeratorUnit',
        title='Original Numerator Unit',
        description='Original numerator unit.',
    )
    originalDenominatorNumber: Union[str, None] = Field(
        default=None,
        alias='originalDenominatorNumber',
        title='Original Denominator Number',
        description='Original denominator number.',
    )
    originalDenominatorUnit: Union[str, None] = Field(
        default=None,
        alias='originalDenominatorUnit',
        title='Original Denominator Unit',
        description='Original denominator unit.',
    )
    manufactureIngredientCatalogId: Union[str, None] = Field(
        default=None,
        alias='manufactureIngredientCatalogId',
        title='Manufacture Ingredient Catalog ID',
        description='Manufacture ingredient catalog identifier.',
    )
    manufactureIngredientUrl: Union[str, None] = Field(
        default=None,
        alias='manufactureIngredientUrl',
        title='Manufacture Ingredient URL',
        description='Manufacture ingredient URL.',
    )


class ProductLot(ProductBaseModel):
    """Manufacturing lot detail."""

    lotNo: Union[str, None] = Field(
        default=None,
        alias='lotNo',
        title='Lot Number',
        description='Lot number.',
    )
    lotSize: Union[str, None] = Field(
        default=None,
        alias='lotSize',
        title='Lot Size',
        description='Lot size.',
    )
    lotType: Union[str, None] = Field(
        default=None,
        alias='lotType',
        title='Lot Type',
        description='Lot type.',
    )
    expiryDate: Union[datetime, None] = Field(
        default=None,
        alias='expiryDate',
        title='Expiry Date',
        description='Expiry date.',
    )
    manufactureDate: Union[datetime, None] = Field(
        default=None,
        alias='manufactureDate',
        title='Manufacture Date',
        description='Manufacture date.',
    )
    productIngredients: Union[List[ProductIngredient], None] = Field(
        default=None,
        alias='productIngredients',
        title='Product Ingredients',
        description='Ingredients included in the lot.',
    )

    @field_validator('expiryDate', 'manufactureDate', mode='before')
    @classmethod
    def _parse_date_string(cls, value):
        if isinstance(value, str):
            # Attempt to parse the date string
            for fmt in ('%Y-%m-%d', '%m/%d/%Y'):
                try:
                    return datetime.strptime(value, fmt).astimezone(timezone.utc)
                except ValueError:
                    continue
        return value

    @field_serializer('expiryDate', 'manufactureDate', when_used='always')
    def _serialize_date_string(self, value: Union[datetime, None]):
        if value is None:
            return None
        return value.strftime('%d/%m/%Y')


class ProductProvenance(ProductBaseModel):
    """Source-system provenance for a product."""

    provenance: Union[str, None] = Field(
        default=None,
        alias='provenance',
        title='Provenance',
        description='Source provenance.',
    )
    productStatus: Union[str, None] = Field(
        default=None,
        alias='productStatus',
        title='Product Status',
        description='Status of the product in that provenance.',
    )
    productType: Union[str, None] = Field(
        default=None,
        alias='productType',
        title='Product Type',
        description='Product type.',
    )
    applicationType: Union[str, None] = Field(
        default=None,
        alias='applicationType',
        title='Application Type',
        description='Application type.',
    )
    applicationNumber: Union[str, None] = Field(
        default=None,
        alias='applicationNumber',
        title='Application Number',
        description='Application number.',
    )
    publicDomain: Union[str, None] = Field(
        default=None,
        alias='publicDomain',
        title='Public Domain',
        description='Public-domain indicator.',
    )
    isListed: Union[str, None] = Field(
        default=None,
        alias='isListed',
        title='Is Listed',
        description='Listing indicator.',
    )
    jurisdictions: Union[str, None] = Field(
        default=None,
        alias='jurisdictions',
        title='Jurisdictions',
        description='Jurisdictions.',
    )
    marketingCategoryName: Union[str, None] = Field(
        default=None,
        alias='marketingCategoryName',
        title='Marketing Category Name',
        description='Marketing category name.',
    )
    controlSubstanceCode: Union[str, None] = Field(
        default=None,
        alias='controlSubstanceCode',
        title='Control Substance Code',
        description='Control substance code.',
    )
    controlSubstanceClass: Union[str, None] = Field(
        default=None,
        alias='controlSubstanceClass',
        title='Control Substance Class',
        description='Control substance class.',
    )
    controlSubstanceSource: Union[str, None] = Field(
        default=None,
        alias='controlSubstanceSource',
        title='Control Substance Source',
        description='Control substance source.',
    )
    productUrl: Union[str, None] = Field(
        default=None,
        alias='productUrl',
        title='Product URL',
        description='Source URL for the product provenance.',
    )
    productNames: Union[List[ProductName], None] = Field(
        default=None,
        alias='productNames',
        title='Product Names',
        description='Product names.',
    )
    productCodes: Union[List[ProductCode], None] = Field(
        default=None,
        alias='productCodes',
        title='Product Codes',
        description='Product codes.',
    )
    productCompanies: Union[List[ProductCompany], None] = Field(
        default=None,
        alias='productCompanies',
        title='Product Companies',
        description='Product companies.',
    )
    productDocumentations: Union[List[ProductDocumentation], None] = Field(
        default=None,
        alias='productDocumentations',
        title='Product Documentations',
        description='Product documentation entries.',
    )
    productIndications: Union[List[ProductIndication], None] = Field(
        default=None,
        alias='productIndications',
        title='Product Indications',
        description='Product indications.',
    )


class ProductManufactureItem(ProductBaseModel):
    """Manufactured item detail for a product."""

    charSize: Union[str, None] = Field(
        default=None,
        alias='charSize',
        title='Characteristic Size',
        description='Characteristic size.',
    )
    charImprintText: Union[str, None] = Field(
        default=None,
        alias='charImprintText',
        title='Characteristic Imprint Text',
        description='Characteristic imprint text.',
    )
    charColor: Union[str, None] = Field(
        default=None,
        alias='charColor',
        title='Characteristic Color',
        description='Characteristic color.',
    )
    charFlavor: Union[str, None] = Field(
        default=None,
        alias='charFlavor',
        title='Characteristic Flavor',
        description='Characteristic flavor.',
    )
    charShape: Union[str, None] = Field(
        default=None,
        alias='charShape',
        title='Characteristic Shape',
        description='Characteristic shape.',
    )
    charNumFragments: Union[str, None] = Field(
        default=None,
        alias='charNumFragments',
        title='Characteristic Number of Fragments',
        description='Characteristic number of fragments.',
    )
    dosageForm: Union[str, None] = Field(
        default=None,
        alias='dosageForm',
        title='Dosage Form',
        description='Dosage form.',
    )
    dosageFormCode: Union[str, None] = Field(
        default=None,
        alias='dosageFormCode',
        title='Dosage Form Code',
        description='Dosage form code.',
    )
    dosageFormCodeType: Union[str, None] = Field(
        default=None,
        alias='dosageFormCodeType',
        title='Dosage Form Code Type',
        description='Dosage form code type.',
    )
    dosageFormNote: Union[str, None] = Field(
        default=None,
        alias='dosageFormNote',
        title='Dosage Form Note',
        description='Dosage form note.',
    )
    compositionNote: Union[str, None] = Field(
        default=None,
        alias='compositionNote',
        title='Composition Note',
        description='Composition note.',
    )
    routeOfAdministration: Union[str, None] = Field(
        default=None,
        alias='routeOfAdministration',
        title='Route Of Administration',
        description='Route of administration.',
    )
    amount: Union[int, None] = Field(
        default=None,
        alias='amount',
        title='Amount',
        description='Manufactured item amount.',
    )
    unit: Union[str, None] = Field(
        default=None,
        alias='unit',
        title='Unit',
        description='Manufactured item unit.',
    )
    provenanceManufactureItemId: Union[str, None] = Field(
        default=None,
        alias='provenanceManufactureItemId',
        title='Provenance Manufacture Item ID',
        description='Provenance manufacture item identifier.',
    )
    productManufacturers: Union[List[ProductManufacturer], None] = Field(
        default=None,
        alias='productManufacturers',
        title='Product Manufacturers',
        description='Product manufacturers.',
    )
    productLots: Union[List[ProductLot], None] = Field(
        default=None,
        alias='productLots',
        title='Product Lots',
        description='Product lots.',
    )


class Product(ProductBaseModel):
    """GSRS product model."""

    productContainer: Union[str, None] = Field(
        default=None,
        alias='productContainer',
        title='Product Container',
        description='Product container.',
    )
    routeAdmin: Union[str, None] = Field(
        default=None,
        alias='routeAdmin',
        title='Route Admin',
        description='Route of administration at product level.',
    )
    unitPresentation: Union[str, None] = Field(
        default=None,
        alias='unitPresentation',
        title='Unit Presentation',
        description='Unit presentation.',
    )
    countryCode: Union[str, None] = Field(
        default=None,
        alias='countryCode',
        title='Country Code',
        description='Country code.',
    )
    language: Union[str, None] = Field(
        default=None,
        alias='language',
        title='Language',
        description='Product language.',
    )
    shelfLife: Union[str, None] = Field(
        default=None,
        alias='shelfLife',
        title='Shelf Life',
        description='Shelf life.',
    )
    storageConditions: Union[str, None] = Field(
        default=None,
        alias='storageConditions',
        title='Storage Conditions',
        description='Storage conditions.',
    )
    numberOfManufactureItem: Union[str, None] = Field(
        default=None,
        alias='numberOfManufactureItem',
        title='Number Of Manufacture Item',
        description='Number of manufacture items.',
    )
    manufacturerName: Union[str, None] = Field(
        default=None,
        alias='manufacturerName',
        title='Manufacturer Name',
        description='Root manufacturer name.',
    )
    manufacturerCode: Union[str, None] = Field(
        default=None,
        alias='manufacturerCode',
        title='Manufacturer Code',
        description='Root manufacturer code.',
    )
    manufacturerCodeType: Union[str, None] = Field(
        default=None,
        alias='manufacturerCodeType',
        title='Manufacturer Code Type',
        description='Root manufacturer code type.',
    )
    effectiveDate: Union[datetime, None] = Field(
        default=None,
        alias='effectiveDate',
        title='Effective Date',
        description='Effective date.',
    )
    endDate: Union[datetime, None] = Field(
        default=None,
        alias='endDate',
        title='End Date',
        description='End date.',
    )
    productProvenances: Union[List[ProductProvenance], None] = Field(
        default=None,
        alias='productProvenances',
        title='Product Provenances',
        description='Product provenance entries.',
    )
    productManufactureItems: Union[List[ProductManufactureItem], None] = Field(
        default=None,
        alias='productManufactureItems',
        title='Product Manufacture Items',
        description='Product manufacture item entries.',
    )
    selfLink: Union[str, None] = Field(
        default=None,
        alias='_self',
        title='Self Link',
        description='Canonical API URL for the product record.',
    )

    @field_validator('effectiveDate', 'endDate', mode='before')
    @classmethod
    def _parse_date_string(cls, value):
        if isinstance(value, str):
            # Attempt to parse the date string
            for fmt in ('%Y-%m-%d', '%m/%d/%Y'):
                try:
                    return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
                except ValueError:
                    continue
        return value

    @field_serializer('effectiveDate', 'endDate', when_used='always')
    def _serialize_date_string(self, value: Union[datetime, None]):
        if value is None:
            return None
        return value.strftime('%d/%m/%Y')
