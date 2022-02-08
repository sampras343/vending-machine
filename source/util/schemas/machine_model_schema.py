
PAGINATION = {
    "name": "Pagination",
    "properties": {
        "number": {
            "type": "number",
            "default": 1
        },
        "size": {
            "type": "number",
            "default": 0
        },
        "total-elements": {
            "type": "number",
            "default": 0
        },
        "total-pages": {
            "type": "number",
            "default": 1
        }
    },
    "additionalProperties": False,
}


POST_REQ_MODEL = {
    "name": "Validate POST Req Model",
    "required": ["racks", "name", "quantity"],
    "properties": {
        "racks": {
            "type": "object",
            "properties": {
                "max-racks": {
                    "type": "number"
                },
                "max-products-per-rack": {
                    "type": "number"
                }
            }
        },
        "name": {
            "type": "string",
            "minLength": 3
        },
        "quantity": {
            "type": "number"
        }
    }
}

CREATE_MODEL = {
    "name": "Register Model",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 3
        },
        "racks": {
            "type": "object",
            "properties": {
                "max-racks": {
                    "type": "number",
                    "default": 0
                },
                "max-products-per-rack": {
                    "type": "number",
                    "default": 0
                }
            }
        }
    }
}


CREATE_QUANTITY_MODEL = {
    "name": "Quantity Model",
    "properties": {
        "total": {
            "type": "number",
                    "default": 0
        },
        "active": {
            "type": "number",
                    "default": 0
        },
        "inactive": {
            "type": "number",
                    "default": 0
        },
        "damaged": {
            "type": "number",
                    "default": 0
        },
        "archived": {
            "type": "number",
                    "default": 0
        }
    }

}
