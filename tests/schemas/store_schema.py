STORE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "petId": {
            "type": "integer"
        },
        "quantity": {
            "type": "integer"
        },
        "status": {
            "type": "string",
            "enum": ["approved", "placed"]
        },
        "complete": {
            "type": "boolean"
        }

    },
    "required": ["id", "petId", "quantity", "status", "complete"]
}

INVENTORY_STORE_SCHEMA = {
    "type": "object",
    "properties": {
        "approved": {
            "type": "integer"
        },
        "delivered": {
            "type": "integer"
        }
    }
}
