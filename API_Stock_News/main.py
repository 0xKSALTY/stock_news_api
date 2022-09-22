import requests
import smtplib
# API DOCUMENTATION https://www.alphavantage.co/documentation/
# API KEY REGISTER https://www.alphavantage.co/support/#api-key

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "P7FEEGDXXECOBSTM" # TODO ADD YOUR API KEY
NEWS_API_KEY = "1c5a322ed48b46e39bae5f45f649dffb" # TODO ADD YOUR API KEY
TWILIO_SID = "YOUR TWILIO ACCOUNT SID"
TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

MY_EMAIL = "fakeemail@gmail.com"
TO_EMAIL = "anotherfakeeemail@gmail.com"
PASSWORD = "qwerty"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT,
                        params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_data = day_before_yesterday_data["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_data)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_perc = round(difference / float(yesterday_closing_price)) * 100

if abs(diff_perc) > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT,
                                 params=news_params)

    news_response.raise_for_status()

    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    formatted_articles = [f"Headline: {article['title']}. " \
                          f"\nBrief: {article['description']}"
                          for article in three_articles]

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()  # encrypts email
        connection.login(user=MY_EMAIL,
                         password=PASSWORD)
        connection.sendmail(

            from_addr=MY_EMAIL,
            to_addrs=TO_EMAIL,
            msg=f"{STOCK_NAME}: {up_down}{diff_perc}%\n"
                f"Subject:Stock News\n\n{formatted_articles}"
        )


