# 🎬 CineStar Booking API

A FastAPI-based Movie Booking System that supports movie management, bookings, seat handling, and advanced features like filtering, sorting, and pagination.

---

## 🚀 Features

- Movie CRUD (Create, Read, Update, Delete)
- Booking system
- Seat hold, confirm, and release
- Search, filter, and sort APIs
- Pagination support
- Movie summary

---

## 🛠️ Tech Stack

- FastAPI
- Uvicorn
- Python 3.x

---

## 📂 Project Structure

project/
│── main.py
│
│── requirements.txt
│
│── README.md
|
│── Screenshots

---

## ⚙️ Installation

git clone https://github.com/your-username/cinestar-booking.git  
cd cinestar-booking  

python -m venv venv  
venv\Scripts\activate   # Windows  

pip install -r requirements.txt  

---

## ▶️ Run the Application

uvicorn main:app --reload

---

## 🌐 API Docs

Swagger UI → http://127.0.0.1:8000/docs  
ReDoc → http://127.0.0.1:8000/redoc  

---

## 📌 API Endpoints

### Movies
GET /movies  
POST /movies  
GET /movies/{movie_id}  
PUT /movies/{movie_id}  
DELETE /movies/{movie_id}  

### Bookings
GET /bookings  
POST /bookings  
GET /bookings/search  
GET /bookings/sort  
GET /bookings/page  

### Seat Management
GET /seat-hold  
POST /seat-hold  
POST /seat-confirm/{hold_id}  
DELETE /seat-release/{hold_id}  

### Advanced
GET /movies/search  
GET /movies/filter  
GET /movies/sort  
GET /movies/page  
GET /movies/browse  

---

## 📊 Example Request

{
  "customer_name": "Siva",
  "movie_id": 1,
  "seats": 2,
  "seat_type": "standard",
  "promo_code": "HELLOCINEMA"
}

---

## 📌 Future Improvements

- Database integration
- Authentication (JWT)
- Payment gateway
- Docker support

---

## 👨‍💻 Author

Siva Kishore

EOF
