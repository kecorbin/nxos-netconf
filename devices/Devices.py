#!/usr/bin/env python
from lxml import etree as ET
from lxml import objectify
from ncclient import manager
import helpers
import xmltodict

class Nexus(object):
    """
    Class for gleaning useful information from an NX-OS device.

    """

    def __init__(self, host, user, passwd, **kwargs):

        self.args = kwargs
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = 22
        self.hostkey_verify = False
        self.device_params = {'name': 'nexus'}
        self.allow_agent = False
        self.look_for_keys = False
        self.manager = manager.connect(host=self.host,
                                       port=22,
                                       username=self.user,
                                       password=self.passwd,
                                       hostkey_verify=False,
                                       # ssh_subsystem_name must be declared as of 7.0(3)I5
                                       device_params={'name': 'nexus','ssh_subsystem_name' : 'xmlagent'},
                                       allow_agent=False,
                                       look_for_keys=False)


    def build_xml(self, cmd):
        """
        build Netconf XML for a basic command, this should work pretty good for most
        show commands
        """

        args = cmd.split(' ')
        xml = ""
        for a in reversed(args):
            xml = """<%s>%s</%s>""" % (a, xml, a)
        return xml

    def run_cmd(self, cmd):
        xml = self.build_xml(cmd)
        ncdata = str(self.manager.get(('subtree', xml)))
        try:
            # we return valid XML
            root = ET.fromstring(ncdata)
            return root

        except:
            # somthing f'd up we'll return it as a we got it back
            return ncdata

    def version_dict(self):
        version = self.run_cmd('show version')
        for data in version.iter(tag='{http://www.cisco.com/nxos:1.0:sysmgrcli}__readonly__'):
            print data.getchildren()
        return version

    @staticmethod
    def to_html_table(xmlstr, nsdict=None):
        """
        convert xml table to html
        """
        raise NotImplemented

    @staticmethod
    def format_mac_address(mac):
        """
        Re-format IOS mac addresses
        :param mac: string mac address in 0000.0000.0000 format
        :return: string 00:00:00:00:00
        """
        return '{0}:{1}:{2}:{3}:{4}:{5}'.format(mac[:2],
                                                mac[2:4],
                                                mac[5:7],
                                                mac[7:9],
                                                mac[10:12],
                                                mac[12:14])


    def search_for_prefix(self, prefix):
        """
        Find VRF name containing a prefix
        """
        query = self.build_xml('show ip route vrf all')
        ncdata = str(self.manager.get(('subtree', query)))
        root = ET.fromstring(ncdata)
        mod = {'mod': 'http://www.cisco.com/nxos:1.0:urib'}

        # it is entirely possible that the prefix could exist in many prefixes
        vrfs = list()

        for vrf in root.iter(tag='{http://www.cisco.com/nxos:1.0:urib}ROW_vrf'):
            name = vrf.find('mod:vrf-name-out', mod)
            for pfx in vrf.iter(tag='{http://www.cisco.com/nxos:1.0:urib}ipprefix'):
                if pfx.text == prefix:
                    vrfs.append(name.text)

        return vrfs
