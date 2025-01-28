from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import os
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime, timedelta
import pandas as pd

load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


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
@app.route('/api/search-stocks', methods=['GET'])
def search_stocks():
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])
    
    try:
        # Using yfinance to search for stocks
        stock = yf.Ticker(query)
        matches = []
        
        # Get suggestions from common stock search patterns
        possible_tickers = [
            query.upper(),  # Exact match
            f"{query.upper()}.X",  # International stocks
            f"{query.upper()}-USD"  # Crypto
        ]
        
        for ticker_try in possible_tickers:
            try:
                stock = yf.Ticker(ticker_try)
                info = stock.info
                if info and 'longName' in info:
                    matches.append({
                        'ticker': ticker_try.split('.')[0],  # Remove any suffix
                        'name': info.get('longName', ''),
                        'exchange': info.get('exchange', '')
                    })
            except:
                continue
                
        return jsonify(matches)
    except Exception as e:
        print(f"Error searching stocks: {e}")
        return jsonify([])


def calculate_period_performance(data, period):
    if data.empty:
        return 'N/A'
    current_price = data['Close'].iloc[-1]
    initial_price = data['Close'].iloc[0]
    return f"{((current_price - initial_price) / initial_price * 100):.2f}%"

def fetch_insights(ticker):
    try:
        stock = yf.Ticker(ticker)
        
        # Fetch historical data for different periods
        data_1y = stock.history(period="1y")
        data_3y = stock.history(period="3y")
        data_5y = stock.history(period="5y")
        current_data = stock.history(period="1mo")
        
        # Get current metrics
        current_price = current_data['Close'].iloc[-1] if not current_data['Close'].empty else None
        info = stock.info or {}

        # Calculate historical performance
        performance_1y = calculate_period_performance(data_1y, '1y')
        performance_3y = calculate_period_performance(data_3y, '3y')
        performance_5y = calculate_period_performance(data_5y, '5y')

        # Revenue Growth Calculations
        income_statements = stock.income_stmt
        
        def calculate_revenue_growth(data, periods):
            if data.empty or len(data.columns) < periods:
                return 'N/A'
            latest_revenue = data.loc['Total Revenue'].iloc[0]
            past_revenue = data.loc['Total Revenue'].iloc[periods-1]
            return f"{((latest_revenue - past_revenue) / past_revenue * 100):.2f}%"

        revenue_growth_1y = calculate_revenue_growth(income_statements, 2)
        revenue_growth_3y = calculate_revenue_growth(income_statements, 4)
        revenue_growth_5y = calculate_revenue_growth(income_statements, 6)

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
        
        rsi = calculate_rsi(current_data)

        insights = {
            'Current Price': f"${current_price:.2f}" if current_price else 'N/A',
            'Performance 1 Year': performance_1y,
            'Performance 3 Year': performance_3y,
            'Performance 5 Year': performance_5y,
            'Revenue Growth 1 Year': revenue_growth_1y,
            'Revenue Growth 3 Year': revenue_growth_3y,
            'RSI': f"{rsi:.2f}" if rsi is not None else 'N/A',
            'P/E Ratio': info.get('trailingPE', 'N/A'),
            'Market Cap': f"${info.get('marketCap', 'N/A'):,}" if info.get('marketCap') != 'N/A' else 'N/A',
            'Dividend Yield': f"{info.get('dividendYield', 0) * 100:.2f}%",
            '52 Week High': f"${info.get('fiftyTwoWeekHigh', 'N/A')}",
            '52 Week Low': f"${info.get('fiftyTwoWeekLow', 'N/A')}",
            'Sector': info.get('sector', 'N/A'),
            'Industry': info.get('industry', 'N/A')
        }

        api_key = os.environ.get('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-8b')

        prompt = f"""
Provide a comprehensive stock analysis for {ticker} based on these metrics:

Market Position:
- Sector: {insights['Sector']}
- Industry: {insights['Industry']}

Historical Performance:
1 Year: {insights['Performance 1 Year']}
3 Year: {insights['Performance 3 Year']}
5 Year: {insights['Performance 5 Year']}

Revenue Growth:
1 Year: {insights['Revenue Growth 1 Year']}
3 Year: {insights['Revenue Growth 3 Year']}


Current Financial Metrics:
- Price: {insights['Current Price']}
- P/E Ratio: {insights['P/E Ratio']}
- Dividend Yield: {insights['Dividend Yield']}
- Market Cap: {insights['Market Cap']}

Technical Indicators:
- RSI: {insights['RSI']}
- 52-Week Range: {insights['52 Week Low']} - {insights['52 Week High']}

Analyze the stock's historical performance, current position, potential risks, and investment outlook.
Use the following structure:

Stock Analysis for {ticker}

Market Position:
Analyze the company's position within its sector and industry.

Historical Performance Analysis:
Analyze 1, 3, and 5-year performance trends and what they indicate about the company's growth trajectory.

Revenue Growth Analysis:
Compare revenue growth across different time periods and what this suggests about the company's business model and market success.

Current Financial Analysis:
Evaluate current financial metrics and their implications for the company's health and valuation.

Technical Analysis:
Interpret current technical indicators and their implications for short-term trading.

Risk Assessment:
Identify key risks based on historical performance and current market conditions.

Investment Outlook:
Provide both short-term and long-term outlook based on historical trends and current metrics.

Recommendation:
Offer a clear investment recommendation supported by the analysis.

Keep the analysis concise but comprehensive, focusing on key insights from the historical data.
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)