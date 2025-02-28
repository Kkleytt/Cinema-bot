import subprocess
import json


api_key = "4a7ba7f7-31b6-4df3-8308-827ce7c1deb0"
url_kino = f"https://kinopoiskapiunofficial.tech/api/v2.2/films/1431131"
text = []
command = [
    "curl",
    "-X", "GET",
    url_kino,
    "-H", "accept: application/json",
    "-H", f"X-API-KEY: {api_key}"
]
result = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
)
stdout, stderr = result.communicate()

data = json.loads(stdout)
for key, value in data.items():
    if key == 'nameRu':
        print(f"Name - {value}")
    elif key == 'year':
        print(f"Year - {value}")
    else:
        continue