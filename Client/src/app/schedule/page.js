'use client'
// 'use client'
import dynamic from 'next/dynamic';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation'

const SchedulePage = () => {
  const [reportName, setReportName] = useState('');
  const [datetime, setDateTime] = useState('');
  const [requests, setRequests] = useState();
  const [currentTime, setCurrentTime] = useState('');
  const [empid, setEmpId] = useState("");
  const [email, setEmail] = useState("");
  const [rerender, setRerender] = useState(false); // State variable for triggering rerender
  const { push } = useRouter();
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedEmpId = window.sessionStorage.getItem('empId');
      setEmpId(storedEmpId);
      console.log(storedEmpId); // Log the retrieved empId
    }
  }, [rerender]); // Empty dependency array to run this effect only once
  
  useEffect(() => {
    if (empid) { // Ensure empid is truthy before making the axios call
      axios.get(`http://127.0.0.1:5000/get_records/${empid}`)
        .then(response => {
          setRequests(response.data.records);
          setEmail(response.data.email);
        })
        .catch(error => {
          console.error("Error fetching data:", error);
        });
    }
  
    const intervalId = setInterval(() => {
      const now = new Date();
      setCurrentTime(now.toLocaleTimeString());
    }, 1000);
  
    return () => {
      clearInterval(intervalId);
    };
  }, [empid,rerender]); // Run this effect whenever empid changes
  
  // Add rerender to dependencies so that useEffect runs again when rerender state changes

  const handleRequestSubmit = () => {
    const date = new Date(datetime);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Month starts from 0
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    const formattedDatetime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;

    axios
      .post("http://127.0.0.1:5000/schedule_report", {
        empid,
        reportName,
        email,
        datetime: formattedDatetime, // Use the formatted datetime
      })
      .then((response) => {
        console.log(response.data)
        setReportName("");
        setDateTime("");
        setRerender(prev => !prev); // Toggle the rerender state
      })
      .catch((error) => {
        console.error("Error:", error); // Logging errors, if any
      });
  };

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      window.sessionStorage.removeItem('empId');
      setEmpId(""); // Clear empid state
      setRequests(null); // Clear requests state
      setEmail(""); // Clear email state
      setRerender(prev => !prev); // Trigger rerender to reset the component
      push("/login")
    }
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
        <button onClick={handleLogout} className="button">Logout</button>
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
          {requests && requests.map((request, index) => (
            <tr key={index}>
              <td>{index + 1}</td>
              <td>{request.requestid}</td>
              <td>{request.reportname}</td>
              <td>{request.needtime}</td>
              <td>{request.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default dynamic(() => Promise.resolve(SchedulePage), { ssr: false });
