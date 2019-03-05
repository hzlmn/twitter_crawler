def setup_routes(app, handler):
    app.router.add_get("/search_settings",
                       handler.get_settings, name="get_settings")

    app.router.add_post("/search_settings",
                        handler.create_settings, name="create_settings")

    app.router.add_get("/search_results",
                       handler.get_results, name="get_results")

    return app
