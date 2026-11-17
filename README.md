# SMS Gateway Web Application (TextBee Integration)

**IT 120 – Integrative Programming and Technologies**  
**Group Laboratory / Assignment: Build a Django Application for Sending SMS**

---

## 1. Project Title & Description

**Project Title:** Django SMS Gateway Application  
**Description:**  
This project is a web-based SMS gateway messaging system built with Python and the Django framework. The application allows users to compose and dispatch SMS messages to recipient phone numbers using an external SMS provider API (TextBee Gateway). It incorporates client- and server-side validation, secure environment-based credential handling, detailed error trapping, and an interactive dashboard tracking previous dispatch attempts alongside a live character counter.

---

## 2. Group Members and Assigned Responsibilities

*(Please update the placeholders below with your group's details)*

| Member Name | Role & Assigned Responsibilities |
| :--- | :--- |
| **Joshua Marvin D. Tabania** | **Lead Developer / Application Architecture:** Django project setup, URL routing, view logic, and overall system design. |
| **Jounes S. Quezzagan** | **Frontend & UI/UX Developer:** UI design with Bootstrap 5, form creation, client/server input validation, user feedback messages. |
| **Michael D. Tiposo** | **Integration, Testing & Documentation:** SMS API gateway integration, error handling, automated unit testing, and documentation. |

---

## 3. Main Features

- **SMS Composition Interface:** User-friendly form with a Philippine mobile prefix (+63), 10-digit input constraint, multi-line message composition, and submission loading state.
- **Live Smartphone Message Preview (Additional Feature):** Real-time interactive handset mockup showing how the SMS looks in a chat bubble as the user types.
- **Real-Time Character & Segment Counter (Additional Feature):** Live counter tracking typed characters alongside carrier segment calculation (e.g., `45 / 160 characters • 1 SMS part`).
- **Quick Transmission Statistics Summary:** Dynamic metrics dashboard displaying total attempts, successful dispatches, and failed dispatches.
- **Robust Input Validation:**
  - Prevents empty phone numbers or empty messages.
  - Sanitizes and enforces Philippine mobile format (e.g., 10 digits after +63: `9123456789`).
  - Preserves entered form values when validation errors occur.
- **Comprehensive Error Handling:**
  - Catches missing or invalid API keys.
  - Handles provider rejections (HTTP 4xx/5xx).
  - Handles network timeouts and connectivity failures.
- **Interactive Sending Attempts Dashboard (Additional Feature):**
  - Displays the last 10 sending attempts.
  - Details timestamp, recipient number, message snippet, and status badge (`Success`, `Failed (Rejected)`, `Failed (Network)`).
- **Distinction Between Submission & Delivery:** Confirms successful API submission to the gateway without falsely claiming confirmed cellular delivery.

---

## 4. Technologies & Dependencies Used

- **Programming Language:** Python 3.13+
- **Backend Framework:** Django 6.1.2
- **Frontend Framework:** HTML5, CSS3, Bootstrap 5.3.0
- **HTTP Client:** `requests` 2.34.2
- **Environment Management:** `python-dotenv` 1.2.4
- **Database:** SQLite3
- **SMS Gateway Provider:** TextBee Gateway API (`https://api.textbee.dev`)

---

## 5. Installation and Setup Instructions

### Prerequisites
- Python 3.10+ installed on your computer.
- Git installed.

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd SmsProjectTextBee
   ```

2. **Create and activate a virtual environment:**
   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

---

## 6. Instructions for Configuring the SMS Provider

1. **Create an account on TextBee:**
   - Register at [https://textbee.dev](https://textbee.dev).
   - Follow the instructions to configure your Android SMS Gateway device and obtain your **API Key**.

2. **Set up Environment Variables:**
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
     *(On Windows Command Prompt / PowerShell, use `copy .env.example .env`)*
   - Open `.env` and fill in your actual credentials:
     ```env
     TEXTBEE_API_KEY=your_actual_textbee_api_key_here
     SECRET_KEY=your_optional_django_secret_key
     ```
   - **Important:** Never commit the `.env` file to GitHub. It is ignored by `.gitignore`.

---

## 7. Instructions for Running the Application

1. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

2. **Open the application:**
   - Open your web browser and navigate to:  
     `http://127.0.0.1:8000/`

3. **Send a Test Message:**
   - Enter a 10-digit mobile number (e.g., `9123456789`).
   - Type your test message.
   - Click **Send SMS**.

---

## 8. Testing Procedures and Results

### Automated Unit Tests
The project includes a suite of automated unit tests covering all required test cases. Run the tests using:
```bash
python manage.py test
```

### Test Case Matrix & Results

| # | Test Case | Action / Input | Expected Result | Result |
|---|:---|:---|:---|:---:|
| 1 | **Page Load** | Access root URL (`/`) | Renders SMS composition page with form fields | **Passed** |
| 2 | **Empty Phone** | Submit with blank phone | Rejects submission; shows validation error message | **Passed** |
| 3 | **Empty Message** | Submit with blank message | Rejects submission; shows validation error message | **Passed** |
| 4 | **Invalid Phone** | Submit non-numeric or malformed phone (e.g. `123`) | Rejects submission; informs user of invalid format | **Passed** |
| 5 | **Missing API Key** | Send SMS without `TEXTBEE_API_KEY` in environment | Catches error safely without crashing; displays config error | **Passed** |
| 6 | **Gateway Rejection** | API returns 401/403/400 (Bad or expired key) | Logs `Failed (Rejected)`; shows gateway response details | **Passed** |
| 7 | **Network Error** | API unreachable or timeout | Logs `Failed (Network)`; informs user of connection error | **Passed** |
| 8 | **Successful Dispatch**| Submit valid number and message with active key | Logs `Success` in DB; redirects with confirmation message | **Passed** |

---

## 9. Known Limitations

- **Gateway Device Dependency:** Delivery relies on the connected Android gateway device remaining online with active cellular network connectivity and SMS credits.
- **Philippine Number Preset:** The application is formatted by default with the Philippine country code (`+63`). Dispatching to international numbers requires adjusting the prefix in `views.py` and `index.html`.
- **Delivery Confirmation:** The application confirms that the message was accepted by the gateway (`Message successfully sent to gateway!`), but full cellular delivery to the handset is dependent on the carrier network.
