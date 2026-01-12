from flask import Blueprint, request, jsonify
from models import db, Conference, Track

conference_bp = Blueprint("conference_bp", __name__)

# =============================
# CONFERENCE
# =============================

@conference_bp.route("/api/conferences", methods=["POST"])
def create_conference():
    data = request.json

    conf = Conference(
        name=data["name"],
        description=data.get("description"),
        start_date=data["start_date"],
        end_date=data["end_date"],
        submission_deadline=data["submission_deadline"]
    )

    db.session.add(conf)
    db.session.commit()

    return jsonify({
        "message": "Conference created successfully",
        "conference_id": conf.id
    }), 201


@conference_bp.route("/api/conferences", methods=["GET"])
def get_conferences():
    conferences = Conference.query.all()
    result = []

    for c in conferences:
        result.append({
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "start_date": str(c.start_date),
            "end_date": str(c.end_date),
            "submission_deadline": str(c.submission_deadline)
        })

    return jsonify(result)


# =============================
# TRACK
# =============================

@conference_bp.route("/api/conferences/<int:cid>/tracks", methods=["POST"])
def create_track(cid):
    data = request.json

    track = Track(
        name=data["name"],
        conference_id=cid
    )

    db.session.add(track)
    db.session.commit()

    return jsonify({
        "message": "Track created successfully",
        "track_id": track.id
    }), 201


@conference_bp.route("/api/conferences/<int:cid>/tracks", methods=["GET"])
def get_tracks(cid):
    tracks = Track.query.filter_by(conference_id=cid).all()

    result = []
    for t in tracks:
        result.append({
            "id": t.id,
            "name": t.name
        })

    return jsonify(result)
