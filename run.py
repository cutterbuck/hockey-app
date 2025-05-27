from package.app import app
from package.schedules import start_running_schedules
from waitress import serve



if __name__ == '__main__':
    with app.server.app_context():
        start_running_schedules()

    # app.run_server(debug = True, dev_tools_ui = True, use_reloader = True, port=8060)
    serve(app.server, host="0.0.0.0", port=8080)