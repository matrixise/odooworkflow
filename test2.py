from pprint import pprint as pp
import lxml
from lxml import etree


import pytest

def main():
    with open('example2.wkf') as fp:
        parser = yacc.yacc(debug=False) #, debuglog=log)
        workflow = parser.parse(fp.read())
        pp(workflow)

    #print(workflow)

    #while True:
    #    tok = lexer.token()
    #    if not tok:
    #        break
    #    print(tok)



#def to_odoo_xml(workflow):
#    openerp_tag = etree.Element('openerp')
#    data_tag = etree.SubElement(openerp_tag, 'data')
#
#    workflow.to_xml(data_tag)
#    return openerp_tag

#root = to_odoo_xml(workflow)
#
#etree.dump(root, pretty_print=True)
#
#with open('demo.xml', 'wb') as fp:
#    result = etree.tostring(
#        root,
#        pretty_print=True,
#        xml_declaration=True,
#        encoding='utf-8'
#    )
#    fp.write(result)
