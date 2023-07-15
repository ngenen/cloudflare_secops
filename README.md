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

- Access Rules (Account, Zone, User)

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