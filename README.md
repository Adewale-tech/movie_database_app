# Movie Database App 🎬

A sophisticated movie discovery platform built with **Django** and **TailwindCSS**. This application allows users to browse trending movies, search for their favorites, view detailed cast and crew information, and manage a personal watchlist.

![Project Banner](https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=2525&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)
*(Replace with actual screenshot of your app)*

## 🚀 Features

### Core Functionality
-   **🔥 Trending Movies**: Discover the latest and most popular movies on the home page.
-   **🔍 Real-time Search**: Instantly find movies using the powerful TMDB API integration.
-   **📄 Detailed Insights**: View comprehensive movie details, including plot summaries, release dates, ratings, and top cast members.
-   **📱 Responsive Design**: A seamless experience across desktop, tablet, and mobile devices.

### Advanced Features (User Accounts)
-   **🔐 Secure Authentication**: User registration and login system.
-   **⭐ Personal Watchlist**: Logged-in users can add movies to their watchlist to save for later.
-   **💾 Persistent Data**: User data is securely stored in a SQL database.

## 🛠️ Tech Stack

-   **Backend**: Python, Django 5
-   **Frontend**: Django Templates, TailwindCSS (via CDN), Lucide Icons
-   **API**: The Movie Database (TMDB) API
-   **Database**: SQLite (Dev), PostgreSQL (Production ready)

## 📦 Installation & Setup

Follow these steps to run the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/Adewale-tech/movie_database_app.git
cd movie_database_app
```

### 2. Create a Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Note: If requirements.txt is missing, install manually: `pip install django requests python-dotenv`)*

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add your TMDB API Key:
```env
TMDB_API_KEY=your_api_key_here
SECRET_KEY=your_django_secret_key
DEBUG=True
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Start the Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your browser.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Developed by [Adewale-tech](https://github.com/Adewale-tech)**