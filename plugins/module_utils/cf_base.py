
import traceback

try:
    import CloudFlare
except ImportError:
    HAS_CLOUDFLARE_LIBRARY = False
    CLOUDFLARE_LIBRARY_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_CLOUDFLARE_LIBRARY = True
    CLOUDFLARE_LIBRARY_IMPORT_ERROR = None

from ansible.module_utils.basic import missing_required_lib


class CFBase:
    def __init__(self, module):
        # We evaluate if we have the required library to function.
        if not HAS_CLOUDFLARE_LIBRARY:
            module.fail_json(
                msg=missing_required_lib('CloudFlare'),
                exception=CLOUDFLARE_LIBRARY_IMPORT_ERROR)

        # We initialize variables
        self.module = module
        self.params = module.params
        self.action_params = self.params['params']
        self.user = module.params['email']
        self.key = module.params['token']
        self.account_id = None
        self.api = CloudFlare.CloudFlare(email=self.user, key=self.key)

    def initialize(self):
        if not self.validate_credentials():
            raise Exception('Please check your Cloudflare credentials.')

    def validate_credentials(self):
        try:
            self.account_id = self.api.accounts()[0]['id']
            return True
        except CloudFlare.exceptions.CloudFlareAPIError:
            return False
