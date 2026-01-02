import json
from logging import info
import xmltodict
import re

class packet:
    def __init__(self, name, extrainfo, servicefp, protocol, port):
        self.name = name
        self.extrainfo = extrainfo
        self.servicefp = servicefp
        self.protocol = protocol
        self.port = port
    
    def __str__(self):
        return (
            f"Port: {self.port}/{self.protocol} | "
            f"Service: {self.name} | "
            f"Extra: {self.extrainfo}"
        )    

def parser_xml2packet(xml):
    data = xmltodict.parse(xml)
    return json.dumps(data)

def parser_xml2packet(xml_file):
    with open(xml_file, "r", encoding="utf-8") as f:
        data = xmltodict.parse(f.read())

    ports = (
        data
        .get("nmaprun", {})
        .get("host", {})
        .get("ports", {})
        .get("port", [])
    )

    if isinstance(ports, dict):
        ports = [ports]

    objects = []

    for p in ports:
        service = p.get("service", {})

        obj = packet(
            name=service.get("@name"),
            extrainfo=service.get("@extrainfo"),
            servicefp=service.get("@servicefp"),
            protocol=p.get("@protocol"),
            port=p.get("@portid")
        )

        objects.append(obj)

    return objects

def print_objs(ob):
    for o in ob:
        print(o)