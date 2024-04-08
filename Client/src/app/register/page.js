'use client'

import React, { useState } from 'react';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation'
import Head from 'next/head';
import Link from 'next/link';
import axios from 'axios'; // Import axios for making HTTP requests
import { redirect } from 'next/navigation';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { push } = useRouter();
  const handleRegister = async () => {
    try {
      
      const response = await axios.post('http://127.0.0.1:5000/register', { email, password });
      alert(`LoginIn With Your EmpID : ${response.data.empid}`) // You can handle the response as needed
      push('/login');
    } catch (error) {
      console.error("Error fetching data:", error);
      // Handle error, show error message
    }
  };
  

  return (
    <div className="register-container">
      <Head>
        <title>Register</title>
      </Head>
      <div className="register-form">
        <h2>Register</h2>
        <div className="form-group">
          <input
            type="text"
            id="email"
            name="email"
            placeholder="Enter Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            placeholder="Enter Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="button" onClick={handleRegister}>Register</button>
        <Link href="/login">
          <button>Go back to Login</button>
        </Link>
      </div>
    </div>
  );
};

export default Register;
