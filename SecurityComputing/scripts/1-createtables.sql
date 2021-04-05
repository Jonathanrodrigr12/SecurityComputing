CREATE TABLE public."log_user"
(
    "id" serial NOT NULL ,
    "user_log" character varying(1000) COLLATE pg_catalog."default" NOT NULL,
    date_log timestamp without time zone,
    CONSTRAINT log_user_pk PRIMARY KEY ("id")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

CREATE TABLE public.registerip
(
    id serial,
    ip character varying(100) COLLATE pg_catalog."default",
    country character varying(100) COLLATE pg_catalog."default",
    distance integer,
    invocation integer DEFAULT 1
)

TABLESPACE pg_default;

ALTER TABLE public.registerip
    OWNER to postgres;

CREATE TABLE public.security
(
    id serial,
    token character varying(1000) COLLATE pg_catalog."default",
    active boolean DEFAULT true
)

TABLESPACE pg_default;

ALTER TABLE public.security
    OWNER to postgres;	

CREATE TABLE public."user"
(
    id serial,
    email character varying(100) COLLATE pg_catalog."default",
    password character varying(100) COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE public."user"
    OWNER to postgres;	
	