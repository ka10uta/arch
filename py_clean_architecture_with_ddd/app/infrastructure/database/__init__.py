tortoise_config = {
    "connections": {
        "default": "sqlite://data/db.sqlite3",
    },
    "apps": {
        "models": {
            "models": ["app.infrastructure.database.model", "aerich.models"],
            "default_connection": "default",
        },
    },
}
