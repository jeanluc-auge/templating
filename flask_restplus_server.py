from flask import Flask, request  # , redirect, render_temple
from flask_restplus import Resource, Api, reqparse, fields
from macros import LcdnContentdClient, LcdnSecretClient

# ******* define Flask api *******
app = Flask(__name__)
api = Api(app)

# ********* contentd api *************
contentd = api.namespace(
    "contentd", description="macros for Akamai LCDN contentd"
)
contentd_client = LcdnContentdClient()

# ********* secret api *************
secret = api.namespace(
    "secret", description="macros for Akamai LCDN secret"
)
secret_client = LcdnSecretClient()

# ********** endpoints declaration ****************
@contentd.route('/provider/<string:account>')
class Provider_account(Resource):
    @api.doc(
        description=contentd_client.get_content_provider.__doc__
    )
    def get(self, account):
        base_path = request.args.get('base_path')
        response = contentd_client.get_content_provider(
             account=account, base_path=base_path,
        )
        status_code = 200 if response else 400
        return (
            response, status_code
        )

    @api.doc(
        description=contentd_client.post_content_provider.__doc__
    )
    def post(self, account):
        base_path = request.args.get('base_path')
        response = contentd_client.get_content_provider(
             account=account, base_path=base_path,
        )
        status_code = 200 if response else 400
        return (
            response, status_code
        )

# TODO exercise for you:
# manually create endpoint for macros post_content_provider & get_secret


if __name__ == "__main__":
    # ***** start app server *******
    app.run(debug=True, host="0.0.0.0", port=9999)    