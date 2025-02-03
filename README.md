# Aanand Chat Bot 🤖  

Aanand Chat Bot is a simple yet functional chatbot built using **Dialogflow**, designed to assist users in:  
- 🛒 **Placing new orders**  
- 💰 **Inquiring about prices**  
- 📦 **Tracking existing orders**  
- ❌ **Removing items from orders**  

## Tech Stack ⚙️  
- **Frontend**: Website hosted on [Vercel](https://natural-language-processing-iota.vercel.app)  
- **Backend**: FastAPI for handling communication between the website, server, and database  
- **Database**: **MySQL**, hosted on **Aiven**, storing all order-related information  
- **Server**: Running on **Render** ([View Here](https://dashboard.render.com/web/srv-cu32p323esus73db0rrg))  

## How It Works 🛠️  
1. Users interact with the chatbot on the website.  
2. Dialogflow processes user intents (e.g., new order, price inquiry, track order).  
3. FastAPI handles API requests between the website, server, and database.  
4. MySQL stores and retrieves order-related data.  

## Future Enhancements 🚀  
- Implement AI-based recommendation system  
- Improve natural language understanding  
