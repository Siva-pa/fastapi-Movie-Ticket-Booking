from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# -------------------------
# DATA
# -------------------------
movies = [
    {
        "id": 1,
        "title": "Avengers",
        "genre": "Action",
        "language": "English",
        "duration_mins": 180,
        "ticket_price": 250,
        "seats_available": 50
    },
    {
        "id": 2,
        "title": "RRR",
        "genre": "Action",
        "language": "Telugu",
        "duration_mins": 170,
        "ticket_price": 200,
        "seats_available": 40
    },
    {
        "id": 3,
        "title": "Inception",
        "genre": "Drama",
        "language": "English",
        "duration_mins": 150,
        "ticket_price": 220,
        "seats_available": 30
    },
    {
        "id": 4,
        "title": "Joker",
        "genre": "Drama",
        "language": "English",
        "duration_mins": 140,
        "ticket_price": 180,
        "seats_available": 35
    },
    {
        "id": 5,
        "title": "Hangover",
        "genre": "Comedy",
        "language": "English",
        "duration_mins": 120,
        "ticket_price": 150,
        "seats_available": 25
    },
    {
        "id": 6,
        "title": "Conjuring",
        "genre": "Horror",
        "language": "English",
        "duration_mins": 130,
        "ticket_price": 170,
        "seats_available": 20
    }
]

bookings = []
booking_counter = 1

# -------------------------
# Q1
# -------------------------
@app.get("/")
def home():
    return {"message": "Welcome to CineStar Booking"}

# -------------------------
# Q2
# -------------------------
@app.get("/movies")
def get_movies():
    total_seats = sum(movie["seats_available"] for movie in movies)
    return {
        "total_movies": len(movies),
        "total_seats_available": total_seats,
        "movies": movies
    }

# -------------------------
# Q3
# -------------------------
@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")

# -------------------------
# Q4
# -------------------------
@app.get("/bookings")
def get_bookings():
    total_revenue = sum(b["total_cost"] for b in bookings)
    return {
        "total_bookings": len(bookings),
        "total_revenue": total_revenue,
        "bookings": bookings
    }

# -------------------------
# Q5
# -------------------------
@app.get("/movies/summary")
def movies_summary():
    prices = [m["ticket_price"] for m in movies]
    total_seats = sum(m["seats_available"] for m in movies)

    genre_count = {}
    for m in movies:
        genre_count[m["genre"]] = genre_count.get(m["genre"], 0) + 1

    return {
        "total_movies": len(movies),
        "most_expensive": max(prices),
        "cheapest": min(prices),
        "total_seats": total_seats,
        "movies_by_genre": genre_count
    }

# -------------------------
# Q6
# -------------------------
class BookingRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    movie_id: int = Field(..., gt=0)
    seats: int = Field(..., gt=0, le=10)
    phone: str = Field(..., min_length=10)
    seat_type: str = "standard"
    promo_code: str = ""

# -------------------------
# Q7
# -------------------------
def find_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return None


def calculate_ticket_cost(price, seats, seat_type, promo_code):
    multiplier = 1

    if seat_type == "premium":
        multiplier = 1.5
    elif seat_type == "recliner":
        multiplier = 2

    original_cost = price * seats * multiplier

    discount = 0
    if promo_code == "SAVE10":
        discount = 0.1
    elif promo_code == "SAVE20":
        discount = 0.2

    final_cost = original_cost * (1 - discount)

    return original_cost, final_cost

# -------------------------
# Q8 & Q9
# -------------------------
@app.post("/bookings")
def create_booking(data: BookingRequest):
    global booking_counter

    movie = find_movie(data.movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    if movie["seats_available"] < data.seats:
        raise HTTPException(status_code=400, detail="Not enough seats")

    original, final = calculate_ticket_cost(
        movie["ticket_price"],
        data.seats,
        data.seat_type,
        data.promo_code
    )

    movie["seats_available"] -= data.seats

    booking = {
        "booking_id": booking_counter,
        "customer_name": data.customer_name,
        "movie": movie["title"],
        "seats": data.seats,
        "seat_type": data.seat_type,
        "original_cost": original,
        "total_cost": final
    }

    bookings.append(booking)
    booking_counter += 1

    return booking

# -------------------------
# Q10
# -------------------------
@app.get("/movies/filter")
def filter_movies(genre: str = None, language: str = None,
                  max_price: int = None, min_seats: int = None):

    result = movies

    if genre is not None:
        result = [m for m in result if m["genre"].lower() == genre.lower()]

    if language is not None:
        result = [m for m in result if m["language"].lower() == language.lower()]

    if max_price is not None:
        result = [m for m in result if m["ticket_price"] <= max_price]

    if min_seats is not None:
        result = [m for m in result if m["seats_available"] >= min_seats]

    return {"filtered_movies": result}


# -------------------------
# Q11
# -------------------------
class NewMovie(BaseModel):
    title: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=2)
    language: str = Field(..., min_length=2)
    duration_mins: int = Field(..., gt=0)
    ticket_price: int = Field(..., gt=0)
    seats_available: int = Field(..., gt=0)


@app.post("/movies", status_code=201)
def add_movie(movie: NewMovie):
    # check duplicate title
    for m in movies:
        if m["title"].lower() == movie.title.lower():
            raise HTTPException(status_code=400, detail="Movie already exists")

    new_movie = movie.dict()
    new_movie["id"] = len(movies) + 1

    movies.append(new_movie)
    return new_movie
# -------------------------
# Q12
# -------------------------
@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, ticket_price: int = None, seats_available: int = None):
    movie = find_movie(movie_id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    if ticket_price is not None:
        movie["ticket_price"] = ticket_price

    if seats_available is not None:
        movie["seats_available"] = seats_available

    return {"message": "Movie updated", "movie": movie}
# -------------------------
# Q13
# -------------------------
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    movie = find_movie(movie_id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # check if bookings exist
    for b in bookings:
        if b["movie"] == movie["title"]:
            raise HTTPException(status_code=400, detail="Cannot delete movie with bookings")

    movies.remove(movie)

    return {"message": "Movie deleted"}
# -------------------------
# Q14
# -------------------------
holds = []
hold_counter = 1


class HoldRequest(BaseModel):
    customer_name: str
    movie_id: int
    seats: int


@app.post("/seat-hold")
def create_hold(data: HoldRequest):
    global hold_counter

    movie = find_movie(data.movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    if movie["seats_available"] < data.seats:
        raise HTTPException(status_code=400, detail="Not enough seats")

    movie["seats_available"] -= data.seats

    hold = {
        "hold_id": hold_counter,
        "customer_name": data.customer_name,
        "movie_id": data.movie_id,
        "seats": data.seats
    }

    holds.append(hold)
    hold_counter += 1

    return hold


@app.get("/seat-hold")
def get_holds():
    return {"holds": holds}
# -------------------------
# Q15
# -------------------------
@app.post("/seat-confirm/{hold_id}")
def confirm_hold(hold_id: int):
    global booking_counter

    hold = None
    for h in holds:
        if h["hold_id"] == hold_id:
            hold = h
            break

    if not hold:
        raise HTTPException(status_code=404, detail="Hold not found")

    movie = find_movie(hold["movie_id"])

    total_cost = movie["ticket_price"] * hold["seats"]

    booking = {
        "booking_id": booking_counter,
        "customer_name": hold["customer_name"],
        "movie": movie["title"],
        "seats": hold["seats"],
        "seat_type": "standard",
        "original_cost": total_cost,
        "total_cost": total_cost
    }

    bookings.append(booking)
    booking_counter += 1

    holds.remove(hold)

    return {"message": "Booking confirmed", "booking": booking}

@app.delete("/seat-release/{hold_id}")
def release_hold(hold_id: int):
    hold = None
    for h in holds:
        if h["hold_id"] == hold_id:
            hold = h
            break

    if not hold:
        raise HTTPException(status_code=404, detail="Hold not found")

    movie = find_movie(hold["movie_id"])
    movie["seats_available"] += hold["seats"]

    holds.remove(hold)

    return {"message": "Hold released"}

# -------------------------
# Q16
# -------------------------
@app.get("/movies/search")
def search_movies(keyword: str):
    result = []

    for m in movies:
        if (keyword.lower() in m["title"].lower() or
            keyword.lower() in m["genre"].lower() or
            keyword.lower() in m["language"].lower()):
            result.append(m)

    if not result:
        return {"message": "No movies found"}

    return {
        "total_found": len(result),
        "movies": result
    }
# -------------------------
# Q17
# -------------------------
@app.get("/movies/sort")
def sort_movies(sort_by: str = "ticket_price", order: str = "asc"):

    valid_fields = ["ticket_price", "title", "duration_mins", "seats_available"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    reverse = True if order == "desc" else False

    sorted_movies = sorted(movies, key=lambda x: x[sort_by], reverse=reverse)

    return {"sorted_movies": sorted_movies}
# -------------------------
# Q18
# -------------------------
@app.get("/movies/page")
def paginate_movies(page: int = 1, limit: int = 3):

    start = (page - 1) * limit
    end = start + limit

    total = len(movies)
    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total_movies": total,
        "total_pages": total_pages,
        "movies": movies[start:end]
    }
# -------------------------
# Q19
# -------------------------
@app.get("/bookings/search")
def search_bookings(name: str):
    result = [b for b in bookings if name.lower() in b["customer_name"].lower()]

    return {
        "total_found": len(result),
        "bookings": result
    }


@app.get("/bookings/sort")
def sort_bookings(sort_by: str = "total_cost"):
    if sort_by not in ["total_cost", "seats"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    sorted_data = sorted(bookings, key=lambda x: x[sort_by])

    return {"bookings": sorted_data}


@app.get("/bookings/page")
def paginate_bookings(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    end = start + limit

    return {
        "bookings": bookings[start:end],
        "total": len(bookings)
    }
# -------------------------
# Q20
# -------------------------
@app.get("/movies/browse")
def browse_movies(
    keyword: str = None,
    genre: str = None,
    language: str = None,
    sort_by: str = "ticket_price",
    order: str = "asc",
    page: int = 1,
    limit: int = 3
):

    result = movies

    # 🔍 keyword filter
    if keyword:
        result = [
            m for m in result
            if keyword.lower() in m["title"].lower()
            or keyword.lower() in m["genre"].lower()
            or keyword.lower() in m["language"].lower()
        ]

    # 🎯 genre/language filter
    if genre:
        result = [m for m in result if m["genre"].lower() == genre.lower()]

    if language:
        result = [m for m in result if m["language"].lower() == language.lower()]

    # 📊 sorting
    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x.get(sort_by, 0), reverse=reverse)

    # 📄 pagination
    start = (page - 1) * limit
    end = start + limit

    total = len(result)

    return {
        "total_results": total,
        "page": page,
        "movies": result[start:end]
    }
