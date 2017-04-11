import functools
import hashlib
import hmac

from tornado import escape
from tornado.auth import OAuth2Mixin, AuthError
from tornado.concurrent import chain_future


class FacebookGraphMixin(OAuth2Mixin):
    """Facebook authentication using the new Graph API and OAuth2."""
    _OAUTH_ACCESS_TOKEN_URL = "https://graph.facebook.com/oauth/access_token?"
    _OAUTH_AUTHORIZE_URL = "https://www.facebook.com/dialog/oauth?"
    _OAUTH_NO_CALLBACKS = False
    _FACEBOOK_BASE_URL = "https://graph.facebook.com"

    def get_authenticated_user(self, redirect_uri, client_id, client_secret,
                               code, callback, extra_fields=None):
        """Handles the login for the Facebook user, returning a user object.

        Example usage:

        .. testcode::

            class FacebookGraphLoginHandler(tornado.web.RequestHandler,
                                            tornado.auth.FacebookGraphMixin):
              @tornado.gen.coroutine
              def get(self):
                  if self.get_argument("code", False):
                      user = yield self.get_authenticated_user(
                          redirect_uri='/auth/facebookgraph/',
                          client_id=self.settings["facebook_api_key"],
                          client_secret=self.settings["facebook_secret"],
                          code=self.get_argument("code"))
                      # Save the user with e.g. set_secure_cookie
                  else:
                      yield self.authorize_redirect(
                          redirect_uri='/auth/facebookgraph/',
                          client_id=self.settings["facebook_api_key"],
                          extra_params={"scope": "read_stream,offline_access"})

        .. testoutput::
           :hide:

        """
        http = self.get_auth_http_client()
        args = {
            "redirect_uri": redirect_uri,
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        fields = set(['id', 'name', 'first_name', 'last_name',
                      'locale', 'picture', 'link'])
        if extra_fields:
            fields.update(extra_fields)

        http.fetch(self._oauth_request_token_url(**args),
                   functools.partial(self._on_access_token, redirect_uri, client_id,
                                     client_secret, callback, fields))

    def _on_access_token(self, redirect_uri, client_id, client_secret,
                         future, fields, response):
        if response.error:
            future.set_exception(
                AuthError('Facebook auth error: %s' % str(response)))
            return

        args = escape.json_decode(response.body)
        session = {
            "access_token": args.get("access_token"),
            "expires": args.get("expires")
        }

        self.facebook_request(
            path="/me",
            callback=functools.partial(
                self._on_get_user_info, future, session, fields),
            access_token=session["access_token"],
            appsecret_proof=hmac.new(key=client_secret.encode('utf8'),
                                     msg=session["access_token"].encode(
                                         'utf8'),
                                     digestmod=hashlib.sha256).hexdigest(),
            fields=",".join(fields)
        )

    def _on_get_user_info(self, future, session, fields, user):
        if user is None:
            future.set_result(None)
            return

        fieldmap = {}
        for field in fields:
            fieldmap[field] = user.get(field)

        fieldmap.update(
            {"access_token": session["access_token"], "session_expires": session.get("expires")})
        future.set_result(fieldmap)

    def facebook_request(self, path, callback, access_token=None,
                         post_args=None, **args):
        """Fetches the given relative API path, e.g., "/btaylor/picture"

        If the request is a POST, ``post_args`` should be provided. Query
        string arguments should be given as keyword arguments.

        An introduction to the Facebook Graph API can be found at
        http://developers.facebook.com/docs/api

        Many methods require an OAuth access token which you can
        obtain through `~OAuth2Mixin.authorize_redirect` and
        `get_authenticated_user`. The user returned through that
        process includes an ``access_token`` attribute that can be
        used to make authenticated requests via this method.

        Example usage:

        ..testcode::

            class MainHandler(tornado.web.RequestHandler,
                              tornado.auth.FacebookGraphMixin):
                @tornado.web.authenticated
                @tornado.gen.coroutine
                def get(self):
                    new_entry = yield self.facebook_request(
                        "/me/feed",
                        post_args={"message": "I am posting from my Tornado application!"},
                        access_token=self.current_user["access_token"])

                    if not new_entry:
                        # Call failed; perhaps missing permission?
                        yield self.authorize_redirect()
                        return
                    self.finish("Posted a message!")

        .. testoutput::
           :hide:

        The given path is relative to ``self._FACEBOOK_BASE_URL``,
        by default "https://graph.facebook.com".

        This method is a wrapper around `OAuth2Mixin.oauth2_request`;
        the only difference is that this method takes a relative path,
        while ``oauth2_request`` takes a complete url.

        .. versionchanged:: 3.1
           Added the ability to override ``self._FACEBOOK_BASE_URL``.
        """
        url = self._FACEBOOK_BASE_URL + path
        # Thanks to the _auth_return_future decorator, our "callback"
        # argument is a Future, which we cannot pass as a callback to
        # oauth2_request. Instead, have oauth2_request return a
        # future and chain them together.
        oauth_future = self.oauth2_request(url, access_token=access_token,
                                           post_args=post_args, **args)
        chain_future(oauth_future, callback)
