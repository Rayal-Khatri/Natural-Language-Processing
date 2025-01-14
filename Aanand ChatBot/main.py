from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
# from fastapi.middleware.cors import CORSMiddleware
import db_helper
import logging
import Generic_helper

app = FastAPI()

inprogress_orders ={}

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust this to specify allowed origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.post("/")
async def handle_request(request: Request):
    intent_handler_dict = {
        'order.add - context: ongoing-order': add_to_order,
        'order.remove - context: Ongoing-order': remove_from_order,
        'order-complete - context: Ongoing order': complete_order,
        'track-order - context: ongoing-tracking': track_order
        }
    try:
        # Retrieve the JSON data from the request
        payload = await request.json()

        # Extract the necessary information from the payload
        intent = payload['queryResult']['intent']['displayName']
        parameters = payload['queryResult']['parameters']
        output_contexts = payload['queryResult']['outputContexts']
        session_id = Generic_helper.extract_session_id(output_contexts[0]['name'])

        # Log the parameters for debugging
        logging.info(f"Parameters received: {parameters}")

        return intent_handler_dict[intent](parameters, session_id)
        
    except KeyError as e:
        return JSONResponse(content={
            "fulfillmentText": f"Missing key in request payload: {e}"
        })
    except Exception as e:
        return JSONResponse(content={
            "fulfillmentText": f"An error occurred: {e}"
        })




def track_order(parameters: dict, session_id: str):
    order_id = parameters.get('number')
    if not order_id:
        return JSONResponse(content={
            "fulfillmentText": "Order ID is missing in the parameters"
        })

    status = db_helper.get_order_status(order_id)
    if status:
        return JSONResponse(content={
            "fulfillmentText": f"Your order status is: {status}"
        })
    else:
        return JSONResponse(content={
            "fulfillmentText": "Order not found"
        })
    
def add_to_order(parameters: dict, session_id: str):
    food_item = parameters["food-item"]
    quantity = parameters["number"]

    if len(food_item) != len(quantity):
        fulfillment_text = "Kindly mention the amount of food you'd like. For instance: I'll have two samosas."
    else:
        new_food_dict = dict(zip(food_item, quantity))

        if session_id in inprogress_orders:
            inprogress_orders[session_id].update(new_food_dict)
        else:
            inprogress_orders[session_id] = new_food_dict
        order_str = Generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have {order_str} in your order. Any changes you'd like to make?"
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



def remove_from_order(parameters: dict, session_id: str):
    food_item = parameters["food-item"]
    if session_id in inprogress_orders:
        for item in food_item:
            if item in inprogress_orders[session_id]:
                del inprogress_orders[session_id][item]
                order_str = Generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
                fulfillment_text = f"Removed sucessfully. So far you have {order_str} in your order. Any changes you'd like to make?"
            else:
                order_str = Generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
                fulfillment_text = f"{item} is not in your order. So far you have {order_str} in your order. Any changes you'd like to make?"

    else:
        fulfillment_text = "Please place an order to remove items from it."
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def complete_order(parameters: dict, session_id: str):
    if session_id in inprogress_orders:
        order = inprogress_orders[session_id]
        order_id = db_helper.save_to_db(order)

        if order_id == -1: 
            fulfillment_text = "An error occurred while saving the order. Please try again."
        else:
            order_total = db_helper.get_total_price(order_id)
            fulfillment_text = f"Your order has been placed with a total of Rs. {order_total}. Your order ID is {order_id}."
            del inprogress_orders[session_id]
    else:
        fulfillment_text = "Please place an order before completing it."
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

if __name__ == "__main__":
    config = uvicorn.Config("main:app", host = "0.0.0.0", port=8000, reload=True)
    server = uvicorn.Server(config)
    server.run()