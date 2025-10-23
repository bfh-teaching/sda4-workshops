# SDA4 Challenge 2: Webhook Event Processor
**Duration:** 30 minutes  
**Difficulty:** ⭐⭐☆☆

## Learning Objectives
- Understand event-driven architecture
- Work with webhooks (vs. polling)
- Route events based on type

## Scenario
You're building an event processor that receives webhook events (user signups, logins, purchases) and routes them to different actions.

## Step-by-Step Instructions

### Step 1: Create New Workflow (2 minutes)
1. In n8n, click **"New Workflow"**
2. Name it: "Challenge 2 - Webhook Events"

### Step 2: Add Webhook Trigger (5 minutes)
1. Click **"+"** to add node
2. Search for **"Webhook"**
3. Configure:
   - **HTTP Method:** POST
   - **Path:** `student-events`
4. **Important:** Copy the webhook URL that appears (looks like: `https://n8n.../webhook/student-events`)

### Step 3: Parse Incoming Data (8 minutes)
1. Add a **"Code"** node after the webhook
2. Paste this code:
```javascript
const payload = $input.item.json.body;

return {
  event_type: payload.event_type || 'unknown',
  user_id: payload.user_id || 'anonymous',
  data: payload.data || {},
  received_at: new Date().toISOString()
};
```
3. Don't execute yet (we need to send data first)

### Step 4: Test the Webhook (10 minutes)

**Option A: Using curl (Command Line)**
Open your terminal and run:
```bash
curl -X POST [YOUR-WEBHOOK-URL] \
  -H "Content-Type: application/json" \
  -d '{"event_type": "user_signup", "user_id": "123", "data": {"email": "test@example.com"}}'
```

**Option B: Using Postman (If you have it)**
1. Create new POST request
2. Enter your webhook URL
3. Body → Raw → JSON:
```json
{
  "event_type": "user_signup",
  "user_id": "123",
  "data": {"email": "test@example.com"}
}
```
4. Send

**Option C: Using Python (If terminal scares you)**
```python
import requests

url = "YOUR-WEBHOOK-URL"
data = {
    "event_type": "user_signup",
    "user_id": "123",
    "data": {"email": "test@example.com"}
}

response = requests.post(url, json=data)
print(response.status_code)
```

### Step 5: Add Event Router (10 minutes)
1. Add a **"Switch"** node (or "Route" in some versions)
2. Configure three routes:
   - **Route 0:** `event_type` equals `user_signup`
   - **Route 1:** `event_type` equals `user_login`
   - **Route 2:** `event_type` equals `purchase`
3. This will create 3 output branches

### Step 6: Add Actions per Event Type (15 minutes)
Add different HTTP Request nodes to each branch:

**For "user_signup":**
- Add HTTP Request node
- Method: POST
- URL: `https://webhook.site/[unique-id]` (create at webhook.site)
- Body: `{"action": "send_welcome_email", "user": "{{$json.user_id}}"}`

**For "user_login":**
- Add HTTP Request node
- URL: `https://webhook.site/[unique-id]`
- Body: `{"action": "log_activity", "user": "{{$json.user_id}}"}`

**For "purchase":**
- Add HTTP Request node
- URL: `https://webhook.site/[unique-id]`
- Body: `{"action": "process_order", "user": "{{$json.user_id}}"}`

### Your Task (20 minutes)
1. **Send 3 different events** to your webhook (one of each type)
2. **Verify each routes correctly** (check webhook.site)
3. **Add a 4th event type:** `password_reset`
4. **Add error handling:** What if event_type is missing?

## Testing Checklist
- [ ] Webhook receives data successfully
- [ ] Parse node extracts fields correctly
- [ ] Switch routes to correct branch
- [ ] Each branch executes its action
- [ ] Can see results in webhook.site

## Common Issues

**❌ "Webhook not found"**
- Workflow must be **Active** (toggle in top right)
- Check URL is exactly as shown in webhook node

**❌ "Nothing happens when I send data"**
- Check workflow execution history (left sidebar)
- Verify JSON is valid (use jsonlint.com)

**❌ "Switch node doesn't route"**
- Check exact spelling of event_type values
- Use === (exact match) in conditions

## Bonus Challenges
1. Add timestamp validation (reject old events)
2. Add rate limiting (max 10 events per minute)
3. Store events in a database (use HTTP Request to a storage service)

## What You Learned
✅ Webhooks vs. polling (push vs. pull)  
✅ Event-driven architecture patterns  
✅ Event routing and conditional processing  
✅ How to test async workflows  

**Save and keep Active!** You'll use this in Challenge 4.