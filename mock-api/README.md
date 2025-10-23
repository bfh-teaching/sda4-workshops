# SDA4 Mock API Service

## Quick Deploy to Coolify
1. Push this repo to GitHub
2. Coolify → New Service → Public Repository
3. Point to this repo
4. Port: 8080
5. Deploy

## Endpoints

### Weather
```bash
GET /weather/zurich
GET /weather/london
```

### Currency
```bash
GET /currency/USD
GET /currency/EUR
```

### News
```bash
GET /news
```

### Testing (Error Handling)
```bash
GET /random-status  # 50% chance of 500 error
GET /slow?delay=5   # Delayed response
```

### Echo (Webhook Testing)
```bash
POST /echo
Body: {"test": "data"}
```
