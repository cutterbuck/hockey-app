from package.app import app


if __name__ == '__main__':
    # app.run_server(debug = True, dev_tools_ui = True, use_reloader = True, port=8060)
    app.server.run()

