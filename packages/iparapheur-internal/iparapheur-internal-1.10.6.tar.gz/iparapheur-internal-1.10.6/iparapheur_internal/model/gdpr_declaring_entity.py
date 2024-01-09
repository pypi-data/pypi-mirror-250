# coding: utf-8

"""
    iparapheur

    iparapheur v5.x main core application.  The main link between every sub-services, integrating business code logic.   # noqa: E501

    The version of the OpenAPI document: DEVELOP
    Contact: iparapheur@libriciel.coop
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from iparapheur_internal import schemas  # noqa: F401


class GdprDeclaringEntity(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            name = schemas.StrSchema
            address = schemas.StrSchema
            siret = schemas.StrSchema
            apeCode = schemas.StrSchema
            phoneNumber = schemas.StrSchema
            mail = schemas.StrSchema
        
            @staticmethod
            def dpo() -> typing.Type['GdprDeclaringEntityDpo']:
                return GdprDeclaringEntityDpo
        
            @staticmethod
            def responsible() -> typing.Type['GdprDeclaringEntityResponsible']:
                return GdprDeclaringEntityResponsible
            __annotations__ = {
                "name": name,
                "address": address,
                "siret": siret,
                "apeCode": apeCode,
                "phoneNumber": phoneNumber,
                "mail": mail,
                "dpo": dpo,
                "responsible": responsible,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["address"]) -> MetaOapg.properties.address: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["siret"]) -> MetaOapg.properties.siret: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["apeCode"]) -> MetaOapg.properties.apeCode: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["phoneNumber"]) -> MetaOapg.properties.phoneNumber: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["mail"]) -> MetaOapg.properties.mail: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["dpo"]) -> 'GdprDeclaringEntityDpo': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["responsible"]) -> 'GdprDeclaringEntityResponsible': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["name", "address", "siret", "apeCode", "phoneNumber", "mail", "dpo", "responsible", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["address"]) -> typing.Union[MetaOapg.properties.address, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["siret"]) -> typing.Union[MetaOapg.properties.siret, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["apeCode"]) -> typing.Union[MetaOapg.properties.apeCode, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["phoneNumber"]) -> typing.Union[MetaOapg.properties.phoneNumber, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["mail"]) -> typing.Union[MetaOapg.properties.mail, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["dpo"]) -> typing.Union['GdprDeclaringEntityDpo', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["responsible"]) -> typing.Union['GdprDeclaringEntityResponsible', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["name", "address", "siret", "apeCode", "phoneNumber", "mail", "dpo", "responsible", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
        address: typing.Union[MetaOapg.properties.address, str, schemas.Unset] = schemas.unset,
        siret: typing.Union[MetaOapg.properties.siret, str, schemas.Unset] = schemas.unset,
        apeCode: typing.Union[MetaOapg.properties.apeCode, str, schemas.Unset] = schemas.unset,
        phoneNumber: typing.Union[MetaOapg.properties.phoneNumber, str, schemas.Unset] = schemas.unset,
        mail: typing.Union[MetaOapg.properties.mail, str, schemas.Unset] = schemas.unset,
        dpo: typing.Union['GdprDeclaringEntityDpo', schemas.Unset] = schemas.unset,
        responsible: typing.Union['GdprDeclaringEntityResponsible', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'GdprDeclaringEntity':
        return super().__new__(
            cls,
            *_args,
            name=name,
            address=address,
            siret=siret,
            apeCode=apeCode,
            phoneNumber=phoneNumber,
            mail=mail,
            dpo=dpo,
            responsible=responsible,
            _configuration=_configuration,
            **kwargs,
        )

from iparapheur_internal.model.gdpr_declaring_entity_dpo import GdprDeclaringEntityDpo
from iparapheur_internal.model.gdpr_declaring_entity_responsible import GdprDeclaringEntityResponsible
