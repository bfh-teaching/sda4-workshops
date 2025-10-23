# SDA4 Challenge 1: Weather-Driven Currency Converter
**Duration:** 30 minutes  
**Difficulty:** ⭐☆☆☆

## Learning Objectives
- Understand service integration patterns
- Work with REST APIs
- Transform data between services

## Scenario
You're building an agent that checks the weather in a city. If the temperature is above 20°C, it fetches current currency exchange rates (for vacation planning).

## APIs We'll Use (No Keys Needed!)
- **Weather:** Your Mock API (`[MOCK-API-URL]/weather/zurich`)
- **Currency:** Your Mock API (`[MOCK-API-URL]/currency/USD`)

## Step-by-Step Instructions

### Step 1: Access n8n (5 minutes)
1. Open your browser
2. Navigate to: `[YOUR-N8N-URL]`
3. Log in with your credentials (from Sunday email)
4. Click **"Create new workflow"**

### Step 2: Add Manual Trigger (2 minutes)
1. Click the **"+"** button in the workflow canvas
2. Search for **"Manual Trigger"**
3. Click to add it
4. This is your starting point

### Step 3: Add Weather API Request (8 minutes)
1. Click **"+"** after the Manual Trigger node
2. Search for **"HTTP Request"**
3. Configure the node:
   - **Method:** GET
   - **URL:** `[MOCK-API-URL]/weather/zurich`
   - **No authentication needed!**
4. Click **"Execute Node"** to test
5. Verify you see weather data in the output

**Expected Output:**
```json
{
  "city": "zurich",
  "temperature": 22,
  "condition": "sunny",
  "humidity": 65,
  "timestamp": "2025-10-22T10:30:00"
}
```

### Step 4: Extract Temperature (5 minutes)
1. Add a **"Code"** node
2. Paste this code:
```javascript
const temp = $input.item.json.temperature;
const city = $input.item.json.city;

return {
  temperature: temp,
  location: city
};
```
3. Execute and verify output shows just temperature and location

### Step 5: Add Temperature Check (5 minutes)
1. Add an **"IF"** node
2. Configure condition:
   - **Value 1:** `{{$json.temperature}}`
   - **Operation:** `Larger`
   - **Value 2:** `20`
3. This splits your workflow into two paths

### Step 6: Add Currency API (5 minutes)
1. Connect to the **"true"** output of the IF node
2. Add **"HTTP Request"** node
3. Configure:
   - **Method:** GET
   - **URL:** `[MOCK-API-URL]/currency/USD`
4. Execute and verify currency rates appear

**Expected Output:**
```json
{
  "base": "USD",
  "rates": {
    "EUR": 0.85,
    "GBP": 0.73,
    "CHF": 0.88
  },
  "timestamp": "2025-10-22T10:30:00"
}
```

### Your Task (10 minutes)
**Modify the workflow:**
1. Change the city from "zurich" to another city (try "london", "paris", "berlin")
2. Change the temperature threshold to 15°C
3. Add a **third HTTP Request** on the **"false"** branch that fetches news:
   - URL: `[MOCK-API-URL]/news`

## Testing Your Workflow
1. Click **"Execute Workflow"** (top right)
2. Verify all nodes execute successfully (green checkmarks)
3. Check the output of each node
4. Try different cities to see different temperatures

## Common Issues

**❌ "Connection refused"**
- Check the Mock API URL is correct
- Make sure Mock API service is running in Coolify

**❌ "Node execution failed"**
- Click on the failed node to see error details
- Verify the URL has no typos

**❌ "Cannot read property 'temperature'"**
- Check the previous node's output
- The field name must match exactly (case-sensitive)

## Bonus Challenges (If You Finish Early)
1. Add error handling: Use the `/random-status` endpoint and handle failures
2. Add a delay: Call `/slow?delay=2` and see how your workflow handles it
3. Format the final output as a nice summary message

## What You Learned
✅ How to connect multiple services via APIs  
✅ How to transform data between service calls  
✅ How to use conditional logic in workflows  
✅ How to debug API integrations  

**Save your workflow!** (Top right corner)