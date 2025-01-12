from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from db_helper import get_order_status
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.post("/")
async def handle_request(request: Request):
    try:
        # Retrieve the JSON data from the request
        payload = await request.json()

        # Extract the necessary information from the payload
        intent = payload['queryResult']['intent']['displayName']
        parameters = payload['queryResult']['parameters']
        output_contexts = payload['queryResult']['outputContexts']

        # Log the parameters for debugging
        logging.info(f"Parameters received: {parameters}")

        if intent == "track-order - context: ongoing-tracking":
            return await track_order(parameters)
        else:
            return JSONResponse(content={
                "fulfillmentText": "Received some other intent"
            })
    except KeyError as e:
        return JSONResponse(content={
            "fulfillmentText": f"Missing key in request payload: {e}"
        })
    except Exception as e:
        return JSONResponse(content={
            "fulfillmentText": f"An error occurred: {e}"
        })

async def track_order(parameters: dict):
    order_id = parameters.get('number')
    if not order_id:
        return JSONResponse(content={
            "fulfillmentText": "Order ID is missing in the parameters"
        })

    status = get_order_status(order_id)
    if status:
        return JSONResponse(content={
            "fulfillmentText": f"Your order status is: {status}"
        })
    else:
        return JSONResponse(content={
            "fulfillmentText": "Order not found"
        })