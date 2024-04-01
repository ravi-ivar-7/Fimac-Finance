import requests

url = "https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqa1drTXZyM0hrYjlnTXl2VnVtVlByT3BzM216d3xBQ3Jtc0tteHMtLWYwbXVrdEI1VEV5Rk5sRmUtZnFpRmc5WEZzaTE2Mkw1YlBXZkJlaGdDX1dCQXhET1BKVk80dnR5U3BHMUFsanlpNGZsd09xYWMwX21uTVQtbmJZcE9UM2dFQmFWYjNSS0didm9YbmlLWGFnNA&q=https%3A%2F%2Fwww.nseindia.com%2Fapi%2Foption-chain-indices%3Fsymbol%3DNIFTY&v=2WePbjbK3zw"
response = requests.get(url)

if response.status_code == 200:
    print("Request successful")
else:
    print("Request failed with status code:", response.status_code)
    # Optionally handle errors here

data = response.content
# If it's a text-based format (e.g., CSV, JSON), decode it
decoded_data = data.decode("utf-8")  # Replace with appropriate encoding

import json

json_data = json.loads(decoded_data)

print(json_data)
# from jugaad_data.nse import NSE

# nse = NSE()
# historical_data = nse.get_history(symbol="TCS", series="EQ", start="2023-01-01", end="2023-08-01")
# print(historical_data)