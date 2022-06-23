"""
filename: api.py
last-updated: *in development
authors: Josh Schmitz

description:
    API for interracting with controller. This api acts as in intermediary
        API between the front-end and the trinsic api (accessed via controller).
    It is necessary to have this intermediary api for authentication purposes
        as we may want to seperate privileges and we do not want the trinsic api
        key to be put in the front-end.

TODO
    * input validation / error catching
    * logging
    * qr codes?
    * make controller global scope?
    * authentication
    * better documentation for endpoint inputs (ie url, params, json form, etc)
    * documentation for return objects
    * endpoint for searching for records based on names, ids, tags, etc
"""

from flask import Flask, render_template, request, redirect
import utils
from controller import Controller

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    # TODO delete this or add meta information for interacting with api?
    return render_template('form.html')


@app.route("/", methods=["POST"])
def form_post():
    # get the data from the user
    
    data = {}
    data['name'] = request.form.get('name')
    data['email'] = request.form.get('email')
    print(data)

    # create the credential
    alphaledger = Controller('alphaledger', utils.get_api_key('alphaledger'))
    login_cred = alphaledger.create_credential(
        alphaledger.get_cred_def('BbRYr1N4QJLM8nacfxsVM4:3:CL:328263:Default'), 
        {"Name":data['name'], "Email":data['email']}
        )
    utils.generate_qr_code(login_cred.offer_url)
    
    return redirect("/create-account")


@app.route("/create-account")
def issue_login_credential():
    return render_template("create-account.html")

@app.route("/login")
def login_verification():
    return render_template('login.html')



@app.route("/records/connections")
def view_connections():
    """
    Returns list of connections.
    
    http://127.0.0.1:5000/records/connections?org_name=<name>
    """
    org_name = request.args.get("org_name")
    controller = Controller(organization_name=org_name, api_key=utilities.get_api_key(org_name))
    conns = controller.get_connections(state=None)
    return_obj = {"connections": [conn.as_dict() for conn in conns]}
    return return_obj

@app.route("/records/credential_definitions")
def view_credential_definitions():
    """
    Returns list of credential definitions.
    
    http://127.0.0.1:5000/records/credential_definitions?org_name=<name>
    """
    org_name = request.args.get("org_name")
    controller = Controller(organization_name=org_name, api_key=utilities.get_api_key(org_name))
    cred_defs = controller.get_credential_definitions()
    return_obj = {"credential_definitions": [cred_def.as_dict() for cred_def in cred_defs]}
    return return_obj
    
@app.route("/records/verification_policies")
def view_verification_policies():
    """
    Returns list of verification policies.
    
    http://127.0.0.1:5000/records/verification_policies?org_name=<name>
    """
    org_name = request.args.get("org_name")
    controller = Controller(organization_name=org_name, api_key=utilities.get_api_key(org_name))
    ver_pols = controller.get_verification_policies()
    return_obj = {"verification_policies": [ver_pol.as_dict() for ver_pol in ver_pols]}
    return return_obj

@app.route("/create/credential_definition", methods=["POST"])
def create_credential_definition():
    """
    Create/publish a credential definition.
    
    http://127.0.0.1:5000/create/credential_definition?org_name=<name>
        * json form:
            {
                "schema_name": <name>,
                "version": <version>,
                "attributes": [<attributes>],
                "tag": <tag>
            }
    """
    org_name = request.args.get("org_name")
    json = request.get_json()
    schema_name = json["schema_name"]
    version = json["version"]
    attributes = json["attributes"]
    support_revocation = False # TODO
    tag = json["tag"]
    controller = Controller(organization_name=org_name, api_key=utilities.get_api_key(org_name))
    return_obj = controller.publish_credential_definition(
        name=schema_name,
        version=version,
        attributes=attributes,
        support_revocation=support_revocation,
        tag=tag
    )
    return return_obj.as_dict()

@app.route("/create/verification_policy")
def create_verification_policy():
    """
    Creates a verification policy.
    
    http://127.0.0.1:5000/create/verification_policy?org_name=<name>
        * json form:
            {
                "policy_name": <name>,
                "version": <version>,
                "attributes": [<attributes>]
            }
    """
    org_name = request.args["org_name"]
    json = request.get_json()
    policy_name = json["policy_name"]
    version = json["version"]
    attributes = json["attributes"]
    predicates = None # TODO
    revocation_requirement = None # TODO
    controller = Controller(organization_name=org_name, api_key=utilities.get_api_key(org_name))
    return_obj = controller.create_verification_policy(
        name=policy_name,
        version=version,
        attributes=attributes,
        predicates=predicates,
        revocation_requirement=revocation_requirement
    )
    return return_obj.as_dict()

@app.route("/create/connection", methods=["POST"])
def create_connection():
    """
    Create a connection invitation.
    
    http://127.0.0.1:5000/create/connection?org_name=<name>
        * json form:
            {
                "connection_name": <name>
            }
    """
    org_name = request.args.get("org_name")
    json = request.get_json()
    connection_name = json["connection_name"]
    connection_id = None # TODO
    multi_party = False # TODO
    controller = Controller(organization_name=org_name, api_key=utilities.get_api_key(org_name))
    return_obj = controller.create_connection(
        name=connection_name,
        connection_id=connection_id,
        multi_party=multi_party
    )
    return return_obj.as_dict()

@app.route("/issue_credential", methods=["POST"])
def issue_credential():
    """
    Issue a credential.
    
    http://127.0.0.1:5000/issue_credential?org_name=<name>
        * json form:
            {
                "cred_def_id": <name>,
                "credential_values": {<attribute>: <value>}
            }
    """
    org_name = request.args.get("org_name")
    json = request.get_json()
    connection_id = None # TODO
    definition_id = json["cred_def_id"]
    credential_values = json["credential_values"]
    automatic_issuance = False # TODO
    controller = Controller(organization_name=org_name, api_key=utilities.get_api_key(org_name))
    return_obj = controller.create_credential(
        definition_id=definition_id,
        connection_id=connection_id,
        credential_values=credential_values,
        automatic_issuance=automatic_issuance
    )
    return return_obj.as_dict()

@app.route("/request_verification", methods=["POST"])
def request_verification():
    """
    Send a credential verification request to the given connection.
    
    http://127.0.0.1:5000/request_verification?org_name=<name>
        * json form:
            {
                "connection_id": <connection_id>,
                "policy_id": <policy_id>
            }
    """
    org_name = request.args.get("org_name")
    json = request.get_json()
    connection_id = json["connection_id"]
    policy_id = json["policy_id"]
    controller = Controller(organization_name=org_name, api_key=utilities.get_api_key(org_name))
    return_obj = controller.send_verification_from_policy(
        connection_id=connection_id,
        policy_id=policy_id
    )
    return return_obj.as_dict()

@app.route("/verification")
def verification_status():
    """
    Get a given verification record by id. Used to determine if verification
        was succesful.
    
    http://127.0.0.1:5000/verification?org_name=<name>&verification_id=<id>
    """
    org_name = request.args.get("org_name")
    verification_id = request.args.get("verification_id")
    controller = Controller(organization_name=org_name, api_key=utilities.get_api_key(org_name))
    return_obj = controller.get_verification(verification_id=verification_id)
    return return_obj.as_dict()

if __name__ == "__main__":
    app.run()