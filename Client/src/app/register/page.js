// pages/register.js
'use client'

import React from 'react';
import Head from 'next/head';
import Link from 'next/link';

const Register = () => {
  return (
    <div className="register-container">
      <Head>
        <title>Register</title>
      </Head>
      <div className="register-form">
        <h2>Register</h2>
        <div className="form-group">
          <label htmlFor="empId">EmpId</label>
          <input type="text" id="empId" name="empId" placeholder="Enter EmpId" />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input type="password" id="password" name="password" placeholder="Enter Password" />
        </div>
        <button type="submit">Register</button>
        <Link href="/login">
          <button>Go back to Login</button>
        </Link>
      </div>
    </div>
  );
};

export default Register;
