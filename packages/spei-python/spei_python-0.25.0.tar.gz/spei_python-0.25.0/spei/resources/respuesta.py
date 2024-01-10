from lxml import etree
from pydantic import BaseModel

from spei import types
from spei.utils import to_snake_case, to_upper_camel_case  # noqa: WPS347


class Respuesta(BaseModel):
    id: str
    fecha_oper: int
    err_codigo: types.CodigoError
    err_descripcion: str
    categoria: types.CategoriaOrdenPago

    class Config:  # noqa: WPS306, WPS431
        use_enum_values = True

    def build_xml(self):
        qname = etree.QName('http://www.w3.org/2001/XMLSchema-instance', 'type')
        mensaje = etree.Element(
            'mensaje',
            {qname: 'mensaje'},
            categoria=self.categoria,
        )
        respuesta = etree.SubElement(mensaje, 'respuesta')

        for element, value in self.dict(exclude={'categoria'}).items():  # noqa: WPS110
            if element in self.__fields__:
                upper_camel_case_element = to_upper_camel_case(element)
                subelement = etree.SubElement(respuesta, upper_camel_case_element)
                subelement.text = str(value)

        return mensaje

    @classmethod
    def parse_xml(cls, mensaje_element):
        respuesta = mensaje_element.find('respuesta')

        respuesta_data = {
            'categoria': mensaje_element.attrib['categoria'],
        }

        for sub_element in respuesta.getchildren():
            tag = to_snake_case(sub_element.tag)
            respuesta_data[tag] = sub_element.text

        return cls(**respuesta_data)
