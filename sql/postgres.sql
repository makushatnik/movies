CREATE DATABASE IF NOT EXISTS movies;

CREATE SCHEMA IF NOT EXISTS content;

CREATE EXTENSION "uuid-ossp";

SET search_path TO content, public;

CREATE TABLE IF NOT EXISTS content.film_work (
  id uuid PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  creation_date DATE,
  certificate TEXT,
  file_path TEXT,
  rating FLOAT,
  type TEXT NOT NULL,
  created_at timestamp with time zone,
  updated_at timestamp with time zone
);

-- CREATE INDEX film_work_creation_date_idx ON
--  content.film_work(creation_date);

CREATE INDEX film_work_unique_idx1 ON content.film_work (creation_date, rating);

CREATE TABLE IF NOT EXISTS content.genre (
  id uuid PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  created_at timestamp with time zone,
  updated_at timestamp with time zone
);

-- Обобщение для актёра, режиссёра и сценариста
CREATE TABLE IF NOT EXISTS content.person (
  id uuid PRIMARY KEY,
  full_name TEXT NOT NULL,
  birth_date DATE,
  created_at timestamp with time zone,
  updated_at timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
  id uuid PRIMARY KEY,
  film_work_id uuid NOT NULL,
  genre_id uuid NOT NULL,
  created_at timestamp with time zone
);

CREATE UNIQUE INDEX film_work_genre_unique_idx ON content.genre_film_work
(film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS content.person_film_work (
  id uuid PRIMARY KEY,
  film_work_id uuid NOT NULL,
  person_id uuid NOT NULL,
  role TEXT NOT NULL,
  created_at timestamp with time zone
);

-- CREATE UNIQUE INDEX film_work_person ON content.person_film_work
-- (film_work_id, person_id);

CREATE UNIQUE INDEX film_work_person_role_idx ON
content.person_film_work (film_work_id, person_id, role);
