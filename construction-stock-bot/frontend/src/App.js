import React, { useState, useEffect } from 'react';
import './App.css';
import { X } from 'lucide-react';
import logoWhite from './logo-white.png';

function App() {
  const [selectedStock, setSelectedStock] = useState(null);
  const [stockData, setStockData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [animationStep, setAnimationStep] = useState(0);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);

  // Animation effect for initial load
  useEffect(() => {
    const animationInterval = setInterval(() => {
      setAnimationStep((prev) => (prev < 3 ? prev + 1 : 3));
    }, 1000);
    return () => clearInterval(animationInterval);
  }, []);

  // Search functionality
  const searchStocks = async (query) => {
    if (!query || query.length < 2) {
      setSearchResults([]);
      setIsSearching(false);
      return;
    }

    setIsSearching(true);
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/search-stocks?query=${encodeURIComponent(query)}`
      );
      if (!response.ok) {
        throw new Error('Search failed');
      }
      const data = await response.json();
      
      // Filter out duplicates based on ticker
      const filteredData = data.filter((stock, index, self) =>
        index === self.findIndex((s) => s.ticker === stock.ticker)
      );
      
      setSearchResults(filteredData);
    } catch (error) {
      console.error('Error searching stocks:', error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  // Debounced search effect
  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchQuery.length >= 2) {
        searchStocks(searchQuery);
      } else {
        setSearchResults([]);
        setIsSearching(false);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  // Fetch stock data
  const fetchStockData = async (ticker) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('http://127.0.0.1:5000/api/stock-analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ticker }),
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch: ${response.statusText}`);
      }

      const data = await response.json();
      if (data.error) {
        setError(data.error);
      } else {
        setStockData(data);
      }
    } catch (error) {
      setError(error.message);
      console.error('Error fetching stock data:', error);
    }
    setIsLoading(false);
  };

  // Handle stock selection
  const handleStockSelect = (stock) => {
    setSelectedStock(stock);
    fetchStockData(stock.ticker);
    setSearchQuery('');
    setSearchResults([]);
  };

  // Handle closing stock view
  const handleClose = () => {
    setSelectedStock(null);
    setStockData(null);
    setSearchQuery('');
    setSearchResults([]);
  };

  // Format response text
  const formatResponse = (responseText) => {
    const formattedText = responseText
      .replace(/\*\*/g, '')
      .split('\n')
      .filter((line) => line.trim() !== '')
      .map((line, index) => {
        if (line.includes(':')) {
          return <h4 key={index}>{line}</h4>;
        }
        return <li key={index}>{line}</li>;
      });
  
    return <div>{formattedText}</div>;
  };
  
  return (
    <div className="app">
      {animationStep < 3 ? (
        <div className="animation-container">
          {animationStep === 0 && <h2 className="fade-in">Hi!</h2>}
          {animationStep === 1 && <h2 className="fade-in">Welcome</h2>}
          {animationStep === 2 && <h2 className="fade-in">To Briqko</h2>}
        </div>
      ) : (
        <div className="main-container">
          {!selectedStock ? (
            <div className="search-view">
              <div className="logo-container">
                <img src={logoWhite} alt="Briako Logo" className="logo" />
              </div>
              <div className="search-container">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search for any stock..."
                  className="search-input"
                />
                {isSearching && searchQuery.length >= 2 && (
                  <div className="searching-message">Searching...</div>
                )}
                {searchQuery.length >= 2 && searchResults.length > 0 && (
                  <div className="search-results">
                    {searchResults.map((stock) => (
                      <div
                        key={stock.ticker}
                        className="search-result-item"
                        onClick={() => handleStockSelect(stock)}
                      >
                        <span className="stock-symbol">{stock.ticker}</span>
                        <span className="stock-name">{stock.name}</span>
                        {stock.exchange && (
                          <span className="stock-exchange">{stock.exchange}</span>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="insights-view">
              <div className="header">
                <img src={logoWhite} alt="Briako Logo" className="logo-small" />
                <button className="close-button" onClick={handleClose}>
                  <X size={24} />
                </button>
              </div>
              
              {isLoading && <div className="loading">Loading...</div>}
              {error && <div className="error-message">{error}</div>}

              {stockData && !error && (
                <div className="stock-details">
                  <h2>{selectedStock.name} ({selectedStock.ticker})</h2>
                  
                  <div className="stock-info">
                    <h3>Metrics:</h3>
                    <ul>
                      {Object.entries(stockData.metrics || {}).map(([key, value]) => (
                        <li key={key}>
                          {key}: {value}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="ai-analysis">
                    <h3>AI Analysis:</h3>
                    <div>
                      {formatResponse(stockData.aiAnalysis || 'No analysis available.')}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;