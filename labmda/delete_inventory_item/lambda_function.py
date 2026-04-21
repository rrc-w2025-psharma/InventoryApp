import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Inventory")


def lambda_handler(event, context):
    try:
        item_id = event["pathParameters"]["id"]

        scan_response = table.scan(
            FilterExpression="item_id = :item_id",
            ExpressionAttributeValues={":item_id": item_id}
        )

        items = scan_response.get("Items", [])

        if not items:
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"message": "Item not found"})
            }

        item = items[0]

        table.delete_item(
            Key={
                "item_id": item["item_id"],
                "location_id": item["location_id"]
            }
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "Item deleted successfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }