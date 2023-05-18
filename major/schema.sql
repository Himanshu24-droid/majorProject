CREATE TABLE user(
  id INT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255) UNIQUE NOT NULL,
  password TEXT NOT NULL
);
CREATE TABLE playlist(
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  user_id INT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user(id)
);
CREATE TABLE song(
  id VARCHAR(255) PRIMARY KEY,
  playlist_id INT NOT NULL,
  FOREIGN KEY (playlist_id) REFERENCES playlist(id)
);
CREATE TABLE ratings(
  rating FLOAT NOT NULL,
  user_id INT NOT NULL,
  song_id VARCHAR(255) NOT NUll,
  FOREIGN KEY(user_id) REFERENCES user(id),
  CONSTRAINT PK_Ratings PRIMARY KEY (user_id,song_id)
);