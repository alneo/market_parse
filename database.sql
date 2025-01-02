-- Table: public.tovars

-- DROP TABLE IF EXISTS public.tovars;

CREATE TABLE IF NOT EXISTS public.tovars
(
    id integer NOT NULL DEFAULT nextval('tovars_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    price double precision,
    price_v character varying COLLATE pg_catalog."default",
    picture character varying COLLATE pg_catalog."default",
    razdel character varying COLLATE pg_catalog."default"
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tovars
    OWNER to postgres;