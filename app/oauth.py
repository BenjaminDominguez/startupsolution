from app import app
from flask import url_for
from rauth import OAuth2Service

class OAuthSignIn(object):
    """
    this is going to be a dictionary defined later
    """
    providers = None

    def __init__(self, provider_name):
        """
        initializing provider name
        grabbing credentials (notice we don't initialize it),
        so that we can set the consumer id tag and consumer_secret
        from that app.config object OAUTH_CREDENTIALS
        We then grab 'id' and 'secret' and initialize to our class
        """
        self.provider_name = provider_name
        credentials = app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    """
    callback and authorize are under OAuthSignIn class
    because the authorize portion of Oauth (initiation of the authorization process)
    callback (initiation of the callback protion)

    """
    def authorize(self):
        pass

    def callback(self):
        pass
    """
    this is the url that the provider will callback to after
    authentication is complete
    """
    def callback_url(self):
        """

        this will not raise an exception because it is not being run
        here (It wouldve because our route is in our routes module)
        """
        return url_for('oath_callback', provider=self.provider_name, _external=True)


    @classmethod
    def get_provider(self, provider_name):
        """
        if no providers, (it is at the top)
        [note, if this is not none, we simply return the provider name we are asking for]
        [we do this by finding the provider name within the provider dict]
        create a providers dict to store to the class
        for each provider_class (LinkedIn and GitHub) in our sublclasses (classes that inherited from us)
        create an instance of that class, "provider".
        So if there is no provider dict, we are creating it from every class that inherits from us
        we are setting the key equal to the provider name and setting that to the instance of the provider
        for instance,
        providers =
            {
            'linkedin.com': LinkedIn, (an instance of this class)
            'github.com': Github
            }
        """
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]

class LinkedInSignIn(OAuthSignIn):
    # allow inheritance
    super(LinkedInSignIn, self).__init__('linkedin')
    self.service = OAuth2Service(
    name='LinkedIn',
    client_id = self.consumer_id,
    client_secret = self.consumer_secret,
    authorize_url = 'string',
    access_token_url='string',
    base_url='string'
    )

class GitHubSignIn(OAuthSignIn):
    pass
