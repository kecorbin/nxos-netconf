# NX-OS netconf

This is the python libary for using cisco gear if you are a mere human....

Don't be scared. Just look..

# Installation

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Usage

Just launch a session and issue the same command(s) you are used to, and the output is returned as structured data
that we can parse (we'll get to that in just a second)

```
from devices import Nexus
dist1 = Nexus('192.168.51.128', 'admin', 'R0yal5!!')

```

You know have dist1 at your disposable via python, you can either output the command as it would appear in an interactive session with the device, or retrieve specific parameters by parsing a little XML.  (i know, it sucks, we'll get to that in a second.)

```
print ET.tostring(dist1.run_cmd('show version'))
print ET.tostring(dist1.run_cmd('show version'))
```


Outputs
```
<?xml version="1.0" encoding="ISO-8859-1"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:if="http://www.cisco.com/nxos:1.0:if_manager" xmlns:nfcli="http://www.cisco.com/nxos:1.0:nfcli" xmlns:nxos="http://www.cisco.com/nxos:1.0" xmlns:vlan_mgr_cli="http://www.cisco.com/nxos:1.0:vlan_mgr_cli" xmlns:mod="http://www.cisco.com/nxos:1.0:sysmgrcli" message-id="urn:uuid:20f33e19-721f-4794-9af0-4b1166ac7297">
 <data>
  <mod:show>
   <mod:version>
    <mod:__XML__OPT_Cmd_sysmgr_show_version___readonly__>
     <mod:__readonly__>
      <mod:header_str>Cisco Nexus Operating System (NX-OS) Software
TAC support: http://www.cisco.com/tac
Documents: http://www.cisco.com/en/US/products/ps9372/tsd_products_support_series_home.html
Copyright (c) 2002-2015, Cisco Systems, Inc. All rights reserved.
The copyrights to certain works contained herein are owned by
other third parties and are used and distributed under license.
Some parts of this software are covered under the GNU Public
License. A copy of the license is available at
http://www.gnu.org/licenses/gpl.html.

NX-OSv9K is a demo version of the Nexus Operating System
</mod:header_str>
      <mod:bios_ver_str></mod:bios_ver_str>
      <mod:kickstart_ver_str>7.0(3)I2(2)</mod:kickstart_ver_str>
      <mod:bios_cmpl_time></mod:bios_cmpl_time>
      <mod:kick_file_name>bootflash:///nxos.7.0.3.I2.2.bin</mod:kick_file_name>
      <mod:kick_cmpl_time> 11/9/2015 23:00:00</mod:kick_cmpl_time>
      <mod:kick_tmstmp>11/10/2015 07:59:54</mod:kick_tmstmp>
      <mod:chassis_id>NX-OSv Chassis</mod:chassis_id>
      <mod:cpu_name>Intel(R) Core(TM) i7-4770HQ CPU @ 2.20GHz</mod:cpu_name>
      <mod:memory>8165892</mod:memory>
      <mod:mem_type>kB</mod:mem_type>
      <mod:host_name>switch</mod:host_name>
      <mod:bootflash_size>1747849</mod:bootflash_size>
      <mod:kern_uptm_days>0</mod:kern_uptm_days>
      <mod:kern_uptm_hrs>0</mod:kern_uptm_hrs>
      <mod:kern_uptm_mins>34</mod:kern_uptm_mins>
      <mod:kern_uptm_secs>15</mod:kern_uptm_secs>
      <mod:rr_reason>Unknown</mod:rr_reason>
      <mod:rr_sys_ver></mod:rr_sys_ver>
      <mod:rr_service></mod:rr_service>
      <mod:manufacturer>Cisco Systems, Inc.</mod:manufacturer>
     </mod:__readonly__>
    </mod:__XML__OPT_Cmd_sysmgr_show_version___readonly__>
   </mod:version>
  </mod:show>
 </data>
</rpc-reply>
```


# Finding Specific Values
```
version = dist1.run_cmd('show version')

for e in version.getiterator():
    print e.tag, '-', e.text

print(version.find(".//{http://www.cisco.com/nxos:1.0:sysmgrcli}kickstart_ver_str").text) # 7.0(3)I2(2)
ver = [ b.text for b in version.iterfind(".//{http://www.cisco.com/nxos:1.0:sysmgrcli}kickstart_ver_str")] # ['7.0(3)I2(2)']
print ver
```

# Further reading

https://docs.python.org/2/library/xml.etree.elementtree.html
