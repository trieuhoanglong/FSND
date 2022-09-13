--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

CREATE TABLE public.actor_in_movie (
    actor_id integer NOT NULL,
    movie_id integer NOT NULL
);


ALTER TABLE public.actor_in_movie OWNER TO postgres;


CREATE TABLE public.actors (
    id integer NOT NULL,
    name character varying(120) NOT NULL,
    date_of_birth date NOT NULL
);


ALTER TABLE public.actors OWNER TO postgres;


CREATE SEQUENCE public.actors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actors_id_seq OWNER TO postgres;


ALTER SEQUENCE public.actors_id_seq OWNED BY public.actors.id;


CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;


CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying(120) NOT NULL,
    release_date date NOT NULL,
    imdb_rating double precision NOT NULL
);


ALTER TABLE public.movies OWNER TO postgres;


CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO postgres;


ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


ALTER TABLE ONLY public.actors ALTER COLUMN id SET DEFAULT nextval('public.actors_id_seq'::regclass);


ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


INSERT INTO public.alembic_version VALUES ('0f87e8f45ce0');


SELECT pg_catalog.setval('public.actors_id_seq', 1, false);


SELECT pg_catalog.setval('public.movies_id_seq', 1, false);


ALTER TABLE ONLY public.actor_in_movie
    ADD CONSTRAINT actor_in_movie_pkey PRIMARY KEY (actor_id, movie_id);


ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.actor_in_movie
    ADD CONSTRAINT actor_in_movie_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actors(id);


ALTER TABLE ONLY public.actor_in_movie
    ADD CONSTRAINT actor_in_movie_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(id);


INSERT INTO public.actors(name, date_of_birth) VALUES('Long', 'April 9, 1991');
INSERT INTO public.actors(name, date_of_birth) VALUES('Andree Right', 'July 7, 1923');
INSERT INTO public.actors(name, date_of_birth) VALUES('John Left', 'August 16, 1986');


INSERT INTO public.movies(title, release_date, imdb_rating) VALUES('G.J.Joe', 'January 16, 1961', 7.2);
INSERT INTO public.movies(title, release_date, imdb_rating) VALUES('Titanic', 'March 24, 1996', 9.5);


INSERT INTO public.actor_in_movie VALUES(1, 1);
INSERT INTO public.actor_in_movie VALUES(2, 1);
INSERT INTO public.actor_in_movie VALUES(3, 2);

