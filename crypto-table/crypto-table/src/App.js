import React, { useState, useEffect } from 'react'
import './App.css';

function App() {
  const [data, setData] = useState([{}]);

  useEffect(() => {
    fetchCryptoData();

    const interval = setInterval(fetchCryptoData, 60000)

    return () => clearInterval(interval);
  }, []);

  const fetchCryptoData = async() => {
    try {
      const response = await fetch('/latest')
      const data = await response.json();
      setData(data);
    } catch (error) {
      console.error('Error fetching Cryptocurrency data:', error)
    }

  }

  return (
    <div>
      <h2>Latest Data on Top 10 Cryptocurrencies</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Symbol</th>
            <th>Rank</th>
            <th>USD Price </th>
            <th>% Change (Last 24H) </th>
            <th>Circulating Supply </th>
            <th>Last Updated At</th>
          </tr>
        </thead>
        <tbody>
          {(typeof data.data === 'undefined') ? (
            <tr>
              <td> Loading... </td>
            </tr>
          ): (
          data.data.map((crypto, index) => (
            <tr key={index} id={index+1} data-testid={`row-${index+1}`}>
              <td>{crypto.name}</td>
              <td>{crypto.symbol}</td>
              <td>{crypto.cmc_rank}</td>
              <td>{parseFloat(crypto.quote.USD.price).toFixed(2)}</td>
              <td>{parseFloat(crypto.quote.USD.percent_change_24h).toFixed(4)}</td>
              <td>{parseFloat(crypto.circulating_supply).toFixed(2)}</td>
              <td>{crypto.last_updated}</td>
            </tr>
          ))
          )
        }
        </tbody>
      </table>
    </div>
  );
}

export default App;
