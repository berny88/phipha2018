import flask
import os
import sys
import logging
import logging.handlers
from pymongo import MongoClient
import sendgrid
from sendgrid.helpers.mail import *

print("start app.py")
print(__name__)

application = flask.Flask(__name__)
application.secret_key = u'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT#BB'

from tools.Tools import ToolManager, tools_page
from users.UserServices import users_page
from bets.BetsServices import bets_page
from matchs.MatchServices import matchs_page
from communities.CommunityServices import communities_page
from chat.ChatServices import chat_page
from stats.StatsServices import stats_page
 

application.register_blueprint(communities_page, url_prefix="/communities", template_folder='templates')
application.register_blueprint(users_page, url_prefix="/users", template_folder='templates')
application.register_blueprint(bets_page, url_prefix="/bets", template_folder='templates')
application.register_blueprint(stats_page, url_prefix="/stats", template_folder='templates')
application.register_blueprint(matchs_page, url_prefix="/matchs", template_folder='templates')
application.register_blueprint(tools_page, url_prefix="/tools", template_folder='templates')
application.register_blueprint(chat_page, url_prefix="/chat", template_folder='templates')

# Only enable Flask debugging if an env var is set to true
application.debug = os.environ.get('FLASK_DEBUG') in ['true', 'True']
print("Started...")

application.logger.info('Started')
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
logging.basicConfig(filename='betapp.log',level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(ch)


logger.info('Started')
logger.debug('test debug message')
logger.info('test info message')
logger.warn('test warn message')
logger.error('test error message')
logger.critical('test critical message ..')

# Get application version from env
app_version = os.environ.get('APP_VERSION')

# Get cool new feature flag from env
enable_cool_new_feature = os.environ.get('ENABLE_COOL_NEW_FEATURE') in ['true', 'True']

@application.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0, no-cache, no-store, must-revalidate'
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    #logger.info(u'response.headers={}'.format(response.headers))
    return response
@application.route('/')
def hello_world():
    return application.send_static_file('index.html')
    
@application.route('/testmongo/')
def testmongo():
    client = MongoClient("mongodb+srv://phipha:phiphaxxxviii@phiphaxxxviii-cs6ex.mongodb.net/phipha?retryWrites=true", ssl=True)
    db = client.first
    logger.info(u'test mongo : db={}'.format(db))
    tool = ToolManager()
    db = tool.getDb()
    logger.info(u'test mongo : db={}'.format(db))
    tmp = tool.getProperty(u"test")
    logger.info(u'test mongo : tmp={}'.format(tmp))
    tool.saveProperty(u"test", "firstProperties")
    props = tool.getProperties()
    logger.info(u'test mongo : {}'.format(props))

    return u"Test Mongo", 200

@application.route('/testmail/')
def testmail():
    tool = ToolManager()
    sg = tool.get_sendgrid()

    api_key=tool.getProperty('SENDGRID_API_KEY')["value"]
    logger.info("sendgrid={}".format(api_key))
    sg = sendgrid.SendGridAPIClient(apikey=api_key)
    from_email = Email("eurommxvi.foot@gmail.com")
    to_email = Email("eurommxvi.foot@gmail.com")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/html", "and <b>easy</h> to do anywhere, even with <h1>Python</h1>")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

    return u"look at your email box : result="+str(response.status_code)+" - "+str(response.body), 200

@application.errorhandler(404)
def ma_page_404(error):
    return u"Page not found !<br/> <h1>404 error code !</h1> Where do you really want to go ?", 404
    
 
if __name__ == '__main__':
    print("main app.py application.run")
    print(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
    application.run(host='0.0.0.0', port=os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
