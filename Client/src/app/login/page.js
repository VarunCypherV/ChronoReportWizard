// pages/login.js
'use client'

import React from 'react';
import Head from 'next/head';
import Link from 'next/link';

const Login = () => {
  return (
    <div className="login-container">
      <Head>
        <title>Login</title>
      </Head>
      <div className="login-form">
        <h2>Login</h2>
        <div className="form-group">
          <label htmlFor="empId">EmpId</label>
          <input type="text" id="empId" name="empId" placeholder="Enter EmpId" />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input type="password" id="password" name="password" placeholder="Enter Password" />
        </div>
        <button type="submit">Login</button>
        <Link href="/register">
          <button>Register</button>
        </Link>
      </div>
    </div>
  );
};

export default Login;
