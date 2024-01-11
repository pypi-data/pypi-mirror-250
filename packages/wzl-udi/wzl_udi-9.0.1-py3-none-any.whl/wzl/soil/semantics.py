import rdflib


class Semantics(object):
    prefix: str = None
    url: str = None
    namespace: rdflib.Namespace = None

    def __init__(self, config: dict[str, str]):
        Semantics.prefix = config['prefix']
        Semantics.url = config['url']
        Semantics.namespace = rdflib.Namespace(config['url'])


class Namespaces(object):
    m4i = rdflib.Namespace('http://w3id.org/nfdi4ing/metadata4ing#')
    quantitykind = rdflib.Namespace('http://qudt.org/vocab/quantitykind/')
    qudt = rdflib.Namespace('http://qudt.org/schema/qudt/')
    rdf = rdflib.namespace.RDF
    schema = rdflib.Namespace('https://schema.org/')
    si = rdflib.Namespace('https://ptb.de/si/')
    soil = rdflib.Namespace('https://purl.org/fair-sensor-services/soil#')
    sosa = rdflib.namespace.SOSA
    ssn = rdflib.namespace.SSN
    ssn_system = rdflib.Namespace('http://www.w3.org/ns/ssn/systems/')
    unit = rdflib.Namespace('http://qudt.org/vocab/unit/')
