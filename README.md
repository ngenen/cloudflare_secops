# Ansible Collection: ngenen.cloudflare_secops

This repo hosts the `ngenen.cloudflare_secops` Ansible Collection.

The collection includes some tools to automate security operations for cloudflare accounts.

## Installation

Use the ansible-galaxy manager to install the collection.

```bash
ansible-galaxy collection install ngenen.cloudflare_secops
```

## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.15.1**.

## Features

- Account - Access Rules [https://api.cloudflare.com/client/v4/accounts/{account_identifier}/firewall/access_rules/rules]

## Usage

Example Playbook

```yaml
- hosts: localhost
  collections:
    - ngenen.cloudflare_secops
  vars:
    email: '<account_email>'
    token: '<account_global_apikey>'
  tasks:
    - name: Creating CF Access Rule (Target IP)
      ngenen.cloudflare_secops.access_rule:
        email: '{{ email }}'
        token: '{{ token }}'
        state: present
        params:
          target: 'ip'
          value: '1.2.3.4'
          mode: 'block'
          notes: 'Example IP Block'

    - name: Creating CF Access Rule (Target Country)
      ngenen.cloudflare_secops.access_rule:
        email: '{{ email }}'
        token: '{{ token }}'
        state: present
        params:
          target: 'country'
          value: 'US'
          mode: 'challenge'
          notes: 'Example - Challenge US Country'
          
    - name: Updating mode/notes CF Access Rule (Search By Target and Value)
      ngenen.cloudflare_secops.access_rule:
        email: '{{ email }}'
        token: '{{ token }}'
        state: update
        params:
          target: 'ip'
          value: '1.2.3.4'
          mode: 'challenge'
          notes: 'Updated to challenge'

    - name: Deleting CF Access Rule (Search By Target and Value) - IP
      ngenen.cloudflare_secops.access_rule:
        email: '{{ email }}'
        token: '{{ token }}'
        state: absent
        params:
          target: 'ip'
          value: '1.2.3.4'

    - name: Deleting CF Access Rule (Search By Target and Value) - Country
      ngenen.cloudflare_secops.access_rule:
        email: '{{ email }}'
        token: '{{ token }}'
        state: absent
        params:
          target: 'country'
          value: 'US'
```

### Required Python libraries

CloudFlare SecOps collection depends on Python 3.8+ and on following third party libraries:

* [`cloudflare`](https://github.com/cloudflare/python-cloudflare)

### Installing required libraries and SDK

Installing collection does not install any required third party Python libraries or SDKs. You need to install the required Python libraries using following command:

    pip install -r ~/.ansible/collections/ansible_collections/ngenen/cloudflare_secops/requirements.txt

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Tests and Documentation are welcome.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)