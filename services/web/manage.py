from flask.cli import FlaskGroup

from src import app, engine
from src.database.models import Base
from src.utils import drop_everything
from src.views.events import events

app.register_blueprint(events)
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    drop_everything(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    cli()
