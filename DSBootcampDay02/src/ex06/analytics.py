import logging
import config
from random import randint
import requests


logging.basicConfig(
    filename="analytics.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
class Research:
    def __init__(self,path):
        self.path = path
        self.head, self.tail = self.Calculations(self.file_read()).counts()
        self.head_fraction, self.tail_fraction = self.Calculations(self.file_read()).fractions()

    def file_read(self):
        has_header=True
        try:
            with open(self.path,"r") as data:
                lines = data.readlines()
                if has_header:
                    lines = lines[1:]
                result = []
                for line in lines:
                    clean_line = [1 if ch == '1' else 0 for ch in line.strip() if ch in "01"]
                    if clean_line:
                        result.append(clean_line)
                logging.info("%s file is successfully read!",self.path)
                return result
                       

        except FileNotFoundError:
            logging.error(f"{self.path}: No such file or directory!")
            return []

    def send_message_telegram(self):
        if config.success_in_built:
            message = "The report has been successfully created."
        else:
            message = "The report hasn’t been created due to an error."

        send_url = f"https://api.telegram.org/bot{config.API_TOKEN}/sendMessage?chat_id={config.CHAT_ID}&text={message}"
        channel_url = f"https://api.telegram.org/bot{config.API_TOKEN}/sendMessage?chat_id={config.CHANNEL_ID}&text={message}"

        try:
            response = requests.get(send_url)
            response1 = requests.get(channel_url)
            if response.status_code == 200 and response1.status_code == 200:
                logging.info("Telegram messages sent successfully.")
            else:
                logging.error("Failed to send Telegram message. Status codes: %d and %d", response.status_code,response1.status_code)
        except requests.RequestException as e:
            logging.error("Error sending message to Telegram: %s", str(e))

    class Calculations:
        def __init__(self,data):
            self.data = data

        def counts(self):
            head = 0
            tail = 0
            for numbers in self.data:
                if numbers[0] == 1:
                    head += 1
                if numbers[1] == 1:
                    tail += 1
            logging.info("Calculating the counts of %d heads and %d tails",head,tail)
            return [head,tail]

        def fractions(self):
            head ,tail = self.counts()
            total = head + tail
            if total == 0:
                logging.warning("No observations available to calculate fractions.")
                return [0, 0]
            head_fraction = (head / total) * 100
            tail_fraction = (tail / total) * 100
            logging.info("Fraction of heads : %d  and tails : %d ",head_fraction,tail_fraction)
            return [head_fraction, tail_fraction]

class Analytics(Research.Calculations):
    def __init__(self,data, number):
        super().__init__(data)
        self.number = number
    
    def predict_random(self):
        predictions=[[1,0] if randint(0,1) else [0,1] for _ in range(self.number)]
        logging.info("Generated %d random predictions: %s", self.number, predictions)
        return predictions


    def predict_last(self):
        if not self.data:
            logging.warning("No data available to predict last observation.")
            return []
        last=self.data[-1]
        logging.info("Last ")
        return last
    
    def save_file(self, data, filename):
        try:
            with open(f"{filename}.txt","w") as file:
                file.write(data)
                config.success_in_built=1
                logging.info(f"{filename}: File has been created!")
        except Exception as e:
            config.success_in_built=0
            logging.error(f"{filename}: File could not be created!")
            logging.error(f"Error : {str(e)}")