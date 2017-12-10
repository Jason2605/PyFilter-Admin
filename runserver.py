from pyfilter_admin import app, settings

if __name__ == "__main__":
    app.run("0.0.0.0", debug=settings["debug"], threaded=True)
