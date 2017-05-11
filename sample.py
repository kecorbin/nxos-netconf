from devices import Nexus
#import xml.etree.ElementTree as ET
from lxml import etree as ET
import xmltodict
import logging

dist1 = Nexus('192.168.51.128', 'admin', 'R0yal5!!')
print ET.tostring(dist1.run_cmd('show version'))

#
#interfaces = dist1.run_cmd('show interface')
#int_objs = [objectify.fromstring(ET.tostring(i)) for i in interfaces]
#
#
# # list of interfaces as XML elements
# int_list = [i for i in interfaces.iterfind(".//{http://www.cisco.com/nxos:1.0:if_manager}ROW_interface")]
# # print int_list
#
# for i in int_list[0]:
#     print i.tag + "------" + i.text
#
# for i in int_list:
#     print i
#     # print i.text
#     # print ("===========================")
#     # print(ET.tostring(i, pretty_print=True))
