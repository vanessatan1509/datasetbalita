-- Table: public.stunting

-- DROP TABLE IF EXISTS public.stunting;

CREATE TABLE IF NOT EXISTS public.stunting
(
	id serial PRIMARY KEY,
	name VARCHAR(30),
	gender VARCHAR(10),
	birthdate date,
	age int,
	weight float,
	height float
)

TABLESPACE pg_default;

SELECT * FROM public.stunting;

ALTER TABLE IF EXISTS public.stunting
    OWNER to postgres;