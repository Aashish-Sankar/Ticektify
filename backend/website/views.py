from datetime import date, datetime, timedelta
from flask import Blueprint, jsonify,request
from sqlalchemy import func
from . import models
from . import db
from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from .redis_utils import redis_client
import json
from sqlalchemy.orm import joinedload

views = Blueprint('views',__name__)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_identity = get_jwt_identity()
            user = models.User.query.get(user_identity)
            if user.role == models.UserRole.admin:
                return f(*args, **kwargs)
            else:
                return jsonify({'error': 'Access forbidden'}), 403
        except Exception:
            return jsonify({'error': 'User not authenticated'}), 401
    return decorated_function



@views.route('/api/admin/home', methods = ['GET'])
@jwt_required()
@admin_only
def admin_home():
    screenings, num_results = admin_screening_auxiliar()
    serialized_screenings = [serialize_screening(screening) for screening in screenings]
    data = [{"screening": screening, "num_results": n} for screening, n in zip(serialized_screenings, num_results)]
    try:
        cached_response = redis_client.get('admin_home')
        if cached_response:
            if cached_response == json.dumps(data):
                print('cache')
                return json.loads(cached_response)

        redis_client.set('admin_home', json.dumps(data), ex=3600)

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})


def admin_screening_auxiliar():
    current_day = date.today()
    future = current_day + timedelta(weeks=3) 
    past = current_day - timedelta(weeks=1)
   
    screening = models.Screening.query.filter(models.Screening.day <= future, models.Screening.day >= past).order_by(models.Screening.day.asc(), models.Screening.time.asc()).all()
    num_results = []
    for proj in screening:
        num_results.append(proj.venue.capacity - compute_booked_seats(proj.id))
    return screening, num_results

def compute_booked_seats(id):
    screening = models.Screening.query.filter(models.Screening.id == id).one()
    sum_result = db.session.query(db.func.sum(models.Bookings.seats).label('booked')).filter(models.Bookings.screening == screening).one()
    num_booked_seats = sum_result.booked
    if (sum_result.booked != None):
        num_free_seats = screening.venue.capacity - num_booked_seats
    else:
        num_free_seats = screening.venue.capacity

    return  num_free_seats

def serialize_show(show):
    return {
        'id': show.id,
        'name': show.name,
        'rating': show.rating,
        'price': show.price,
        'tags': show.tags,
        'img': show.img
    }

def serialize_venue(venue):
    return {
        'id': venue.id,
        'name': venue.name,
        'capacity': venue.capacity,
        'place': venue.place,
        'location': venue.location
    }

def serialize_screening(screening):
    return {
        'id': screening.id,
        'day': screening.day.strftime('%Y-%m-%d'),
        'time': screening.time.strftime('%H:%M:%S'),
        'show': serialize_show(screening.show),
        'venue': serialize_venue(screening.venue),
    }



@views.route('/api/admin/add', methods=['GET'])
@admin_only
@jwt_required()
def add():
    try:
        Shows = models.Show.query.all()
        venues = models.Venue.query.all()
        current_day = date.today().strftime('%Y-%m-%d')

        data = {
            "Shows": [serialize_show(show) for show in Shows],
            "venues": [serialize_venue(venue) for venue in venues],
            "current_day": current_day
        }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

@views.route('/api/admin/add', methods=['POST'])
@admin_only
@jwt_required()
def add_post():
    data = request.json  
    Show = data.get('Shows')
    venue = data.get('venue')
    day = data.get('day')
    time = data.get('time')
    time = time + ':00'
    day = datetime.strptime(day, "%Y-%m-%d").date()
    time = datetime.strptime(time, "%H:%M:%S").time()

    new_screening = models.Screening(day=day, time=time, show_id=Show, venue_id=venue)
    db.session.add(new_screening)
    db.session.commit()

    return jsonify({"message": "Screening added successfully"})

@views.route('/api/admin/venue_add', methods=['POST'])
@admin_only
@jwt_required()
def add_venue_post():
    data = request.json 

    name = data.get('name')
    capacity = data.get('capacity')
    place = data.get('place')
    location = data.get('location')

    new_venue = models.Venue(name=name, capacity=capacity, place=place, location=location)
    db.session.add(new_venue)
    db.session.commit()

    return jsonify({"message": "Venue added successfully"})

@views.route('/api/admin/show_add', methods=['POST'])
@admin_only
@jwt_required()
def add_show_post():
    data = request.json 

    name = data.get('name')
    tags = data.get('tags')
    rating = data.get('rating')
    price = data.get('price')
    img = data.get('img')

    new_show = models.Show(name=name, tags=tags, rating=rating, price=price, img=img)
    db.session.add(new_show)
    db.session.commit()

    return jsonify({"message": "Show added successfully"})

@views.route('/api/user/search', methods=['POST'])

def user_search():
    current_day = date.today()
    data = request.json 

    search_term = data.get('searched')

    searches = models.Screening.query.join(models.Venue).join(models.Show).filter(
        (models.Screening.day >= current_day),
        (models.Venue.location.like(f'%{search_term}%') |
         models.Venue.place.like(f'%{search_term}%') |
         models.Show.rating.like(f'%{search_term}%') |
         models.Show.tags.like(f'%{search_term}%') |
         models.Venue.name.like(f'%{search_term}%') |
         models.Show.name.like(f'%{search_term}%') |
         models.Screening.day.like(f'%{search_term}%') |
         models.Screening.time.like(f'%{search_term}%'))).order_by(models.Screening.day.asc(), models.Screening.time.asc()).all()

    search_results = []
    for screening in searches:
        bookings = models.Bookings.query.filter(models.Bookings.screening_id == screening.id).all()
        serialized_bookings = [serialize_booking(booking) for booking in bookings]
        serialized_screening = serialize_screening(screening)
        serialized_screening['bookings'] = serialized_bookings
        search_results.append(serialized_screening)

    return jsonify({'searchResults': search_results})


@views.route("/api/admin/edit/<int:id>", methods=["GET"])
@admin_only
@jwt_required()
def edit(id):
    try:
        shows = models.Show.query.all()
        venues = models.Venue.query.all()
        current_data = serialize_screening(models.Screening.query.get(id))
        serialized_shows = [serialize_show(show) for show in shows]
        serialized_venues = [serialize_venue(venue) for venue in venues]  # Serialize the current_data
        data = {"shows": serialized_shows, "venues": serialized_venues, "current_data": current_data}
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

@views.route("/api/admin/edit/<int:id>", methods=["POST"])
@admin_only
@jwt_required()
def edit_post(id):
    try:
        data = request.json
        show_id = data.get("Shows")
        venue_id = data.get("venue")
        day = data.get("day")
        time = data.get("time")
        time = time + ':00'

        day = datetime.strptime(day, "%Y-%m-%d").date()
        time = datetime.strptime(time, "%H:%M:%S").time()

        screening = models.Screening.query.filter_by(id=id).first()
        screening.day = day
        screening.time = time
        screening.show_id = show_id
        screening.venue_id = venue_id

        db.session.commit()
        return jsonify({"message": "Screening edited successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})

@views.route("/api/admin/delete/<int:id>", methods=["DELETE"])
@admin_only
@jwt_required()
def delete(id):
    try:
        current_data = models.Screening.query.get(id)
        if current_data:
            db.session.delete(current_data)
            db.session.commit()
            return jsonify({"message": "Screening deleted successfully"})

        return jsonify({"error": "Screening not found"})

    except Exception as e:
        return jsonify({"error": str(e)})


@views.route("/api/admin/venues")
@jwt_required()
@admin_only
def venue_view():
    try:
        venues = models.Venue.query.all()
        serialized_venues = [serialize_venue(venue) for venue in venues]
        return jsonify(serialized_venues)

    except Exception as e:
        return jsonify({"error": str(e)})


@views.route("/api/admin/shows")
@jwt_required()
@admin_only
def show_view():
    try:
        shows = models.Show.query.all()
        serialized_shows = [serialize_show(show) for show in shows]
        return jsonify(serialized_shows)

    except Exception as e:
        return jsonify({"error": str(e)})
    
@views.route("/api/admin/venue_edit/<int:id>", methods=["GET"])
@admin_only
@jwt_required()
def edit_venue(id):
    try:
        current_data = models.Venue.query.get(id)
        serialized_current_data = serialize_venue(current_data)
        return jsonify(serialized_current_data)

    except Exception as e:
        return jsonify({"error": str(e)})

@views.route("/api/admin/venue_edit/<int:id>", methods=["POST"])
@admin_only
@jwt_required()
def edit_venue_post(id):
    try:
        data = request.json
        name = data.get('name')
        capacity = data.get('capacity')
        place = data.get('place')
        location = data.get('location')

        venue = models.Venue.query.filter_by(id=id).first()
        venue.name = name
        venue.capacity = capacity
        venue.place = place
        venue.location = location 

        db.session.commit()
        return jsonify({"message": "Venue edited successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})

@views.route("/api/admin/venue_delete/<int:id>", methods=["DELETE"])
@admin_only
@jwt_required()
def delete_venue(id):
    try:
        venue = models.Venue.query.get(id)
        if venue:
            db.session.delete(venue)
            db.session.commit()
            return jsonify({"message": "Venue deleted successfully"})
        
        return jsonify({"error": "Venue not found"})

    except Exception as e:
        return jsonify({"error": str(e)})
    
@views.route("/api/admin/show_edit/<int:id>", methods=["GET"])
@admin_only
@jwt_required()
def edit_show(id):
    try:
        current_data = models.Show.query.get(id)
        serialized_current_data = serialize_show(current_data)
        return jsonify(serialized_current_data)

    except Exception as e:
        return jsonify({"error": str(e)})

@views.route("/api/admin/show_edit/<int:id>", methods=["POST"])
@admin_only
@jwt_required()
def edit_show_post(id):
    try:
        data = request.json
        name = data.get('name')
        rating = data.get('rating')
        price = data.get('price')
        tags = data.get('tags')
        img = data.get('img')

        show = models.Show.query.filter_by(id=id).first()
        show.name = name
        show.rating = rating
        show.price = price
        show.tags = tags 
        show.img = img

        db.session.commit()
        return jsonify({"message": "Show edited successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})

@views.route("/api/admin/show_delete/<int:id>", methods=["DELETE"])
@admin_only
@jwt_required()
def delete_show(id):
    try:
        show = models.Show.query.get(id)
        if show:
            db.session.delete(show)
            db.session.commit()
            return jsonify({"message": "Show deleted successfully"})

        return jsonify({"error": "Show not found"})

    except Exception as e:
        return jsonify({"error": str(e)})
    
@views.route("/api/user/home")
@jwt_required()
def user_home():

    current_day = date.today()
    current_day = date.today()

    screening, num_results = admin_screening_auxiliar()
    all_screenings = models.Screening.query.filter(models.Screening.day >= current_day).order_by(models.Screening.day.asc(), models.Screening.time.asc()).all()
    serialized_screenings = [serialize_screening(screening) for screening in all_screenings]

    data = {
        "screenings": serialized_screenings,
        "packed": [{"screening": serialize_screening(s), "num_results": n} for s, n in zip(screening, num_results)]
    }

    try:
        cached_response = redis_client.get('user_home')
        if cached_response:
            match = (cached_response) == json.dumps(data)
            if match:
                return json.loads(cached_response)
        
    
        redis_client.set('user_home', json.dumps(data), ex=3600)
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

@views.route("/api/booking/", defaults={'id': None})
@views.route("/api/booking/<int:id>")
@jwt_required()
def booking(id):
    try:
        current_day = date.today()
        all_screenings = models.Screening.query.filter(models.Screening.day >= current_day).order_by(models.Screening.day.asc(), models.Screening.time.asc()).all()

        if id is None:
            data = {
                "screening": None,
                "screenings": [serialize_screening(screening) for screening in all_screenings]
            }
        else:
            screening = models.Screening.query.get(id)
            screenings = models.Screening.query.filter(models.Screening.show_id == screening.show_id, models.Screening.day >= current_day).order_by(models.Screening.day.asc(), models.Screening.time.asc()).all()
            data = {
                "screening": serialize_screening(screening),
                "screenings": [serialize_screening(s) for s in screenings]
            }

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

@views.route("/api/booking", methods=["POST"])
@jwt_required()
def booking_post():
    try:
        data = request.json
        choosen_screening = data.get("screening")
        choosen_num_seats = data.get("seats")
        cost = data.get("totalPrice")

        screening = models.Screening.query.get(choosen_screening)

        booked_seats = db.session.query(func.sum(models.Bookings.seats)).filter(models.Bookings.screening_id == screening.id).scalar()

        if booked_seats is None:
            booked_seats = 0

        venue_capacity = screening.venue.capacity

        available_seats = venue_capacity - booked_seats

        if available_seats - int(choosen_num_seats) < 0:
            return jsonify({"error": f"You can only book {available_seats} seats"})

        new_reservation = models.Bookings(user_id=get_jwt_identity(), screening_id=screening.id, seats=int(choosen_num_seats), date_time=datetime.now(), cost=int(cost))

        db.session.add(new_reservation)
        db.session.commit()

        return jsonify({"message": f"You have bought {choosen_num_seats} tickets for {screening.show.name}"})

    except Exception as e:
        return jsonify({"message": str(e)})
    
def serialize_booking(booking):
    return {
        'id': booking.id,
        'user_id': booking.user_id,
        'screening_id': booking.screening_id,
        'screening': serialize_screening(booking.screening),
        'seats': booking.seats,
        'cost': booking.cost,
        'date_time': booking.date_time.strftime('%Y-%m-%d %H:%M:%S'),
    }


@views.route("/api/user/bookings")
@jwt_required()
def user_bookings():
    try:
        current_day = date.today()
        now = []
        past = []
        now_bookings = models.Bookings.query.filter(models.Bookings.user_id == get_jwt_identity()).order_by(models.Bookings.date_time).all() #change 3 to current_user.id

        for book in now_bookings:
            if book.screening.day >= current_day:
                now.append(serialize_booking(book))
            else:
                past.append(serialize_booking(book))

        data = {
            "now_bookings": now,
            "past_bookings": past
        }
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

  
@views.route("/api/admin/summary")
@admin_only
@jwt_required()
def admin_summary():
    try:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=7)


        date_summary = db.session.query(
            func.strftime('%Y-%m-%d', models.Bookings.date_time).label('date'),
            func.count(models.Bookings.id).label('count')
        ).filter(models.Bookings.date_time >= start_date, models.Bookings.date_time <= end_date) \
            .group_by(func.strftime('%Y-%m-%d', models.Bookings.date_time)) \
            .order_by(func.strftime('%Y-%m-%d', models.Bookings.date_time)) \
            .all()


        chart_data = [{
            "x": row.date,
            "y": row.count
        } for row in date_summary]

        return jsonify({"bookings": chart_data})

    except Exception as e:
        return jsonify({"error": str(e)})
    
@views.route("/api/admin/csv_download/<int:id>", methods=['GET'])
@jwt_required()
def get_venue_details(id):
    venue = models.Venue.query.options(joinedload(models.Venue.screened)).get(id)
    if not venue:
        return jsonify({"error": "Venue not found"}), 404
    
    venue_details = {
        "id": venue.id,
        "name": venue.name,
        "capacity": venue.capacity,
        "place": venue.place,
        "location": venue.location,
        "screened": []
    }
    
    for screening in venue.screened:
        booked_tickets = sum(booking.seats for booking in screening.booked)
        show_details = {
            "show_id": screening.show.id,
            "show_name": screening.show.name,
            "rating": screening.show.rating,
            "price": screening.show.price,
            "tags": screening.show.tags,
            "img": screening.show.img,
            "day": screening.day.strftime('%Y-%m-%d'),
            "time": screening.time.strftime('%H:%M'),
            "booked": booked_tickets
        }
        venue_details["screened"].append(show_details)

    response = jsonify(venue_details)
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    return response