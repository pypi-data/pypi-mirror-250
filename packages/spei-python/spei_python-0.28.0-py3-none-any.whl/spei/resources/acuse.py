from typing import Union

from lxml import etree
from pydantic import BaseModel

from spei.errors.sice import CodigoErrorAcuseBanxico, CodigoErrorAcuseServidor
from spei.types.sice import CodigoRespuestaAcuse, TipoRespuestaAcuse
from spei.utils import to_snake_case  # noqa: WPS347


class ResultadoBanxico(BaseModel):
    codigo: CodigoErrorAcuseBanxico
    descripcion: str = 'ND'

    class Config:  # noqa: WPS306, WPS431
        use_enum_values = True


class ResultadoServidor(BaseModel):
    codigo: Union[CodigoErrorAcuseServidor, CodigoRespuestaAcuse]
    descripcion: str = 'ND'

    class Config:  # noqa: WPS306, WPS431
        use_enum_values = True


class Acuse(BaseModel):
    cda_id: str
    mensaje_id: str
    tipo_respuesta: TipoRespuestaAcuse
    resultado_enlace_cep: ResultadoServidor = None
    resultado_banxico: ResultadoBanxico = None

    class Config:  # noqa: WPS306, WPS431
        use_enum_values = True

    def build_xml(self):
        qname = etree.QName('http://www.w3.org/2001/XMLSchema-instance', 'type')
        mensaje = etree.Element(
            'mensajeRespuestaCDA',
            {qname: 'mensajeRespuestaCDA'},
            tipoRespuesta=self.tipo_respuesta,
        )
        acuse = etree.SubElement(
            mensaje,
            'acuse',
            idCda=self.cda_id,
            idMensaje=self.mensaje_id,
        )

        etree.SubElement(
            acuse,
            'resultadoEnlaceCep',
            codigo=self.resultado_enlace_cep.codigo,
            descripcion=self.resultado_enlace_cep.descripcion,
        )

        etree.SubElement(
            acuse,
            'resultadoBanxico',
            codigo=self.resultado_banxico.codigo,
            descripcion=self.resultado_banxico.descripcion,
        )

        return mensaje

    @classmethod
    def parse_xml(cls, mensaje_element):
        acuse_element = mensaje_element.find('acuse')

        cda_data = cls._find_mensaje_attributes(mensaje_element, acuse_element)
        enlace_cep_data = cls._find_enlace_cep_attributes(acuse_element)
        banxico_data = cls._find_banxico_attributes(acuse_element)

        return cls._build_acuse(acuse_element, cda_data, enlace_cep_data, banxico_data)

    @classmethod
    def _find_enlace_cep_attributes(cls, acuse_element):
        resultado_element = acuse_element.find('resultadoEnlaceCep')
        return {
            'codigo': resultado_element.attrib['codigo'],
            'descripcion': resultado_element.attrib['descripcion'],
        }

    @classmethod
    def _find_banxico_attributes(cls, acuse_element):
        resultado_element = acuse_element.find('resultadoBanxico')
        return {
            'codigo': resultado_element.attrib['codigo'],
            'descripcion': resultado_element.attrib['descripcion'],
        }

    @classmethod
    def _find_mensaje_attributes(cls, mensaje_element, acuse_element):
        return {
            'tipo_respuesta': mensaje_element.attrib['tipoRespuesta'],
            'cda_id': acuse_element.attrib['idCda'],
            'mensaje_id': acuse_element.attrib['idMensaje'],
        }

    @classmethod
    def _build_acuse(cls, acuse_element, cda_data, enlace_cep_data, banxico_data):
        for element in acuse_element.getchildren():
            tag = to_snake_case(element.tag)
            if tag == 'resultado_enlace_cep':
                cda_data[tag] = ResultadoServidor(**enlace_cep_data)
                continue
            if tag == 'resultado_banxico':
                cda_data[tag] = ResultadoBanxico(**banxico_data)
                continue
            if tag in cls.__fields__:
                cda_data[tag] = element.text

        return cls(**cda_data)
