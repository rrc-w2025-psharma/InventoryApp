import json
import boto3
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
        item_id = event["pathParameters"]["id"]

        response = table.scan(
            FilterExpression="item_id = :item_id",
            ExpressionAttributeValues={":item_id": item_id}
        )

        items = response.get("Items", [])

        if not items:
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"message": "Item not found"})
            }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(items[0], cls=DecimalEncoder)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }