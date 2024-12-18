import base64
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

# Define the scope of the required permissions
SCOPE = "user-library-read user-top-read"
# Define your client ID, client secret, and redirect URI
client_id = "73bce3be0fa34320a350e72d2a2cde3b"
client_secret = "318c48fdd78544f587c09363ee29a212"
redirect_uri = "http://localhost:8080"
# Initialize the Spotify client with the OAuth manager
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=SCOPE))
#sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
# Now you can use the client to access the user's top tracks
results = sp.current_user_top_tracks(limit=10)
#for idx, track in enumerate(results['items']):
#  print(f"{idx + 1}. {track['name']} by {track['artists'][0]['name']}")
##############################################################
from mido import Message, MidiFile, MidiTrack

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Basit bir drum pattern
track.append(Message('note_on', note=36, velocity=100, time=0))  # Kick
track.append(Message('note_off', note=36, velocity=64, time=120))
track.append(Message('note_on', note=38, velocity=100, time=240))  # Snare
track.append(Message('note_off', note=38, velocity=64, time=360))

mid.save('C:\\Users\\denizdu\\Documents\\example.mid')
#mid.save('example.mid')
##############################################################

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Örnek veri (tempo, enerji, dans edilebilirlik, beğeni)
data = [[120, 0.8, 0.7, 1], [100, 0.5, 0.3, 0], [140, 0.9, 0.8, 1]]  # Son değer beğeni (1/0)
X = [row[:-1] for row in data]
y = [row[-1] for row in data]

# Model eğitimi
model = DecisionTreeClassifier()
model.fit(X, y)

# Yeni beat önerisi
new_beat = [[130, 0.7, 0.6]]  # Tempo, enerji, dans edilebilirlik
print("Beğenme olasılığı:", model.predict(new_beat))
