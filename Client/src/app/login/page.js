// // pages/login.js
'use client'

import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import axios from 'axios';
import { useRouter } from 'next/navigation'

const Login = () => {
  const [empId, setEmpId] = useState('');
  const [password, setPassword] = useState('');
  const { push } = useRouter();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/login', {
        empid: empId,
        password: password
      });
      console.log(response)
      if (response.status === 200) {
        sessionStorage.setItem('empId', empId); // Save empId in session storage
        push('/schedule'); // Redirect to '/schedule'
      } else {
        // Handle login error
        console.error(response.data.error);
      }
    } catch (error) {
      console.error('Error during login:', error);
    }
  };

  return (
    <div className="login-container">
      <Head>
        <title>Login</title>
      </Head>
      <div className="login-form">
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="empId">EmpId</label>
            <input
              type="text"
              id="empId"
              name="empId"
              placeholder="Enter EmpId"
              value={empId}
              onChange={(e) => setEmpId(e.target.value)}
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
          <button class="buttonLR" type="submit">Login</button>
        </form>
        <Link href="/register">
          <button class="buttonLR">Register</button>
        </Link>
      </div>
    </div>
  );
};

export default Login;
