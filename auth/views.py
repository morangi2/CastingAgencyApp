import os
from flask import Blueprint, redirect, render_template, request, session, current_app, url_for
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode


# set up _authlib_ and register a new Aith0 OAuth provider

auth_bp = Blueprint('auth', __name__)

oauth = OAuth(current_app)


domain = os.environ['AUTH0_DOMAIN']
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET_KEY']
audience = os.environ['API_AUDIENCE']


oauth.register(
    "auth0",
    client_id = client_id,
    client_secret = client_secret,
    client_kwargs = {
        "scope": "openid profile email",
    },
    server_metadata_url = f'https://{domain}/.well-known/openid-configuration'
)

#now, the _authlib_ library (OAuth) is fully setup and we can start creating the views we need to handle auth with Auth0 auth server

# after the user attempts to log in, (successful or not), Auth0 redirects them to the /callback endpoint
# and the route will call the view that matches with it in the applic

# in the _callback_ view, we A) authenticate the user coming from the request
# B) store the user token in _session_
# C) redirect the user to a new endpoint... eg /profile

# respond with 400 status code incase of an error

@auth_bp.route('/callback', methods=['GET', 'POST'])
def callback():
    # Callback redirect from Auth0

    token = oauth.auth0.authorize_access_token()
    session['user'] = token

    # The app assumes for a /profile path to be available, change here if it's not
    return redirect('/')
    #return render_template('pages/home.html')



@auth_bp.route('/login')
def login():
    #redirects the user to the Auth0 Universal Login ==> (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    # after successful login, it will redirect to the /callback endpoint, completing the authentication process
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True),
        audience=audience
    )

@auth_bp.route('/signup')
def signup():
    # when user Clicks SignUp button, redirected to the signup page, not the login page
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for('auth.callback', _external=True),
        screen_hint = 'signup',
        audience=audience
    )

@auth_bp.route('/logout')
def logout():
    # LOGS OUT the user from the session and from the Auth0 tenant
    # diff from login and sign up as it DOES NOT depend on authlib
    # this method cleans the session to logout the user from the Flask app
    # and, p4ms a redirect to Auth0 to logout the user as well form that end

    session.clear()

    return redirect(
        "https://" 
        + domain 
        + "/v2/logout?" 
        + urlencode(
            {
                "returnTo": url_for("index", _external=True),
                "client_id": client_id,
            },
            quote_via=quote_plus
        )
    )


