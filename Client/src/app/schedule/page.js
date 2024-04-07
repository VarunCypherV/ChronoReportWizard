'use client'
// 'use client'
import dynamic from 'next/dynamic';
import { useState, useEffect } from 'react'; // Importing useEffect hook
import axios from 'axios'; // Import axios for making HTTP requests

const initialRequests = [
  { id: 1, reportName: 'Report 1', datetime: '10:00 AM', status: 'Not yet' },
  { id: 2, reportName: 'Report 2', datetime: '11:00 AM', status: 'Received' },
];

const SchedulePage = () => {
  const [reportName, setReportName] = useState('');
  const [datetime, setDateTime] = useState('');
  const [requests, setRequests] = useState(initialRequests);
  const [currentTime, setCurrentTime] = useState('');

  useEffect(() => {
    const intervalId = setInterval(() => {
      const now = new Date();
      setCurrentTime(now.toLocaleTimeString());
    }, 1000);

    return () => clearInterval(intervalId);
  }, []);

  const handleRequestSubmit = () => {
    // Send POST request to server
    let empid = "12";
    let email = "coolvarun304@gmail.com";
    console.log(datetime); // Logging the datetime value
    
    // Extract date components
    const date = new Date(datetime);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Month starts from 0
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    
    // Format the datetime string
    const formattedDatetime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    
    axios
      .post("http://127.0.0.1:5000/schedule_report", {
        empid,
        reportName,
        email,
        datetime: formattedDatetime, // Use the formatted datetime
      })
      .then((response) => {
        console.log(response.data); // Logging the response from the server
        // Update UI with the new request
        const newRequest = {
          id: requests.length + 1,
          reportName,
          datetime: formattedDatetime, // Use the formatted datetime
          status: "Not yet",
        };
        setRequests([...requests, newRequest]);
        setReportName("");
        setDateTime("");
      })
      .catch((error) => {
        console.error("Error:", error); // Logging errors, if any
      });
  };
  
  
  
  
  return (
    <div className="container">
      <div className="form">
        <select
          value={reportName}
          onChange={(e) => setReportName(e.target.value)}
          className="select"
        >
          <option value="">Select Report</option>
          <option value="Report 1">Report 1</option>
          <option value="Report 2">Report 2</option>
        </select>
        <input
          type="datetime-local"
          value={datetime}
          onChange={(e) => setDateTime(e.target.value)}
          className="input"
        />
        <button onClick={handleRequestSubmit} className="button">
          Request
        </button>
        <div className="current-time">{currentTime}</div>
      </div>

      <table className="table">
        <thead>
          <tr>
            <th>Sno</th>
            <th>Request Id</th>
            <th>Report Name</th>
            <th>Date and Time</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {requests.map((request, index) => (
            <tr key={request.id}>
              <td>{index + 1}</td>
              <td>{request.id}</td>
              <td>{request.reportName}</td>
              <td>{request.datetime}</td>
              <td
                style={{ color: request.status === 'Received' ? 'green' : 'red' }}
                className="status"
              >
                {request.status}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default dynamic(() => Promise.resolve(SchedulePage), { ssr: false });
