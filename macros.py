

# ******** macros definition *******
class LcdnContentdClient:

    def get_content_provider(self, account, base_path):
        """return the content provider ID by querying its account
        Args:
            account (str): content provider account

        """
        return {
            'account': account,
            'base_path': base_path,
        }

    def post_content_provider(self, account, base_path):
        """post the content provider ID by querying its account
        Args:
            account (str): content provider account

        """
        return {
            "posted account": account,
            "base_path": base_path,
        }

class LcdnSecretClient:

    def get_secret(self, secret_id):
        """
        Args:
            secret_id (int):
        Returns:
            AMCSecret:

        """ 
        return {secret_id: 'top-secret'}