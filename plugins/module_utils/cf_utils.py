# -*- coding: utf-8 -*-

# CloudFlare ``non-official´´ Security Operations Ansible Collection
# Copyright: (c) 2023, Nicolás Genen <ngenen@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import env_fallback, missing_required_lib


def cf_handle_errors(module, err):
    error_str = str(err)
    if 'duplicate_of_existing' in error_str:
        return 'The object is duplicated.'
    elif 'not_entitled' in error_str:
        return 'Your account does not support the feature'

    module.fail_json(msg="Error: %s" % error_str)


def cf_parameters():
    return dict(
        email=dict(type='str',
                   required=True,
                   fallback=(env_fallback, ['CF_API_EMAIL']),
                   ),
        token=dict(type='str',
                   required=True,
                   fallback=(env_fallback, ['CF_API_KEY']),
                   ),
    )

