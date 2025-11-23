from begin.xtensions import *

##
def register_app(app:object)->None:

    @app.route('/view/activity')
    def view_activity()->object:
        return flask.render_template('activity.html')
