import json
import boto3
import uuid
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            if obj % 1 == 0:
                return int(obj)
            return float(obj)
        return super().default(obj)


def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])

        item = {
            "item_id": str(uuid.uuid4()),
            "location_id": int(body["location_id"]),
            "item_name": body["item_name"],
            "item_description": body["item_description"],
            "item_qty_on_hand": int(body["item_qty_on_hand"]),
            "item_price": Decimal(str(body["item_price"]))
        }

        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Item created successfully",
                "item": item
            }, cls=DecimalEncoder)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }