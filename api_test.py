import requests

url = "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/150107"

headers = {
	"x-rapidapi-key": "7244d01c4emsh70c1032c3f361ebp109e6fjsna48cf9f005e3",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print(response.json())