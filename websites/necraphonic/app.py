from necraphonic_app import create_app

app = create_app()

if __name__ == '__main__':
    # Debug=True is only for development!
    app.run(debug=True)