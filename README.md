<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Real-Time Alert System</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      padding: 20px;
      background: #fdfdfd;
      color: #333;
    }
    h1 {
      text-align: center;
      color: #0066cc;
    }
    .badge-container {
      text-align: center;
      margin-bottom: 20px;
    }
    .badge-container img {
      margin: 0 5px;
    }
    .gif-center {
      display: flex;
      justify-content: center;
      margin: 20px 0;
    }
    pre {
      background: #eee;
      padding: 10px;
      border-radius: 5px;
      overflow-x: auto;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }
    table, th, td {
      border: 1px solid #bbb;
    }
    th, td {
      padding: 10px;
      text-align: left;
    }
  </style>
</head>
<body>

<h1>🚀 Real-Time Alert System with WebSockets & MySQL</h1>

<div class="gif-center">
  <img src="https://media.giphy.com/media/HhTXt43pk1I1W/giphy.gif" alt="Alert" width="100">
</div>

<div class="badge-container">
  <img src="https://img.shields.io/badge/Python-3.7+-blue?logo=python" />
  <img src="https://img.shields.io/badge/MySQL-Server-005C84?logo=mysql" />
  <img src="https://img.shields.io/badge/WebSocket-Enabled-green" />
</div>

<h2>📦 Requirements</h2>
<ul>
  <li>Python 3.7+</li>
  <li>MySQL Server</li>
</ul>

<h2>🐍 Python Libraries</h2>
<p>The following libraries are required:</p>
<table>
  <tr><th>Library</th><th>Purpose</th></tr>
  <tr><td>asyncio</td><td>For asynchronous operations</td></tr>
  <tr><td>websockets</td><td>WebSocket server functionality</td></tr>
  <tr><td>pymysql</td><td>MySQL database interaction</td></tr>
  <tr><td>json</td><td>JSON data encoding/decoding</td></tr>
  <tr><td>datetime</td><td>Datetime handling and formatting</td></tr>
</table>

<h3>📥 Install dependencies:</h3>
<pre><code>pip install -r requirements.txt</code></pre>

<h2>⚙️ Setup Instructions</h2>
<ol>
  <li>Install MySQL Server on your system.</li>
  <li>Create a new database and a user with appropriate permissions.</li>
  <li>Run the script using Python:
    <pre><code>python API.py</code></pre>
  </li>
  <li>Open the HTML file with Live Server in your browser.</li>
  <li>Add an entry to the database — watch alerts update in real time!</li>
</ol>

<div class="gif-center">
  <img src="https://media.giphy.com/media/l3q2K5jinAlChoCLS/giphy.gif" alt="Live Demo" width="600">
</div>

<h2>🧠 Highlights</h2>
<ul>
  <li>💡 Real-time alerts without page refresh</li>
  <li>🔐 Secure DB connection with PyMySQL</li>
  <li>📦 Modular design for easy expansion</li>
</ul>

<h2>📬 Feedback & Contributions</h2>
<p>Have ideas or improvements? Fork this repo or open an issue!</p>

</body>
</html>
