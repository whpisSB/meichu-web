echo 'endpoint?'
read endpoint
echo 'method?'
read method
echo 'data?'
read data
echo 'JWT?'
read JWT

echo response:
curl -H "Content-Type: application/json" -H "Authorization: Bearer $JWT" -X $method http://localhost:5000/$endpoint -d "$data"
