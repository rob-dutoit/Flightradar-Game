from fr24sdk.client import Client

with Client(api_token="019c89cf-ef0f-7271-9cf8-6f39f4b5c7cf|vYAT0ETgOLG5QQNv46J0l898OGs4IZOe2g3paEfpd1890fdf") as client:
    result = client.live.flight_positions.get_light(bounds="50.682,46.218,14.422,22.243") # N, S, W, E
    print(result)