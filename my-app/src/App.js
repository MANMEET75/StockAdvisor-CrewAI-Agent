// src/App.js

import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css'; // Import CSS file for styling

function App() {
  const [companyName, setCompanyName] = useState('');
  const [response, setResponse] = useState('');
  const [logoUrl, setLogoUrl] = useState('');
  const [loading, setLoading] = useState(false); // Add loading state

  const handleSubmit = async () => {
    setLoading(true); // Set loading state to true while fetching data

    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ CompanyName: companyName })
    };
    const response = await fetch('http://localhost:8080/AnalyzeStock/', requestOptions);
    const data = await response.json();
    setResponse(data.result);
    setLoading(false); // Set loading state back to false after data is fetched

    fetchCompanyLogo(companyName); // Fetch company logo
  };

  const fetchCompanyLogo = async (companyName) => {
    try {
      const response = await fetch(`https://autocomplete.clearbit.com/v1/companies/suggest?query=${companyName}`);
      const data = await response.json();
      if (data.length > 0 && data[0].logo) {
        setLogoUrl(data[0].logo);
      } else {
        setLogoUrl(''); // Set empty URL if logo is not available
      }
    } catch (error) {
      console.error('Error fetching company logo:', error);
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>Stock Analyzer</h1>
      </header>
      <div className="content">
        <div className="input-container">
          <input
            type="text"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            placeholder="Enter Company Name"
            className="input-field"
          />
          <button onClick={handleSubmit} disabled={loading} className="analyze-button">Analyze</button>
        </div>
        {loading && <div className="loading">Loading...</div>} {/* Show loading indicator */}
        {logoUrl && (
          <div className="company-logo">
            <img src={logoUrl} alt="Company Logo" />
          </div>
        )}
        {response && !loading && (
          <div className="result">
            <ReactMarkdown>{response}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
