# imports
from openai import OpenAI
import requests
import json
import streamlit as st

# thêm api key 
api_key = "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"
client = OpenAI(api_key=api_key)


# basic connection with ChatGPT API
def BasicGeneration(userPrompt):
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",  
            prompt=userPrompt,
            max_tokens=1500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {str(e)}")
        return "An error occurred while processing your request."



# Get Bitcoin Price From the last 7 days from Crypto API (rapidAPI Example)
def GetBitCoinPrices():
    # Define the API endpoint and query parameters
    url = "https://coinranking1.p.rapidapi.com/coin/Qwsogvtv82FCd/history"
    querystring = {
        "referenceCurrencyUuid": "yhjMzLPhuIDl",
        "timePeriod": "7d"
    }
    # Define the request headers with API key and host
    headers = {
        "X-RapidAPI-Key": "b76daedcf2msha6278a0d8d2c2e5p15e757jsn7bb3be80a722",
        "X-RapidAPI-Host": "coinranking1.p.rapidapi.com"
    }
    # Send a GET request to the API endpoint with query parameters and headers
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    # Parse the response data as a JSON object
    JSONResult = json.loads(response.text)
    # Extract the "history" field from the JSON response
    history = JSONResult["data"]["history"]
    # Extract the "price" field from each element in the "history" array and add to a list
    prices = []
    for change in history:
        prices.append(change["price"])
    # Join the list of prices into a comma-separated string
    pricesList = ','.join(prices)
    # Return the comma-separated string of prices
    return pricesList


def AnalyzeBitCoin(bitcoinPrices):
    chatGPTPrompt = f"""You are an expert crypto trader with more than 10 years of experience, 
    I will provide you with a list of bitcoin prices for the last 7 days
    can you provide me with a technical analysis
    of Bitcoin based on these prices. here is what I want: 
    Price Overview, 
    Moving Averages, 
    Relative Strength Index (RSI),
    Moving Average Convergence Divergence (MACD),
    Advice and Suggestion,
    Do I buy or sell?
    Please be as detailed as you can, and explain in a way any beginner can understand. and make sure to use headings
    Here is the price list: {bitcoinPrices} and don't forget to highlight every point"""

    return BasicGeneration(chatGPTPrompt)



def main():
    st.title("Analyze Bitcoin Prices")
    st.subheader("Find out market prices and forecasts")

    # Get prices
    bitcoin_prices = GetBitCoinPrices()
    st.text(f"Bitcoin price in the last 7 days: {bitcoin_prices}")

    # Button to trigger analysis
    if st.button("Analyze"):
        # Display loading icon
        with st.spinner('Running analysis...'):
            # Analyze Bitcoin prices
            result = AnalyzeBitCoin(bitcoin_prices)
        # Display result
        st.subheader("Result")
        st.write(result)
        # Indicate that the analysis is done
        st.success('Done!')

# Run the Streamlit app
if __name__ == "__main__":
    main()
