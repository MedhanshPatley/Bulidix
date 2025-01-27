# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import yfinance as yf
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai
# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# @app.route('/')
# def home():
#     return "Welcome to the Stock Analysis API! Use the endpoint '/api/stock-analysis' to fetch insights."

# @app.route('/api/stock-analysis', methods=['POST'])
# def stock_analysis():
#     try:
#         data = request.get_json()
#         ticker = data.get('ticker', None)

#         if not ticker:
#             return jsonify({'error': 'Ticker symbol is required'}), 400

#         insights = fetch_insights(ticker)
#         return jsonify(insights)

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# def fetch_insights(ticker):
#     try:
#         # Fetch stock data from yfinance
#         stock = yf.Ticker(ticker)
#         data = stock.history(period="1d", interval="1m")

#         # Check if data is empty
#         if data.empty:
#             return {'error': f"No data available for ticker {ticker}"}

#         # Extract relevant metrics
#         current_price = data['Close'].iloc[-1] if not data['Close'].empty else None
#         initial_price = data['Close'].iloc[0] if not data['Close'].empty else None
#         info = stock.info or {}

#         if current_price is None or initial_price is None:
#             return {'error': f"Unable to fetch price data for ticker {ticker}"}

#         insights = {
#             'Current Price': f"${current_price:.2f}",
#             'Growth %': f"{((current_price - initial_price) / initial_price * 100):.2f}%" if initial_price else "N/A",
#             'P/E Ratio': info.get('trailingPE', 'N/A'),
#             'Market Cap': f"${info.get('marketCap', 'N/A'):,}" if info.get('marketCap') else 'N/A',
#             'Dividend Yield': f"{info.get('dividendYield', 0) * 100:.2f}%",
#             '52 Week High': f"${info.get('fiftyTwoWeekHigh', 'N/A')}",
#             '52 Week Low': f"${info.get('fiftyTwoWeekLow', 'N/A')}"
#         }

#         # Generate AI analysis (ensure the AI setup is correct)
#         api_key = os.environ.get('GEMINI_API_KEY')
#         genai.configure(api_key=api_key)
#         model = genai.GenerativeModel('gemini-1.5-flash-8b')

#         insights_text = "\n".join([f"{k}: {v}" for k, v in insights.items()])
#         prompt = f"Provide a concise stock analysis for {ticker} based on these metrics:\n{'  '.join([f'{k}: {v}' for k, v in insights.items()])}"

#         response = model.generate_content(prompt)
#         analysis = f"""
#         Stock Analysis for {ticker}
# Key Metrics:

# Current Price: {insights['Current Price']}
# 52 Week High: {insights['52 Week High']}
# 52 Week Low: {insights['52 Week Low']}
# Dividend Yield: {insights['Dividend Yield']}
# Growth %: {insights['Growth %']}
# Market Cap: {insights['Market Cap']}
# P/E Ratio: {insights['P/E Ratio']}

# Analysis:
# The current stock price of {ticker} is {insights['Current Price']}, which is down slightly from its 52-week high of {insights['52 Week High']} and 52-week low of {insights['52 Week Low']}. This wide price range indicates volatility in the stock.
# The company's P/E ratio of {insights['P/E Ratio']} and dividend yield of {insights['Dividend Yield']} suggest moderate valuation and income potential. Its large market cap of {insights['Market Cap']} implies it is a significant player in the industry.
# However, the negative growth percentage of {insights['Growth %']} is a concerning trend that warrants further investigation. Additional analysis of the company's financials, industry positioning, and strategic initiatives would be needed to fully assess the outlook.
# In summary, {ticker} displays both strengths and risks based on the current metrics. A deeper dive into the underlying factors driving performance is recommended to determine if this is a temporary blip or a more significant trend.
# """
#         return {
#             'metrics': insights,
#             'aiAnalysis': analysis
#         }

#     except Exception as e:
#         return {'error': str(e)}


# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Welcome to the Stock Analysis API! Use the endpoint '/api/stock-analysis' to fetch insights."

@app.route('/api/stock-analysis', methods=['POST'])
def stock_analysis():
    try:
        data = request.get_json()
        ticker = data.get('ticker', None)

        if not ticker:
            return jsonify({'error': 'Ticker symbol is required'}), 400

        insights = fetch_insights(ticker)
        return jsonify(insights)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def fetch_insights(ticker):
    try:
        # Fetch stock data
        stock = yf.Ticker(ticker)
        data = stock.history(period="1mo")
        current_price = data['Close'].iloc[-1] if not data['Close'].empty else None
        initial_price = data['Close'].iloc[0] if not data['Close'].empty else None
        info = stock.info or {}

        # Revenue Growth Calculation
        income_statements = stock.income_stmt
        latest_revenue = income_statements.loc['Total Revenue'].iloc[0] if not income_statements.empty and len(income_statements.columns) > 1 else None
        previous_revenue = income_statements.loc['Total Revenue'].iloc[1] if len(income_statements.columns) > 1 else None
        revenue_growth = ((latest_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue else None

        # RSI Calculation
        def calculate_rsi(data, periods=14):
            delta = data['Close'].diff()
            up = delta.clip(lower=0)
            down = -1 * delta.clip(upper=0)
            ma_up = up.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
            ma_down = down.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
            rs = ma_up / ma_down
            rsi = 100.0 - (100.0 / (1.0 + rs))
            return rsi.iloc[-1]
        
        rsi = calculate_rsi(data)

        # Market Position Metrics
        market_cap = info.get('marketCap', 'N/A')
        sector = info.get('sector', 'N/A')
        industry = info.get('industry', 'N/A')

        insights = {
            'Price': f"${current_price:.2f}" if current_price else 'N/A',
            'Revenue Growth': f"{revenue_growth:.2f}%" if revenue_growth is not None else 'N/A',
            'RSI': f"{rsi:.2f}" if rsi is not None else 'N/A',
            'Growth %': f"{((current_price - initial_price) / initial_price * 100):.2f}%" if initial_price and current_price else "N/A",
            'P/E Ratio': info.get('trailingPE', 'N/A'),
            'Market Cap': f"${market_cap:,}" if market_cap != 'N/A' else 'N/A',
            'Dividend Yield': f"{info.get('dividendYield', 0) * 100:.2f}%",
            '52 Week High': f"${info.get('fiftyTwoWeekHigh', 'N/A')}",
            '52 Week Low': f"${info.get('fiftyTwoWeekLow', 'N/A')}",
            'Sector': sector,
            'Industry': industry
        }

        api_key = os.environ.get('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-8b')

        prompt = f"""
Provide a comprehensive stock analysis for {ticker} based on these metrics:

Market Position:
- Sector: {sector}  
- Industry: {industry}  

Financial Performance: 
- Price: {insights['Price']}  
- Revenue Growth: {insights['Revenue Growth']}  
- P/E Ratio: {insights['P/E Ratio']}  
- Dividend Yield: {insights['Dividend Yield']}  

Technical Indicators:
- RSI: {insights['RSI']}  
- 52-Week Range: {insights['52 Week Low']} - {insights['52 Week High']}  
- Market Cap: {insights['Market Cap']}  

Analyze the stock's current performance, potential risks, and investment outlook.
Use the following structure and ensure that each heading is followed by its respective content :
Stock Analysis for {ticker}

Market Position:
Provide details about the company’s market position, focusing on its sector and industry.

Summary:
Summarize the company’s financial and technical standing in a few concise sentences.

Financial Performance:  
 Price: Explain the current price trend and how it compares to historical data.  
 Revenue Growth: Analyze the revenue growth figure and what it suggests about the company.  
 P/E Ratio: Discuss the significance of the P/E ratio and how it compares to the industry average.  
 Dividend Yield: Evaluate the attractiveness of the dividend yield for potential investors.

Technical Indicators: 
 RSI: Interpret the RSI value and what it implies about market sentiment (e.g., neutral, overbought, or oversold).  
 52-Week Range: Discuss the stock’s historical price volatility based on its 52-week range.  
 Market Cap:Explain the company’s market capitalization and its implications for company size and investor confidence.

Current Performance Analysis:
Provide an analysis of the stock's current performance, synthesizing financial and technical metrics.

Potential Risks:  
List the key risks associated with investing in the company, including economic, sectoral, and company-specific risks.

Investment Outlook:
Offer a detailed investment outlook based on the financial performance and technical indicators. Highlight any opportunities or challenges for the stock in the near term and long term. \n

Conclusion:
Summarize your overall analysis, emphasizing the key takeaways.

Recommendation:
provide your final recommendations for investors based on the all analysis.


Be clear and ensure that response is short,and contains only relevant information. 
"""



        
        response = model.generate_content(prompt)
        analysis = response.text

        return {
            'metrics': insights,
            'aiAnalysis': analysis
        }

    except Exception as e:
        return {'error': str(e)}
if __name__ == '__main__':
    app.run(debug=True)

