# WAF
This project is a basic Web Application Firewall (WAF) tool designed to enhance the security of web applications by protecting against common vulnerabilities like SQL Injection, Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), and more.


## Installation

1. Clone the repository:

```bash
  git clone https://github.com/Sudo-Sakib/WAF.git
  cd WAF
```
2. Install requirements:

```bash
  pip install -r requirements.txt
```

3. Set up the database:
First uncomment the database initialization lines in setup.db.py
```bash
  python setup.db.py
```
4. Configure the secret key:
Open the config.py file and set your custom secret key for the application
```bash
  SECRET_KEY = 'your-secure-random-key'
```
5. Start the application:
```bash
  python run.py
```




