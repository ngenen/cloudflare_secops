# -*- coding: utf-8 -*-

# CloudFlare ``non-official´´ Security Operations Ansible Collection
# Copyright: (c) 2023, Nicolás Genen <ngenen@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from ansible_collections.ngenen.cloudflare_secops.plugins.module_utils.cf_base import CFBase, CloudFlare


class CFAccessRule(CFBase):
    def __init__(self, module):
        super().__init__(module)
        self.context = self.params['context']
        self.zone_id = None
        self.rules = None

    def initialize(self):
        super().initialize()

        if self.context == 'account':
            self.rules = self.api.accounts.firewall.access_rules.rules
        elif self.context == 'zone':
            self.rules = self.api.zones.firewall.access_rules.rules
            try:
                zone_name = self.action_params['zone']
                zones = self.api.zones(params={'name': zone_name})
                if zones:
                    self.zone_id = zones[0]['id']
                else:
                    raise Exception('The specified zone does not exist.')
            except KeyError:
                raise Exception('You need to specify a zone name')
        elif self.context == 'user':
            self.rules = self.api.user.firewall.access_rules.rules

    def add_rule(self):
        post_data = {
            'configuration': {
                'target': self.action_params['target'],
                'value': self.action_params['value'],
            },
            'mode': self.action_params['mode'],
            'notes': self.action_params['notes'],
        }

        try:
            if self.context == 'account':
                return True, self.rules.post(self.account_id, data=post_data)
            elif self.context == 'zone':
                return True, self.rules.post(self.zone_id, data=post_data)
            else:
                return True, self.rules.post(data=post_data)
        except CloudFlare.exceptions.CloudFlareError as err:
            return False, err

    def delete_rule(self):
        ok, rule_id = self.__search_rule()
        if not ok:
            return False, rule_id

        try:
            if self.context == 'account':
                return True, self.rules.delete(self.account_id, rule_id)
            elif self.context == 'zone':
                return True, self.rules.delete(self.zone_id, rule_id)
            else:
                return True, self.rules.delete(rule_id)
        except CloudFlare.exceptions.CloudFlareError as err:
            return False, 'Unable to delete rule: Error: %s' % err

    def __search_rule(self):
        target = self.action_params['target']
        value = self.action_params['value']

        try:
            if self.context == 'account':
                rules = self.rules(self.account_id)
            elif self.context == 'zone':
                rules = self.rules(self.zone_id)
            else:
                rules = self.rules()
        except CloudFlare.exceptions.CloudFlareError as err:
            return False, 'Unable to fetch rules. Error: %s' % err

        for rule in rules:
            if rule['configuration']['target'] == target and rule['configuration']['value'] == value:
                return True, rule['id']

        return False, 'Unable to locate the rule, please check search criteria'

    def update_rule(self):
        ok, rule_id = self.__search_rule()
        if not ok:
            return False, rule_id

        update_data = {
            'configuration': {
                'target': self.action_params['target'],
                'value': self.action_params['value'],
            },
            'mode': self.action_params['mode'],
            'notes': self.action_params['notes'],
        }

        try:
            if self.context == 'account':
                return True, self.rules.patch(self.account_id, rule_id, data=update_data)
            elif self.context == 'zone':
                return True, self.rules.patch(self.zone_id, rule_id, data=update_data)
            else:
                return True, self.rules.patch(rule_id, data=update_data)
        except CloudFlare.exceptions.CloudFlareError as err:
            return False, 'Unable to update the rule. Error: %s' % err
