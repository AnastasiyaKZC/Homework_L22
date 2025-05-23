ERROR_LOGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "data": {"type": "null"},
        "error": {
            "type": "object",
            "properties": {
                "status": {"type": "number", "const": 400},
                "name": {"type": "string", "const": "ValidationError"},
                "message": {"type": "string"},
                "details": {
                    "type": "object",
                    "properties": {
                        "errors": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "array", "items": {"type": "string"}},
                                    "message": {"type": "string"},
                                    "name": {"type": "string"},
                                },
                                "required": ["path", "message", "name"],
                            },
                        },
                    },
                    "required": ["errors"],
                },
            },
            "required": ["status", "name", "message", "details"],
        },
    },
    "required": ["data", "error"],
}

SUCCESS_LOGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "jwt": {"type": "string"},
        "user": {
            "type": "object",
            "properties": {
                "id": {"type": "number"},
                "email": {"type": "string"},
                "confirmed": {"type": "boolean"},
                "blocked": {"type": "boolean"},
                "userRole": {"type": "string"},
                "resourceMap": {"type": ["object", "null"]}
            },
            "required": ["id", "email"]
        }
    },
    "required": ["jwt", "user"]
}