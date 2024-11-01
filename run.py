from package.app import app


if __name__ == '__main__':
    # app.run_server(debug = True, dev_tools_ui = True, use_reloader = True, port=8060)

    from waitress import serve
    serve(app.server, host="0.0.0.0", port=8080)

