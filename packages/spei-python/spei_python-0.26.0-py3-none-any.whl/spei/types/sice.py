from enum import Enum


class TipoRespuestaAcuse(str, Enum):
    sincrona = 'sincrona'
    asincrona = 'asincrona'
