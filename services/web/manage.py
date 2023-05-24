from flask.cli import FlaskGroup

from src import app, engine, db_adapter
from src.database.models import Base
from src.utils import drop_everything
from src.views.events import events_api

app.register_blueprint(events_api)
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    drop_everything(engine)
    Base.metadata.create_all(engine)
    db_adapter.create_default_data()


if __name__ == "__main__":
    cli()
