# -*- coding: utf-8 -*-

# CloudFlare ``non-official´´ Security Operations Ansible Collection
# Copyright: (c) 2023, Nicolás Genen <ngenen@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from ansible.module_utils.basic import *
from ansible_collections.ngenen.cloudflare_secops.plugins.module_utils.cf_utils import cf_parameters, cf_handle_errors
from ansible_collections.ngenen.cloudflare_secops.plugins.module_utils.cf_access_rule import CFAccessRule

def main():
    fields = cf_parameters()
    fields.update(dict(
        params=dict(required=False, type="dict"),
        state=dict(type='str', default='present', choices=['absent', 'present', 'update']),
    ))

    module = AnsibleModule(argument_spec=fields)

    # Global Parameters
    email = module.params['email']
    token = module.params['token']
    state = module.params['state']

    result = dict(
        changed=False,
        failed=False,
        msg=''
    )

    try:
        cfr = CFAccessRule(module, email, token)
    except Exception as err:
        module.fail_json(msg=str(err))

    if state == 'present':
        ok, r = cfr.account_rule_add(module.params)
        if not ok:
            result['msg'] = cf_handle_errors(module, r)
        else:
            result['changed'] = True
            result['msg'] = 'A new account rule has been generated with id %s' % r['id']

    elif state == 'absent':
        ok, r = cfr.account_rule_delete(module.params)
        if not ok:
            result['msg'] = cf_handle_errors(module, r)
        else:
            result['changed'] = True
            result['msg'] = 'The rule id %s has been deleted.' % r['id']

    elif state == 'update':
        ok, r = cfr.account_rule_update(module.params)
        if not ok:
            result['msg'] = cf_handle_errors(module, r)
        else:
            result['changed'] = True
            result['msg'] = 'The rule id %s has been updated.' % r['id']

    module.exit_json(**result)


if __name__ == '__main__':
    main()
