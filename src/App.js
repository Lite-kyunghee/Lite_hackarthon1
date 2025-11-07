// App.js
// - 사용자는 로그인하면 JWT를 받아 로컬 스토리지에 보관
// - 과제 생성 폼에서 파일을 포함해 전송하면 Flask 백엔드의 /assignments 엔드포인트로 전송


import React, { useState } from 'react';
import axios from 'axios';


function App() {
// 로컬 상태: 이메일, 비밀번호, 로그인 토큰
const [email, setEmail] = useState('');
const [password, setPassword] = useState('');
const [token, setToken] = useState(localStorage.getItem('token'));
const [title, setTitle] = useState('');
const [file, setFile] = useState(null);


const apiBase = 'http://localhost:5000/api';


// 로그인 함수: 백엔드 /auth