# -*- coding: utf-8 -*-

# CloudFlare ``non-official´´ Security Operations Ansible Collection
# Copyright: (c) 2023, Nicolás Genen <ngenen@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ngenen.cloudflare_secops.plugins.module_utils.cf_utils import cf_parameters, cf_handle_errors
from ansible_collections.ngenen.cloudflare_secops.plugins.module_utils.cf_access_rule import CFAccessRule


DOCUMENTATION = r'''
module: access_rule
short_description: Manage Access Rules
description:
- Add, delete and update access rules for CloudFlare WAF.
author:
- Nicolás Genen
options:
  params:
    description:
    - The module call parameters.
    - This is dictionary with key/value pair.
    - Possible values are zone, target, value, mode and notes.
    type: dict
  email:
    description:
    - The account email to manage the CloudFlare account.
    required: true
    type: str
  token:
    description:
    - The global api token to manage the CloudFlare account.
    required: true
    type: str
  state:
    description:
    -  Whether to add (C(present)), remove (C(absent)) or (C(update)) the access rule.
    choices: [absent, present, update]
    type: str
  context:
    description:
    -  The context for the current task, could be (C(account)) (this is default), (C(zone)) or (C(user)).
    choices: [account, zone, user]
    type: str
    
notes:
- This is a work in progress, please report any issue at https://github.com/ngenen/cloudflare_secops/issues.

'''

EXAMPLES = r'''
- name: Creating Access Rule (Account)
  ngenen.cloudflare_secops.access_rule:
    email: '{{ email }}'
    token: '{{ token }}'
    state: present
    params:
      target: 'ip'
      value: '1.2.3.4'
      mode: 'block'
      notes: 'Example IP Block'

- name: Creating Access Rule (Zone)
  ngenen.cloudflare_secops.access_rule:
    email: '{{ email }}'
    token: '{{ token }}'
    state: present
    context: zone
    params:
      zone: 'example.com'
      target: 'country'
      value: 'US'
      mode: 'challenge'
      notes: 'Example - Challenge US Country'
      
- name: Updating Access Rule (User)
  ngenen.cloudflare_secops.access_rule:
    email: '{{ email }}'
    token: '{{ token }}'
    state: update
    context: user
    params:
      target: 'ip'
      value: '1.2.3.4'
      mode: 'challenge'
      notes: 'Updated to challenge'

- name: Deleting Access Rule (Zone)
  ngenen.cloudflare_secops.access_rule:
    email: '{{ email }}'
    token: '{{ token }}'
    state: absent
    context: zone
    params:
      zone: 'example.com'
      target: 'ip'
      value: '1.2.3.4'
'''


def main():
    fields = cf_parameters()
    fields.update(dict(
        params=dict(required=False, type="dict"),
        state=dict(type='str', default='present', choices=['absent', 'present', 'update']),
        context=dict(type='str', default='account', choices=['zone', 'account', 'user'])
    ))

    module = AnsibleModule(argument_spec=fields)

    # Global Parameters
    state = module.params['state']

    result = dict(
        changed=False,
        failed=False,
        msg=''
    )

    cf = CFAccessRule(module)

    try:
        cf.initialize()
    except Exception as err:
        module.fail_json(msg=str(err))

    if state == 'present':
        ok, r = cf.add_rule()
        if not ok:
            result['msg'] = cf_handle_errors(module, r)
        else:
            result['changed'] = True
            result['msg'] = 'A new account rule has been generated with id %s' % r['id']

    elif state == 'absent':
        ok, r = cf.delete_rule()
        if not ok:
            result['msg'] = cf_handle_errors(module, r)
        else:
            result['changed'] = True
            result['msg'] = 'The rule id %s has been deleted.' % r['id']

    elif state == 'update':
        ok, r = cf.update_rule()
        if not ok:
            result['msg'] = cf_handle_errors(module, r)
        else:
            result['changed'] = True
            result['msg'] = 'The rule id %s has been updated.' % r['id']

    module.exit_json(**result)


if __name__ == '__main__':
    main()
