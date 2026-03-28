## Weather Orders Project :
Python script that checks weather for each order’s city and flags potential delivery delays using aiohttp and python-dotenv.

***Features***
- Fetches weather concurrently for multiple cities
- Flags orders as Delayed if Rain, Snow, or Extreme
- Generates personalized weather-aware apology messages
- Handles invalid cities gracefully
- Uses .env for API keys (no hardcoding)

***Setup*** : 

Clone repo and install dependencies:
- git clone https://github.com/your-username/weather-orders-project.git
- cd weather-orders-project
- pip install -r requirements.txt

-- Create .env with your API keys:
- OPENWEATHER_API_KEY=your_key
- OPENAPI_TOKEN=your_key

***Usage***: 
 Ensure orders.json is in the project root
- Run the script: python main.py
- The script will:
- Fetch weather for all cities concurrently
- Update status to Delayed for Rain, Snow, or Extreme
- Generate personalized apology messages
- Log errors for invalid cities

***Mission & Logic***
- Fetch weather concurrently using asyncio.gather
- If main weather is Rain, Snow, or Extreme, set order status to Delayed
   Generate personalized messages like: Hi Alice, your order to New York is delayed due to heavy rain. We appreciate your patience!

***Error Handling***
- Invalid cities are logged but do not stop execution
- Example: Error: City 'InvalidCity123' not found. Skipping order 1004.

