from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB Connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/meet_and_eat"
mongo = PyMongo(app)


# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Create Event
@app.route('/create-event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        location = request.form.get('location')
        date = request.form.get('date')

        mongo.db.events.insert_one({
            "event_name": event_name,
            "location": location,
            "date": date,
            "participants": []   # New field added
        })

        return redirect('/events')

    return render_template('create_event.html')


# View Events
@app.route('/events')
def events():
    all_events = mongo.db.events.find()
    return render_template('events.html', events=all_events)


# Join Event
@app.route('/join-event/<event_id>', methods=['POST'])
def join_event(event_id):
    participant_name = request.form.get('participant_name')

    mongo.db.events.update_one(
        {"_id": ObjectId(event_id)},
        {
            "$push": {
                "participants": participant_name
            }
        }
    )

    return redirect('/events')


# Delete Event
@app.route('/delete-event/<event_id>')
def delete_event(event_id):
    mongo.db.events.delete_one(
        {"_id": ObjectId(event_id)}
    )

    return redirect('/events')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)