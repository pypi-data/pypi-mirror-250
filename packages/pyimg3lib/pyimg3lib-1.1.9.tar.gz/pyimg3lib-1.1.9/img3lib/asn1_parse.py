
from asn1 import Encoder, Decoder, Numbers, Types, Classes


class CertParser:
    def __init__(self, data) -> None:
        self.data = data
        self.encoder = Encoder()
        self.decoder = Decoder()

    # Numbers, Types, Classes string hack (.name)

    def getClass(self, tag):
        for _class in Classes:
            if tag.cls == _class:
                return _class

    def getType(self, tag):
        for _type in Types:
            if tag.typ == _type:
                return _type

    def getNumber(self, tag):
        for _number in Numbers:
            if tag.nr == _number:
                return _number

    def readTag(self):
        return self.decoder.read()

    def getTagInfo(self, tag):
        info = {
            '_class': self.getClass(tag),
            '_type': self.getType(tag),
            '_number': self.getNumber(tag)
        }

        return info

    def decodeTagData(self, tag, value):
        pass

    def readTagData(self, tag, value):
        tag_info = self.getTagInfo(tag)

        tag_data = self.decodeTagData(tag, value)

        pass

    def readCertificate(self):
        self.decoder.start(self.data)

        while not self.decoder.eof():
            tag = self.decoder.peek()

            if tag is None:
                break

            tag_info = self.getTagInfo(tag)

            if tag_info['_type'] == Types.Constructed:
                # self.decoder.enter()
                # self.decoder.leave()

                pass

            elif tag_info['_type'] == Types.Primitive:
                tag, value = self.readTag()

                pass

            else:
                raise Exception(f'Unknown class: {tag_info["_class"]}')

            pass
