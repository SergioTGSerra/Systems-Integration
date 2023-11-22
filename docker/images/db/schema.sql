CREATE TABLE public.imported_documents (
	id              serial PRIMARY KEY,
	file_name       VARCHAR(250) NOT NULL,
	xml             XML NOT NULL,
	is_deleted      BOOLEAN NOT NULL DEFAULT FALSE,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);