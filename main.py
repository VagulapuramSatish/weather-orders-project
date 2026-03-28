import asyncio
import aiohttp
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Fetch weather for a city
async def fetch_weather(session, city):
    try:
        url = f"{BASE_URL}?q={city}&appid={API_KEY}"
        async with session.get(url) as response:
            data = await response.json()

            if response.status != 200:
                #print(f"City: {order['city']}, Weather: {weather}")
                print(f"Error fetching {city}: {data.get('message')}")
                return None

            return data["weather"][0]["main"]

    except Exception as e:
        print(f"Exception for {city}: {e}")
        return None


# AI-style apology generator
#def generate_apology(customer, city, weather):
    #return f"Hi {customer}, your order to {city} is delayed due to {weather.lower()}. We appreciate your patience!"

async def generate_apology_ai(customer, city, weather):
    try:
        prompt = f"""
        Write a polite and friendly delivery delay message.
        Customer: {customer}
        City: {city}
        Reason: {weather}

        Keep it short and human.
        """

        response = client.chat.completions.create(

            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"AI Error: {e}")
        return f"Hi {customer}, your order is delayed due to {weather}."


# Main processing function
async def process_orders():
    with open("orders.json", "r") as file:
        orders = json.load(file)

    async with aiohttp.ClientSession() as session:

        tasks = []
        for order in orders:
            city = order["city"]
            tasks.append(fetch_weather(session, city))

        results = await asyncio.gather(*tasks)

        for i, weather in enumerate(results):
            order = orders[i]

            if weather in ["Rain", "Snow", "Extreme"]:
            #if weather:
                order["status"] = "Delayed"
                #message = generate_apology(order["customer"], order["city"], weather)
                message = await generate_apology_ai(
                            order["customer"],
                            order["city"],
                            weather
                            )
                print(message)

    with open("orders.json", "w") as file:
        json.dump(orders, file, indent=2)


# Run program
asyncio.run(process_orders())