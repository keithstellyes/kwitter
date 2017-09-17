def run_app(app, settings):
    app.run(host=settings.host,
            port=settings.port)