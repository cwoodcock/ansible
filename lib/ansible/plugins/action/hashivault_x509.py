# Copyright 2017, Colin Woodcock <colin.woodcock@gmail.com>
#
# This file is part of Ansible
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

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class ActionModule(ActionBase):


    def __validate_arguments(args):
        self.result['failed'] = True

        with args:
        if (state is not None and state not in ['absent', 'present']):
            self.result['msg'] = 'Invalid state %s.  Can be "absent" or "present"(default)' % state
        elif (certificate is None or key is None):
            self.result['msg'] = 'certificate and key and key are required'
        else:
            del self.result['failed']


    def run(self, tmp=None, task_vars=None):

        if task_vars is None:
            task_vars = dict()

        self.result = super(ActionModule, self).run(tmp, task_vars)

        args = dict(
            state       = self._task.args.get('state', 'present')
            certificate = self._task.args.get('certificate', None)
            key         = self._task.args.get('key', None)
        )

        self.result.update(__validate_args(args))

        if self.result.get('failed'):
            return result

        # Default changed status
        self.result['changed'] = False


        certificate_stat = self._execute_remote_stat(certificate, all_vars=task_vars, follow=True, tmp=tmp, checksum=False)
        key_stat = self._execute_remote_stat(key, all_vars=task_vars, follow=True, tmp=tmp, checksum=False)

        if (state == 'present'):

            if (certificate_stat['exists'] and key_stat['exists']):
                display.v('check expiry')
                new_module_args = self._task.args.copy()
                result.update(self._execute_module(module_args=new_module_args, task_vars=task_vars, wrap_async=self._task.async))
                display.v('After executing module: %s' % result)
                # TODO check expiry
                expired = False

                if (expired):
                    # TODO issue cert
                    display.v('certificate expired, issuing a new one')
                    result['changed'] = True

            else:
                display.v('cert or key does not exist, issue new cert')
                # TODO issue cert
                result['changed'] = True

        elif (state == 'absent'):

            if (certificate_stat['exists']):
                file_args = dict(path=certificate,state='absent' )
                res = self._execute_module(module_name='file', module_args=file_args, tmp=tmp, task_vars=task_vars)
                display.v('Delete cert result: %s' % res)
                result['changed'] = res['changed']

            if (key_stat['exists']):
                file_args = dict(path=key,state='absent' )
                res = self._execute_module(module_name='file', module_args=file_args, tmp=tmp, task_vars=task_vars)
                display.v('Delete key result: %s' % res)
                result['changed'] = res['changed']

            # TODO merge file module results into ours

        return result
