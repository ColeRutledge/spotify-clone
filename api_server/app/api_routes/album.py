from flask import Flask, Blueprint, jsonify
from app.models import db, Album, Artist, Song
from sqlalchemy.orm import joinedload

bp = Blueprint('album', __name__, url_prefix="/api/album")


# GET all albums on Spotify
@bp.route("/", methods=["GET"])
def get_albums():
    albums = Album.query.all()
    # artist =[artist.to_dict() for artist in albums.artist]
    albums = [{"title": album.title, "id": album.id, "image_url": album.image_url,
                "artist": album.artist.name} for album in albums]
    
    return {"albums": albums}

# GET one album
@bp.route("/<int:id>", methods=["GET"])
def get_album(id):
    album = Album.query.get(id)
    res = {"title": album.title,
           "artist": album.artist.name}
    return jsonify(res)



# GET all songs for an album
@bp.route("/<int:id>/songs")
def get_album_songs(id):
    # Another way of doing this
    # album = Album.query.get(id)
    # songs = Song.query.filter_by(album_id=id).all()
    album = Album.query.options(joinedload("songs")).get(id)
    songs = [song.to_dict() for song in album.songs]
    # payload = {"album": album}
    payload = {"album": {"artist":album.artist.name, 
                        "album_name": album.title,"songs": songs}}
    return payload

# GET one song from album
@bp.route("/<int:id>/<int:song_id>")
def get_album_song(id,song_id):
    songs = Song.query.filter_by(album_id=id,id=song_id).all()
    res = [{"title": song.title,
    "album": song.album.title,
    "song_length": song.song_length,
    "song_url": song.song_url} for song in songs]
    return jsonify(res)