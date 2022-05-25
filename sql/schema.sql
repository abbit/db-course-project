DROP TABLE IF EXISTS book_publications_format;
DROP TABLE IF EXISTS journal_publications_format;
DROP TABLE IF EXISTS paper_publications_format;
DROP TABLE IF EXISTS publications_flow_history;
DROP TABLE IF EXISTS textbook_literacy_works_type;
DROP TABLE IF EXISTS novel_literacy_works_type;
DROP TABLE IF EXISTS poem_literacy_works_type;
DROP TABLE IF EXISTS article_literacy_works_type;
DROP TABLE IF EXISTS scientific_literacy_works_type;
DROP TABLE IF EXISTS publications_storage_locations;
DROP TABLE IF EXISTS storage_locations;
DROP TABLE IF EXISTS publications_literary_works;
DROP TABLE IF EXISTS literary_works_authors;
DROP TABLE IF EXISTS literary_works;
DROP TABLE IF EXISTS literacy_work_types;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS other_readers_category;
DROP TABLE IF EXISTS student_readers_category;
DROP TABLE IF EXISTS teacher_readers_category;
DROP TABLE IF EXISTS worker_readers_category;
DROP TABLE IF EXISTS retiree_readers_category;
DROP TABLE IF EXISTS publications_orders_history;
DROP TABLE IF EXISTS publications;
DROP TABLE IF EXISTS publication_formats;
DROP TABLE IF EXISTS lending_restrictions;
DROP TABLE IF EXISTS readers;
DROP TABLE IF EXISTS librarians;
DROP TABLE IF EXISTS reading_room;
DROP TABLE IF EXISTS library;
DROP TABLE IF EXISTS reader_categories;

CREATE TABLE library
(
    id      SERIAL PRIMARY KEY,
    address VARCHAR(255) NOT NULL UNIQUE,
    title   VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE reading_room
(
    id          SERIAL PRIMARY KEY,
    room_name   VARCHAR(255) NOT NULL,
    seats_count INTEGER      NOT NULL CHECK ( seats_count >= 0),
    library_id  INTEGER      NOT NULL REFERENCES library,
    UNIQUE (library_id, room_name)
);

CREATE TABLE librarians
(
    id              SERIAL PRIMARY KEY,
    full_name       VARCHAR(255) NOT NULL,
    reading_room_id INTEGER      NOT NULL REFERENCES reading_room
);

CREATE TABLE storage_locations
(
    id              SERIAL PRIMARY KEY,
    rack_no         INTEGER NOT NULL CHECK ( rack_no > 0 ),
    shelf_no        INTEGER NOT NULL CHECK ( shelf_no > 0 ),
    reading_room_id INTEGER NOT NULL REFERENCES reading_room,
    UNIQUE (reading_room_id, rack_no, shelf_no)
);

CREATE TABLE publication_formats
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE publications
(
    id               SERIAL PRIMARY KEY,
    item_no          VARCHAR(255) NOT NULL UNIQUE,
    title            VARCHAR(255) NOT NULL,
    publisher        VARCHAR(255) NOT NULL,
    language         VARCHAR(255) NOT NULL,
    pages            INTEGER      NOT NULL CHECK ( pages > 0 ),
    publication_date DATE         NOT NULL,
    count            INTEGER      NOT NULL CHECK ( count >= 0 ),
    format_id        INTEGER      NOT NULL REFERENCES publication_formats,
    UNIQUE (id, format_id)
);

CREATE TABLE book_publications_format
(
    id        INTEGER PRIMARY KEY,
    format    VARCHAR(255) NOT NULL,
    isbn      VARCHAR(255) NOT NULL UNIQUE,
    format_id INTEGER DEFAULT 1 check (format_id = 1),
    constraint subType foreign key (id, format_id) references publications (id, format_id)
);

CREATE TABLE journal_publications_format
(
    id         INTEGER PRIMARY KEY,
    discipline VARCHAR(255) NOT NULL,
    editor     VARCHAR(255) NOT NULL,
    frequency  INTERVAL     NOT NULL,
    format_id  INTEGER DEFAULT 2 check (format_id = 2),
    constraint subType foreign key (id, format_id) references publications (id, format_id)
);

CREATE TABLE paper_publications_format
(
    id        INTEGER PRIMARY KEY,
    category  VARCHAR(255) NOT NULL,
    editor    VARCHAR(255) NOT NULL,
    frequency INTERVAL     NOT NULL,
    format_id INTEGER DEFAULT 3 check (format_id = 3),
    constraint subType foreign key (id, format_id) references publications (id, format_id)
);
CREATE TABLE publications_flow_history
(
    id             INTEGER PRIMARY KEY,
    librarian_id   INTEGER   NOT NULL REFERENCES librarians,
    publication_id INTEGER   NOT NULL REFERENCES publications,
    count          INTEGER   NOT NULL CHECK ( count != 0 ),
    timestamp_     TIMESTAMP NOT NULL DEFAULT current_timestamp
);

CREATE TABLE lending_restrictions
(
    id                 SERIAL PRIMARY KEY,
    name               VARCHAR(255) NOT NULL,
    library_rooms_only BOOLEAN      NOT NULL,
    time_limit         INTERVAL,
    UNIQUE (library_rooms_only, time_limit)
);

CREATE TABLE literacy_work_types
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE literary_works
(
    id      SERIAL PRIMARY KEY,
    title   VARCHAR(255) NOT NULL,
    type_id INTEGER      NOT NULL REFERENCES literacy_work_types,
    UNIQUE (id, type_id)
);

CREATE TABLE textbook_literacy_works_type
(
    id      INTEGER PRIMARY KEY,
    subject VARCHAR(255) NOT NULL,
    type_id INTEGER DEFAULT 1 check (type_id = 1),
    constraint subType foreign key (id, type_id) references literary_works (id, type_id)
);

CREATE TABLE novel_literacy_works_type
(
    id      INTEGER PRIMARY KEY,
    genre   VARCHAR(255) NOT NULL,
    type_id INTEGER DEFAULT 2 check (type_id = 2),
    constraint subType foreign key (id, type_id) references literary_works (id, type_id)
);

CREATE TABLE poem_literacy_works_type
(
    id      INTEGER PRIMARY KEY,
    theme   VARCHAR(255) NOT NULL,
    type_id INTEGER DEFAULT 3 check (type_id = 3),
    constraint subType foreign key (id, type_id) references literary_works (id, type_id)
);

CREATE TABLE article_literacy_works_type
(
    id      INTEGER PRIMARY KEY,
    theme   VARCHAR(255) NOT NULL,
    type_id INTEGER DEFAULT 4 check (type_id = 4),
    constraint subType foreign key (id, type_id) references literary_works (id, type_id)
);

CREATE TABLE scientific_literacy_works_type
(
    id      INTEGER PRIMARY KEY,
    subject VARCHAR(255) NOT NULL,
    type_id INTEGER DEFAULT 5 check (type_id = 5),
    constraint subType foreign key (id, type_id) references literary_works (id, type_id)
);

CREATE TABLE author
(
    id          SERIAL PRIMARY KEY,
    full_name   VARCHAR(255) NOT NULL,
    nationality VARCHAR(255),
    birth_date  DATE CHECK ( birth_date < current_date ),
    death_date  DATE CHECK ( death_date < current_date )
);

CREATE TABLE publications_storage_locations
(
    id                  SERIAL PRIMARY KEY,
    publication_id      INTEGER NOT NULL REFERENCES publications,
    storage_location_id INTEGER NOT NULL REFERENCES storage_locations
);

CREATE TABLE publications_literary_works
(
    id               SERIAL PRIMARY KEY,
    publication_id   INTEGER NOT NULL REFERENCES publications,
    literary_work_id INTEGER NOT NULL REFERENCES literary_works
);

CREATE TABLE literary_works_authors
(
    id               SERIAL PRIMARY KEY,
    literary_work_id INTEGER NOT NULL REFERENCES literary_works,
    author_id        INTEGER NOT NULL REFERENCES author
);

CREATE TABLE reader_categories
(
    id   SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE readers
(
    id               SERIAL PRIMARY KEY,
    full_name        VARCHAR(255)      NOT NULL,
    category_id      INTEGER DEFAULT 1 NOT NULL REFERENCES reader_categories ON DELETE SET DEFAULT,
    issue_date       DATE              NOT NULL,
    issuer_id        INTEGER           NOT NULL REFERENCES librarians,
    issue_library_id INTEGER           NOT NULL REFERENCES library,
    UNIQUE (id, category_id)
);

CREATE TABLE other_readers_category
(
    id          INTEGER PRIMARY KEY,
    category_id INTEGER DEFAULT 1 check (category_id = 1),
    constraint subType foreign key (id, category_id) references readers (id, category_id)
);

CREATE TABLE student_readers_category
(
    id                      INTEGER PRIMARY KEY,
    category_id             INTEGER DEFAULT 2 check (category_id = 2),
    educational_institution VARCHAR(255) NOT NULL,
    group_no                INTEGER      NOT NULL CHECK ( group_no >= 0 ),
    constraint subType foreign key (id, category_id) references readers (id, category_id)
);

CREATE TABLE teacher_readers_category
(
    id                      INTEGER PRIMARY KEY,
    category_id             INTEGER DEFAULT 3 check (category_id = 3),
    educational_institution VARCHAR(255) NOT NULL,
    constraint subType foreign key (id, category_id) references readers (id, category_id)
);

CREATE TABLE worker_readers_category
(
    id           INTEGER PRIMARY KEY,
    category_id  INTEGER DEFAULT 4 check (category_id = 4),
    organization VARCHAR(255) NOT NULL,
    constraint subType foreign key (id, category_id) references readers (id, category_id)
);

CREATE TABLE retiree_readers_category
(
    id                    INTEGER PRIMARY KEY,
    category_id           INTEGER DEFAULT 5 check (category_id = 5),
    years_work_experience INTEGER NOT NULL CHECK ( years_work_experience > 0 ),
    constraint subType foreign key (id, category_id) references readers (id, category_id)
);

CREATE TABLE publications_orders_history
(
    id                     SERIAL PRIMARY KEY,
    publication_id         INTEGER   NOT NULL REFERENCES publications,
    reader_id              INTEGER   NOT NULL REFERENCES readers,
    lending_restriction_id INTEGER   NOT NULL REFERENCES lending_restrictions,
    given_timestamp        TIMESTAMP NOT NULL,
    given_librarian_id     INTEGER   NOT NULL REFERENCES librarians,
    received_timestamp     TIMESTAMP,
    received_librarian_id  INTEGER REFERENCES librarians
);
