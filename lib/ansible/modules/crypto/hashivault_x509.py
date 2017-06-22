#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2017, Colin Woodcock <colin.woodcock@gmail.com>
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.


ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: hashivault_x509
author: "Colin Woodcock (@_colinw)"
version_added: "2.4"
short_description: Requests x509 certificates from Hashicorp Vault
description:
    - Requests x509 certificates from Hashicorp Vault
    - Supports forced install, reissue close/past expiry and skip if present
requirements:
    - "python-pyOpenSSL"
options:
    state:
        required: false
        default: "present"
        choices: [ present, absent ]
        description:
            - Whether the certificate signing request should exist or not, taking action if the state is different from what is stated.
    certificate:
    key:
'''

# TODO examples
EXAMPLES = '''
# Issue a new certificate from a Vault server
'''

# TODO return
RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule

try:
    from OpenSSL import crypto
except ImportError:
    pyopenssl_found = False
else:
    pyopenssl_found = True


class HashivaultError(Exception):
    pass


class HashivaultX509(object):

    def __init__(self, module):
        self.state = module.params['state']


    def exists(self):
        raise HashivaultError("Not implemented yet")

def main():

    module = AnsibleModule(
        argument_spec = dict(
            state=dict(default='present', choices=['present','absent'], type='str'),
            certificate=dict(type='str'),
            key=dict(type='str'),
        ),
    )

    if not pyopenssl_found:
        module.fail_json(msg='the python pyOpenSSL module is required')

    result = dict(
        debug = 'hello world',
    )

    module.exit_json(**result)

if __name__ == '__main__':
    main()
