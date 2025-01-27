// import React, { useState, useEffect } from 'react';
// import './App.css';

// const constructionStocks = [
//   { ticker: 'IBP', name: 'Installed Building Products, Inc.' },
//   { ticker: 'SKY', name: 'Skyline Champion Corporation' },
//   { ticker: 'KBH', name: 'KB Home' },
//   { ticker: 'CVCO', name: 'Cavco Industries, Inc.' },
//   { ticker: 'GRBK', name: 'Green Brick Partners, Inc.' },
//   { ticker: 'TOL', name: 'Toll Brothers, Inc.' },
//   { ticker: 'DHI', name: 'D.R. Horton, Inc.' },
//   { ticker: 'LEN', name: 'Lennar Corporation' },
//   { ticker: 'PHM', name: 'PulteGroup, Inc.' },
//   { ticker: 'NVR', name: 'NVR, Inc.' },
//   { ticker: 'BN', name: 'Brookfield Corp' }
// ];

// function App() {
//   const [selectedStock, setSelectedStock] = useState(null);
//   const [stockData, setStockData] = useState(null);
//   const [isLoading, setIsLoading] = useState(false);
//   const [animationStep, setAnimationStep] = useState(0);
//   const [showStockSelector, setShowStockSelector] = useState(false); // Track visibility of stock selector

//   useEffect(() => {
//     const animationInterval = setInterval(() => {
//       setAnimationStep((prev) => (prev < 3 ? prev + 1 : 3));
//     }, 1000);
//     return () => clearInterval(animationInterval);
//   }, []);

//   const fetchStockData = async (ticker) => {
//     setIsLoading(true);
//     try {
//       const response = await fetch('http://127.0.0.1:5000/api/stock-analysis', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ ticker }),
//       });

//       if (!response.ok) {
//         throw new Error(`Failed to fetch: ${response.statusText}`);
//       }

//       const data = await response.json();

//       if (data.error) {
//         console.error('Error in backend:', data.error);
//       } else {
//         setStockData(data);
//       }
//     } catch (error) {
//       console.error('Error fetching stock data:', error);
//     }
//     setIsLoading(false);
//   };

//   const handleStockSelect = (stock) => {
//     setSelectedStock(stock);
//     fetchStockData(stock.ticker);
//   };

//   const handleNextClick = () => {
//     setShowStockSelector(true); // Show the stock selection after "Next" click
//   };

//   return (
//     <div className="app">
//       {animationStep < 3 ? (
//         <div className="animation-container">
//           {animationStep === 0 && <h2 className="fade-in">Hi!</h2>}
//           {animationStep === 1 && <h2 className="fade-in">Welcome</h2>}
//           {animationStep === 2 && (
//             <h2 className="fade-in">To Buildix</h2>
//           )}
//         </div>
//       ) : (
//         <div>
//           {/* Description and Next Button */}
//           {!showStockSelector && (
//             <div className="description-container">
//               <div className="description-text">
//                 <p>Analyze construction stocks with AI-powered insights.</p>
//               </div>
//               <div
//                 className="next-button"
//                 onClick={handleNextClick}
//               >
//                 &rarr; {/* Right arrow symbol */}
//               </div>
//             </div>
//           )}
//         </div>
//       )}

//       {showStockSelector && (
//         <>
//           <div className="stock-selector">
//             <select
//               onChange={(e) => {
//                 const selected = constructionStocks.find(
//                   (s) => s.ticker === e.target.value
//                 );
//                 handleStockSelect(selected);
//               }}
//             >
//               <option value="">Select a Stock</option>
//               {constructionStocks.map((stock) => (
//                 <option key={stock.ticker} value={stock.ticker}>
//                   {stock.name} ({stock.ticker})
//                 </option>
//               ))}
//             </select>
//           </div>

//           {isLoading && <div className="loading">Loading...</div>}

//           {selectedStock && stockData && (
//             <div className="stock-details">
//               <h2>
//                 {selectedStock.name} ({selectedStock.ticker})
//               </h2>

//               <div className="stock-info">
//                 <h3>Metrics:</h3>
//                 <ul>
//                   {Object.entries(stockData.metrics || {}).map(([key, value]) => (
//                     <li key={key}>
//                       {key}: {value}
//                     </li>
//                   ))}
//                 </ul>
//               </div>

//               <div className="ai-analysis">
//                 <h3>AI Analysis:</h3>
//                 <p>{stockData.aiAnalysis || 'No analysis available.'}</p>
//               </div>
//             </div>
//           )}
//         </>
//       )}
//     </div>
//   );
// }

// export default App;

import React, { useState, useEffect } from 'react';
import './App.css';

const constructionStocks = [
  { ticker: 'IBP', name: 'Installed Building Products, Inc.' },
  { ticker: 'SKY', name: 'Skyline Champion Corporation' },
  { ticker: 'KBH', name: 'KB Home' },
  { ticker: 'CVCO', name: 'Cavco Industries, Inc.' },
  { ticker: 'GRBK', name: 'Green Brick Partners, Inc.' },
  { ticker: 'TOL', name: 'Toll Brothers, Inc.' },
  { ticker: 'DHI', name: 'D.R. Horton, Inc.' },
  { ticker: 'LEN', name: 'Lennar Corporation' },
  { ticker: 'PHM', name: 'PulteGroup, Inc.' },
  { ticker: 'NVR', name: 'NVR, Inc.' },
  { ticker: 'BN', name: 'Brookfield Corp' }
];

function App() {
  const [selectedStock, setSelectedStock] = useState(null);
  const [stockData, setStockData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [animationStep, setAnimationStep] = useState(0);
  const [showStockSelector, setShowStockSelector] = useState(false); // Track visibility of stock selector

  useEffect(() => {
    const animationInterval = setInterval(() => {
      setAnimationStep((prev) => (prev < 3 ? prev + 1 : 3));
    }, 1000);
    return () => clearInterval(animationInterval);
  }, []);

  const fetchStockData = async (ticker) => {
    setIsLoading(true);
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
        console.error('Error in backend:', data.error);
      } else {
        setStockData(data);
      }
    } catch (error) {
      console.error('Error fetching stock data:', error);
    }
    setIsLoading(false);
  };

  const handleStockSelect = (stock) => {
    setSelectedStock(stock);
    fetchStockData(stock.ticker);
  };

  const handleNextClick = () => {
    setShowStockSelector(true); // Show the stock selection after "Next" click
  };

  const formatResponse = (responseText) => {
    // Remove the double stars (**) and split the response into sections
    const formattedText = responseText
      .replace(/\*\*/g, '')
      .split('\n')
      .filter((line) => line.trim() !== '') // Remove empty lines
      .map((line, index) => {
        // If the line contains a colon, treat it as a heading
        if (line.includes(':')) {
          return <h4 key={index}>{line}</h4>; // Heading style
        }
        return <li key={index}>{line}</li>; // Bullet point for content
      });
  
    return <div>{formattedText}</div>;
  };
  
  return (
    <div className="app">
      {animationStep < 3 ? (
        <div className="animation-container">
          {animationStep === 0 && <h2 className="fade-in">Hi!</h2>}
          {animationStep === 1 && <h2 className="fade-in">Welcome</h2>}
          {animationStep === 2 && (
            <h2 className="fade-in">To Buildix</h2>
          )}
        </div>
      ) : (
        <div>
          {/* Description and Next Button */}
          {!showStockSelector && (
            <div className="description-container">
              <div className="description-text">
                <p>Analyze construction stocks with AI-powered insights.</p>
              </div>
              <div
                className="next-button"
                onClick={handleNextClick}
              >
                &rarr; {/* Right arrow symbol */}
              </div>
            </div>
          )}
        </div>
      )}

      {showStockSelector && (
        <>
          <div className="stock-selector">
            <select
              onChange={(e) => {
                const selected = constructionStocks.find(
                  (s) => s.ticker === e.target.value
                );
                handleStockSelect(selected);
              }}
            >
              <option value="">Select a Stock</option>
              {constructionStocks.map((stock) => (
                <option key={stock.ticker} value={stock.ticker}>
                  {stock.name} ({stock.ticker})
                </option>
              ))}
            </select>
          </div>

          {isLoading && <div className="loading">Loading...</div>}

          {selectedStock && stockData && (
            <div className="stock-details">
              <h2>
                {selectedStock.name} ({selectedStock.ticker})
              </h2>

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
        </>
      )}
    </div>
  );
}

export default App;
