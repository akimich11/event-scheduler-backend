from src.views import app
# from src.views.auth import auth
from src.views.plans import plans

# app.register_blueprint(auth)
app.register_blueprint(plans)


@app.route('/')
def root():
    return f'This is the API root'


if __name__ == '__main__':
    app.run()
