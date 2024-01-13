from lxml import etree

from spei.resources import Acuse

SOAP_NS = 'http://schemas.xmlsoap.org/soap/envelope/'
XML_SCHEMA_NS = 'http://www.w3.org/2001/XMLSchema-instance'


class MensajeElement(object):
    def __new__(cls, acuse: Acuse):
        qname = etree.QName(XML_SCHEMA_NS, 'type')

        mensaje = etree.Element(
            'mensajeRespuestaCDA',
            {qname: 'mensajeRespuestaCDA'},
            tipoRespuesta=acuse.tipo_respuesta,
        )

        mensaje.append(acuse.build_xml())

        return mensaje


class BodyElement(object):
    def __new__(cls, acuse):
        body = etree.Element(etree.QName(SOAP_NS, 'Body'))
        body.append(acuse)
        return body


class EnvelopeElement(object):
    def __new__(cls, body):
        etree.register_namespace('soap', SOAP_NS)
        envelope = etree.Element(etree.QName(SOAP_NS, 'Envelope'))
        envelope.append(body)
        return envelope


class AcuseRequest(object):
    def __new__(cls, acuse: Acuse, as_string=True):
        envelope = EnvelopeElement(BodyElement(MensajeElement(acuse)))
        if not as_string:
            return envelope
        return etree.tostring(envelope, xml_declaration=True, encoding='utf-8')
