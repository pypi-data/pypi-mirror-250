import typer
from cli.xleap.sdk import Xleap

from xleap.models import DataPoint

a = DataPoint(
    question="Question: What were the temperatures and snowfall amounts during the cold snap in Afghanistan in January 2023, and how many people and livestock were affected?",
    answer="During the cold snap in Afghanistan in January 2023, temperatures dropped to record lows, reaching as low as -30 degrees Celsius (-22 degrees Fahrenheit) in some regions. The snowfall amounts varied across the country, with some areas experiencing heavy snowfall of up to 2 meters (6.5 feet), while others received lighter snowfall of around 30 centimeters (1 foot).\n\nAs for the number of people and livestock affected, it is estimated that approximately 500,000 people and 1 million livestock were affected by the extreme cold and heavy snowfall. These severe weather conditions caused disruptions in transportation, power outages, and limited access to essential services, leading to significant challenges for the affected population.",
)
b = DataPoint(
    question="did any russian player play?",
    answer="Yes, Russian players participated in Wimbledon 2023.",
    contexts=[
        "players, after they were banned from the previous edition due to the Russian invasion of Ukraine.",
        "Mate Pavić /  Lyudmyla Kichenok def.  Joran Vliegen /  Xu Yifan, 6-4, 6-7(9-11), 6-3",
        "disrupted by rain.The tournament saw the return of Russian and Belarusian tennis players, after",
        "The tournament was played on grass courts, with all main draw matches played at the All England",
    ],
)


def main(name: str = "Xleap"):
    print(f"Hello {name}")

    client = Xleap()

    r = client.data.create(body=b)
    print(r.parsed)


if __name__ == "__main__":
    typer.run(main)
