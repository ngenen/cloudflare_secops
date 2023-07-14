# -*- coding: utf-8 -*-

# CloudFlare ``non-official´´ Security Operations Ansible Collection
# Copyright: (c) 2023, Nicolás Genen <ngenen@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

import traceback
from ansible.module_utils.basic import missing_required_lib

try:
    import CloudFlare
except ImportError:
    HAS_CLOUDFLARE_LIBRARY = False
    CLOUDFLARE_LIBRARY_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_CLOUDFLARE_LIBRARY = True
    CLOUDFLARE_LIBRARY_IMPORT_ERROR = None


class CFAccessRule:
    def __init__(self, module_ref, email, key):
        if not HAS_CLOUDFLARE_LIBRARY:
            module_ref.fail_json(
                msg=missing_required_lib('CloudFlare'),
                exception=CLOUDFLARE_LIBRARY_IMPORT_ERROR)

        self.__cf = CloudFlare.CloudFlare(email=email, key=key)
        ok, self.__account_id = self._get_account_id()
        if not ok:
            raise Exception("Unable to gather account information, please check your credentials.")

    def _get_account_id(self):
        try:
            return True, self.__cf.accounts()[0]['id']
        except CloudFlare.exceptions.CloudFlareError as err:
            return False, err

    def account_rule_add(self, data):
        post_data = {
            'configuration': {
                'target': data['params']['target'],
                'value': data['params']['value'],
            },
            'mode': data['params']['mode'],
            'notes': data['params']['notes'],
        }

        try:
            return True, self.__cf.accounts.firewall.access_rules.rules.post(self.__account_id, data=post_data)
        except CloudFlare.exceptions.CloudFlareError as err:
            return False, err

    def _search_rule(self, data):
        target = data['params']['target']
        value = data['params']['value']
        ok, rules = self.account_rule_list()
        if not ok:
            return False, rules

        rule_id = ''
        for rule in rules:
            if rule['configuration']['target'] == target and rule['configuration']['value'] == value:
                rule_id = rule['id']
                break

        if rule_id:
            return True, rule_id
        else:
            return False, 'Unable to locate rule'

    def account_rule_delete(self, data):
        ok, rule_id = self._search_rule(data)
        if not ok:
            return False, rule_id

        try:
            return True, self.__cf.accounts.firewall.access_rules.rules.delete(self.__account_id, rule_id)
        except CloudFlare.exceptions.CloudFlareError as err:
            return False, err

    def account_rule_update(self, data):
        ok, rule_id = self._search_rule(data)
        if not ok:
            return False, rule_id

        update_data = {
            'configuration': {
                'target': data['params']['target'],
                'value': data['params']['value'],
            },
            'mode': data['params']['mode'],
            'notes': data['params']['notes'],
        }

        try:
            return True, self.__cf.accounts.firewall.access_rules.rules.patch(self.__account_id, rule_id,
                                                                              data=update_data)
        except CloudFlare.exceptions.CloudFlareError as err:
            return False, err

    def account_rule_list(self):
        try:
            return True, self.__cf.accounts.firewall.access_rules.rules(self.__account_id)
        except CloudFlare.exceptions.CloudFlareError as err:
            return False, err