import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key

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
        location_id = int(event["pathParameters"]["id"])

        response = table.query(
            IndexName="location_id-item_id-index",
            KeyConditionExpression=Key("location_id").eq(location_id)
        )

        items = response.get("Items", [])

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(items, cls=DecimalEncoder)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }