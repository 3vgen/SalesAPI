# SalesAPI
Успешный анализ продаж
```
curl -X POST http://localhost:8000/api/v1/sales/analyze_sales \
  -H "Content-Type: application/json" \
  -d '{
    "sales": [
      {"dish": "Паста Карбонара", "cost_price": 180, "selling_price": 450, "quantity": 12},
      {"dish": "Цезарь с курицей", "cost_price": 140, "selling_price": 390, "quantity": 8},
      {"dish": "Маргарита", "cost_price": 90, "selling_price": 320, "quantity": 25}
    ]
  }'
```

