# SDA4 Challenge 4: Hybrid Cloud Agent
**Duration:** 40 minutes  
**Difficulty:** ⭐⭐⭐⭐

## Learning Objectives
- Understand hybrid cloud architecture
- Implement service-to-service communication
- Build workflow orchestration across boundaries
- Recognize service mesh patterns

## Scenario
You're building a hybrid cloud system where:
- **Workflow A** (Public Cloud) receives external requests
- **Workflow B** (Private Cloud) processes sensitive data
- They communicate securely across cloud boundaries

In this workshop, both workflows are in the same n8n instance, but we'll simulate the architecture pattern.

## Architecture Diagram
```
External Request → Workflow A (Public) → Workflow B (Private) → Response → Workflow A → Client
```

## Step-by-Step Instructions

### Part 1: Build Workflow B (Private Cloud Service) - 15 minutes

#### Step 1: Create Workflow B (5 minutes)
1. Click **"New Workflow"**
2. Name it: "Challenge 4 - Workflow B (Private)"
3. Save it immediately (important for later reference)

#### Step 2: Add Webhook Trigger (5 minutes)
1. Add **"Webhook"** node as the starting point
2. Configure:
   - **HTTP Method:** POST
   - **Path:** `private-processor`
   - **Authentication:** None (we'll discuss security after)
3. **Important:** Copy the webhook URL that appears
   - Example: `https://your-n8n.com/webhook/private-processor`
   - **Save this URL** - you'll need it for Workflow A

#### Step 3: Add Data Processing Logic (10 minutes)
1. Add **"Code"** node after the webhook
2. Paste this code:
```javascript
// Simulate private cloud processing
const inputData = $input.item.json.body;

// Validate input
if (!inputData || !inputData.data) {
  throw new Error("Missing required field: data");
}

// Process data (simulate sensitive operations)
const processed = {
  original: inputData.data,
  processed_at: new Date().toISOString(),
  processed_by: "private-cloud-service",
  security_level: "high",
  encrypted: true,
  // Simulate data transformation
  result: `Processed: ${inputData.data.toUpperCase()}`
};

return processed;
```

#### Step 4: Add Response Formatting (5 minutes)
1. Add **"Set"** node (or "Edit Fields" in newer versions)
2. Configure to format the response:
   - Keep all fields from previous node
   - Add field: `status` = `success`
   - Add field: `service` = `workflow-b-private`

#### Step 5: Test Workflow B Independently (5 minutes)
Before connecting to Workflow A, test that B works:

**Using curl:**
```bash
curl -X POST [YOUR-WORKFLOW-B-WEBHOOK-URL] \
  -H "Content-Type: application/json" \
  -d '{"data": "test message"}'
```

**Expected Response:**
```json
{
  "original": "test message",
  "processed_at": "2025-10-22T10:30:00.000Z",
  "processed_by": "private-cloud-service",
  "security_level": "high",
  "encrypted": true,
  "result": "Processed: TEST MESSAGE",
  "status": "success",
  "service": "workflow-b-private"
}
```

**✅ Checkpoint:** Workflow B must work before continuing!

---

### Part 2: Build Workflow A (Public Cloud Orchestrator) - 20 minutes

#### Step 6: Create Workflow A (5 minutes)
1. Click **"New Workflow"**
2. Name it: "Challenge 4 - Workflow A (Public)"
3. This will be the main orchestrator

#### Step 7: Add Public Webhook (5 minutes)
1. Add **"Webhook"** node as starting point
2. Configure:
   - **HTTP Method:** POST
   - **Path:** `public-gateway`
3. Copy this webhook URL - this is your "public entry point"

#### Step 8: Add Input Validation (5 minutes)
1. Add **"Code"** node after webhook
2. Paste this code:
```javascript
// Validate incoming request
const payload = $input.item.json.body;

if (!payload || !payload.data) {
  throw new Error("Invalid request: missing 'data' field");
}

// Log request (in production, this would go to logging service)
console.log(`[Workflow A] Request received at ${new Date().toISOString()}`);

return {
  request_id: `req-${Date.now()}`,
  data: payload.data,
  received_at: new Date().toISOString()
};
```

#### Step 9: Call Workflow B (10 minutes)
This is the key step - cross-service communication!

1. Add **"HTTP Request"** node
2. Configure:
   - **Method:** POST
   - **URL:** `[YOUR-WORKFLOW-B-WEBHOOK-URL]` (from Step 2)
   - **Body Content Type:** JSON
   - **Body (JSON):**
```json
   {
     "data": "={{ $json.data }}",
     "request_id": "={{ $json.request_id }}",
     "source": "workflow-a"
   }
```
3. **Advanced Settings:**
   - Timeout: 10000 (10 seconds)
   - Continue on Fail: Enabled (for error handling)

#### Step 10: Add Response Aggregation (10 minutes)
1. Add **"Code"** node after the HTTP Request
2. Paste this code:
```javascript
// Combine data from Workflow A and Workflow B
const requestData = $input.first().json;
const privateServiceResponse = $input.item.json;

// Check if private service call succeeded
if (!privateServiceResponse || privateServiceResponse.error) {
  return {
    status: "error",
    message: "Private service unavailable",
    request_id: requestData.request_id,
    error_details: privateServiceResponse
  };
}

// Aggregate successful response
return {
  status: "success",
  request_id: requestData.request_id,
  original_data: requestData.data,
  processed_data: privateServiceResponse.result,
  processing_details: {
    processed_at: privateServiceResponse.processed_at,
    processed_by: privateServiceResponse.processed_by,
    security_level: privateServiceResponse.security_level
  },
  workflow_chain: ["workflow-a-public", "workflow-b-private"],
  completed_at: new Date().toISOString()
};
```

#### Step 11: Add Logging (5 minutes)
1. Add **"HTTP Request"** node (parallel branch if possible)
2. Configure to log to Mock API:
   - **Method:** POST
   - **URL:** `[MOCK-API-URL]/echo`
   - **Body:**
```json
   {
     "event": "workflow_completed",
     "request_id": "={{ $json.request_id }}",
     "timestamp": "={{ $json.completed_at }}"
   }
```

---

### Part 3: Testing the Complete System - 10 minutes

#### Step 12: End-to-End Test
1. **Activate both workflows** (toggle in top right of each)
2. Send request to Workflow A:
```bash
curl -X POST [YOUR-WORKFLOW-A-WEBHOOK-URL] \
  -H "Content-Type: application/json" \
  -d '{"data": "hybrid cloud test"}'
```

**Expected Complete Response:**
```json
{
  "status": "success",
  "request_id": "req-1729680000000",
  "original_data": "hybrid cloud test",
  "processed_data": "Processed: HYBRID CLOUD TEST",
  "processing_details": {
    "processed_at": "2025-10-22T10:30:00.000Z",
    "processed_by": "private-cloud-service",
    "security_level": "high"
  },
  "workflow_chain": ["workflow-a-public", "workflow-b-private"],
  "completed_at": "2025-10-22T10:30:05.000Z"
}
```

#### Step 13: Verify Both Workflows Executed
1. Check execution history in Workflow A (left sidebar)
2. Check execution history in Workflow B
3. Both should show successful executions with matching request IDs

---

### Your Task - 15 minutes

**Level 1: Basic (Required)**
1. ✅ Get both workflows communicating successfully
2. ✅ Verify end-to-end response contains data from both workflows
3. ✅ Test with different input data

**Level 2: Intermediate (Recommended)**
1. Add **error handling**: What if Workflow B is down?
   - Disable Workflow B
   - Send request to Workflow A
   - Ensure error is handled gracefully
2. Add **timeout handling**: What if Workflow B is slow?
   - Add a Wait node in Workflow B (5 seconds)
   - Set timeout in Workflow A to 3 seconds
   - Verify timeout error is caught

**Level 3: Advanced (Bonus)**
1. Add **authentication** between workflows:
   - Add API key validation in Workflow B
   - Send API key header from Workflow A
   - Test with valid/invalid keys
2. Add **retry logic** in Workflow A:
   - If Workflow B fails, retry up to 3 times
   - Add exponential backoff
3. Add **circuit breaker pattern**:
   - After 3 consecutive failures, stop calling Workflow B
   - Return cached/fallback response

---

## Testing Checklist

- [ ] Workflow B responds to direct webhook calls
- [ ] Workflow A can reach Workflow B
- [ ] Complete request flows through both workflows
- [ ] Error handling works when Workflow B fails
- [ ] Logs show complete request chain
- [ ] Response includes data from both services

---

## Common Issues

### ❌ "Workflow B not found / 404"
**Cause:** Workflow B is not active or webhook URL is wrong  
**Fix:** 
- Toggle "Active" in Workflow B (top right)
- Double-check webhook URL (must include https://)
- Test Workflow B independently first

### ❌ "Timeout error"
**Cause:** Workflow B is taking too long to respond  
**Fix:**
- Check Workflow B execution history for errors
- Increase timeout in Workflow A's HTTP Request node
- Remove any Wait nodes in Workflow B during testing

### ❌ "Cannot read property 'result'"
**Cause:** Workflow B's response structure doesn't match expectations  
**Fix:**
- Check Workflow B's actual response in execution history
- Update field names in Workflow A to match
- Add null checks: `$json.result || 'default value'`

### ❌ "Circular dependency error"
**Cause:** Accidentally created a loop (A calls B, B calls A)  
**Fix:**
- Verify Workflow B does NOT have HTTP Request calling Workflow A
- Workflow B should only respond, not initiate calls

### ❌ "Both workflows execute but response is empty"
**Cause:** Data not passed correctly between workflows  
**Fix:**
- Check that Workflow A's HTTP Request body contains `data` field
- Verify Workflow B reads from `$input.item.json.body`
- Use `{{ $json.fieldName }}` syntax for dynamic values

---

## Architecture Discussion Points

After completing the challenge, discuss with your group:

1. **Trust Boundaries:**
   - In our setup, both workflows are in the same n8n instance
   - In real hybrid cloud: different security zones, networks, credentials
   - How would you secure cross-boundary communication?

2. **Service Discovery:**
   - We hardcoded Workflow B's URL in Workflow A
   - In production: service registry, DNS, API gateway
   - What happens when Workflow B's URL changes?

3. **Failure Modes:**
   - What if Workflow B is deployed in a region that goes down?
   - How do you handle partial failures?
   - Should Workflow A have a fallback/cache?

4. **Observability:**
   - How do you trace a request across multiple services?
   - What about distributed logging/tracing (request IDs)?
   - How do you monitor cross-service latency?

5. **API Gateway Pattern:**
   - Workflow A acts like an API gateway
   - What other responsibilities could it have?
   - (Rate limiting, authentication, routing, transformation)

---

## Real-World Hybrid Cloud Scenarios

This pattern applies to:

1. **Regulated Data Processing:**
   - Public cloud: User-facing app
   - Private cloud: Medical/financial data processing
   - Reason: Compliance requirements (GDPR, HIPAA)

2. **Legacy System Integration:**
   - Public cloud: Modern microservices
   - On-premises: Legacy mainframe/database
   - Reason: Cannot migrate legacy systems

3. **Edge Computing:**
   - Cloud: Central orchestration
   - Edge: Local processing (IoT devices, stores)
   - Reason: Low latency, offline capability

4. **Multi-Cloud Strategy:**
   - AWS: Primary services
   - Azure: Specific AI/ML services
   - Reason: Best-of-breed services, vendor independence

---

## Bonus Challenges (If You Finish Early)

### Challenge 4.1: Add a Third Workflow (Multi-Hop)
```
Workflow A → Workflow B → Workflow C → Workflow B → Workflow A
```
Create Workflow C that does additional processing, called by Workflow B.

### Challenge 4.2: Implement Request Tracing
Add a `trace_id` that follows the request through all workflows:
- Generate in Workflow A
- Pass to Workflow B
- Include in all logs
- Return in final response

### Challenge 4.3: Add Async Processing
Modify Workflow A to:
1. Immediately return "processing" status
2. Call Workflow B asynchronously
3. Use a webhook callback when complete
4. (Advanced: requires understanding of async patterns)

### Challenge 4.4: Build a Simple API Gateway
Extend Workflow A to:
- Route to different private workflows based on request type
- Add rate limiting (max 10 requests per minute)
- Add request/response transformation
- Add authentication

---

## What You Learned

✅ **Hybrid cloud architecture patterns**  
✅ **Inter-service communication** (synchronous HTTP calls)  
✅ **Service orchestration** (coordinating multiple services)  
✅ **Error handling across service boundaries**  
✅ **API gateway concepts** (routing, aggregation)  
✅ **Distributed system challenges** (timeouts, failures, tracing)  
✅ **Security considerations** (trust boundaries, authentication)  

---

## Connection to SDA2 (This Afternoon)

In this challenge, you orchestrated pre-existing services (Workflows A & B).

**This afternoon in SDA2**, you'll learn how to:
- **Build those underlying services** (like Workflow B)
- **Deploy them** with CI/CD
- **Scale them** independently
- **Monitor them** in production

The services you deploy in SDA2 could be called by n8n workflows like this!

---

## Save Both Workflows!

Make sure both workflows are:
- ✅ Saved with clear names
- ✅ Set to "Active"
- ✅ Documented (add notes to complex nodes)

**Pro tip:** Export both workflows as JSON for backup:
- Workflow settings → Download
- Save to your computer
