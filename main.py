import requests
import json
import time
import subprocess as sub


"""
Very bad WX alert scanner system thing.
Scans a state every 30 seconds for weather alerts.
"""


def clear(shell=True):
  sub.call("clear", shell=shell)


class Scan:

  def __init__(self, state):
    self.state = state

    self.main()

  def main(self):
    clear()

    url = "https://api.weather.gov/alerts/active"

    q = {"area": self.state}

    resp = requests.get(url, params=q)
    d = resp.content
    data = json.loads(d)

    title = data["title"]
    print(title)
    
    try:
      if not data["features"][0]["id"]:
        pass
    except IndexError:
      print("\nNo watches, warning, or advisories")
    finally:

      for each in data["features"]:
        id_url = each["id"]
  
        id_resp = requests.get(id_url)
        id_d = id_resp.content
        id_data = json.loads(id_d)
  
        VTEC = "VTEC was not giving by the API"
  
        try:
          event = id_data["properties"]["event"]
          area = id_data["properties"]["areaDesc"]
          ends = id_data["properties"]["ends"]
          status = id_data["properties"]["status"]
          response = id_data["properties"]["response"]
          headline = id_data["properties"]["headline"]
          urgency = id_data["properties"]["urgency"]
          severity = id_data["properties"]["severity"]
          description = id_data["properties"]["description"]
          instruction = id_data["properties"]["instruction"]
          sender = id_data["properties"]["sender"]
          senderName = id_data["properties"]["senderName"]
          messageType = id_data["properties"]["messageType"]
          WMOidentifier = id_data["properties"]["parameters"]["WMOidentifier"]
          VTEC = id_data["properties"]["parameters"]["VTEC"]
  
        except KeyError:
          pass
  
  
        if VTEC[0] != "V":
          VTEC = VTEC[0]
  
        if instruction is None:
          instruction = "Instruction was not giving by the API"
  
        body = f"""
{VTEC}
      
{WMOidentifier[0]}
Status............: {status}
Message Type......: {messageType}
Response..........: {response}
Urgency...........: {urgency}
Severity..........: {severity}
Ends..............: {ends}
Affected Area(s)..: {area}
      
      
{headline} ({sender})
      
{description}
      
{instruction}
      
-------------------------------------------"""
  
        with open("last.log", "r") as f:
          if f.read() == body:
            continue
  
        print(f"{id_url}/n{body}")
  
        with open("last.log", "w") as f:
          f.write(body)
          f.close()


if __name__ == "__main__":
  state = input("What state would you like to scan? ").upper()

  while True:
    Scan(state)
    print("Updating in 30 seconds...")
    time.sleep(30)

    with open("last.log", "w") as f:
      f.write("")
      f.close()
