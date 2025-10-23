# SDA4 Challenge 3: Resilient Data Fetcher
**Duration:** 40 minutes  
**Difficulty:** ⭐⭐⭐☆

## Learning Objectives
- Implement retry logic
- Handle API failures gracefully
- Build fault-tolerant workflows

## Scenario
You're fetching data from an unreliable API (simulated by `/random-status` endpoint). Your workflow must handle failures gracefully with retries.

## Step-by-Step Instructions

### Step 1: Create New Workflow (2 minutes)
1. In n8n, click **"New Workflow"**
2. Name it: "Challenge 3 - Resilient Fetcher"

### Step 2: Add Manual Trigger (2 minutes)
Standard manual trigger node

### Step 3: Add Unreliable API Call (5 minutes)
1. Add **"HTTP Request"** node
2. Configure:
   - **Method:** GET
   - **URL:** `https://mock-api.coolify.ecys.ch/random-status`
   - This endpoint randomly returns 200 or 500!
3. **Important:** Enable "Continue on Fail" in node settings
   - Click node → Settings (gear icon) → Check "Continue on Fail"

### Step 4: Add Error Detection (10 minutes)
1. Add **"IF"** node
2. Configure to check if previous node failed:
   - **Value 1:** `{{$node["HTTP Request"].json.status}}`
   - **Operation:** `Equal`
   - **Value 2:** `error`
3. This routes failures to error handling

### Step 5: Add Retry Counter (10 minutes)
We'll use n8n's built-in variables to track retries:

1. Add **"Code"** node on the **"true"** (error) path
2. Paste this code:
```javascript
// Get retry count (stored in workflow static data)
const retryCount = $getWorkflowStaticData('global').retryCount || 0;
const maxRetries = 3;

if (retryCount < maxRetries) {
  // Increment and retry
  $getWorkflowStaticData('global').retryCount = retryCount + 1;
  
  return {
    action: 'retry',
    attemptNumber: retryCount + 1,
    maxRetries: maxRetries
  };
} else {
  // Max retries reached
  $getWorkflowStaticData('global').retryCount = 0; // Reset for next run
  
  return {
    action: 'fail',
    message: 'Max retries reached',
    totalAttempts: retryCount + 1
  };
}
```

### Step 6: Add Retry Delay (8 minutes)
1. Add **"Wait"** node after the retry logic
2. Configure:
   - **Resume:** After time interval
   - **Wait time:** 2 seconds
3. This prevents hammering the API

### Step 7: Loop Back to Retry (5 minutes)
**This is tricky in n8n:**
1. You'll need to manually reconnect nodes to create a loop
2. From the Wait node, you want to go back to the HTTP Request
3. **Alternative (simpler):** Use n8n's built-in "Retry on Fail" option:
   - In HTTP Request node settings
   - Enable "Retry on Fail"
   - Set max retries: 3
   - Set wait between retries: 2000ms

### Your Task (15 minutes)
**Choose your approach:**

**Option A: Use n8n's Built-in Retry (Easier)**
1. Configure the HTTP Request node with retry settings
2. Add logging to track retry attempts
3. Add a final node that sends you a notification on final failure

**Option B: Build Custom Retry Logic (Advanced)**
1. Implement the loop-back pattern manually
2. Add exponential backoff (2s, 4s, 8s delays)
3. Log each attempt

### Testing
1. Execute the workflow multiple times
2. Watch how it handles random failures
3. Check that it eventually succeeds (or fails after max retries)

## Common Issues

**❌ "Can't create loop in workflow"**
- Use the built-in "Retry on Fail" instead
- Or use the "Loop Over Items" node (advanced)

**❌ "Retry count doesn't persist"**
- Workflow static data resets between manual executions
- This is expected behavior for testing

## Bonus Challenges
1. Add exponential backoff (delays increase: 1s, 2s, 4s, 8s)
2. Add different behavior for different error codes
3. Send a Slack/email notification on final failure

## What You Learned
✅ Fault tolerance patterns  
✅ Retry logic with delays  
✅ Circuit breaker concepts (manual implementation)  
✅ Error handling strategies  

**Save your workflow!**