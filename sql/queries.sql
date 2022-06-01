-- #1
SELECT r.id, full_name
from readers AS r
         LEFT JOIN other_readers_category orc on r.id = orc.id
         LEFT JOIN student_readers_category src on r.id = src.id
         LEFT JOIN teacher_readers_category trc on r.id = trc.id
         LEFT JOIN worker_readers_category wrc on r.id = wrc.id
         LEFT JOIN retiree_readers_category rrc on r.id = rrc.id
WHERE trc.educational_institution = 'MIT'
ORDER BY r.id;

-- #2
SELECT r.id, full_name, issue_date, issuer_id, issuer_library_id
FROM readers_reader r
         JOIN lending_publicationsordershistory poh ON r.id = poh.reader_id
         JOIN publications_publication_literacy_works plw ON poh.publication_id = plw.publication_id
         JOIN publications_literacywork lw ON plw.literacywork_id = lw.id
WHERE lw.title = '1984';

-- #3
SELECT r.id, full_name
FROM readers_reader r
         JOIN lending_publicationsordershistory poh ON r.id = poh.reader_id
         JOIN publications_publication p ON poh.publication_id = p.id
WHERE p.id = 1;

-- #4
SELECT DISTINCT r.id, full_name, issue_date, issuer_id, issuer_library_id, p.title as publication_title
FROM readers_reader r
         JOIN lending_publicationsordershistory poh ON r.id = poh.reader_id
         JOIN publications_publication_literacy_works plw ON poh.publication_id = plw.publication_id
         JOIN publications_publication p ON poh.publication_id = p.id
         JOIN publications_literacywork lw ON plw.literacywork_id = lw.id
WHERE cast(poh.given_timestamp as date) BETWEEN '2022-01-01' AND '2023-01-01';

-- #5
SELECT *
FROM readers_reader r
         JOIN lending_publicationsordershistory poh ON poh.reader_id = r.id
         JOIN publications_publication p on poh.publication_id = p.id
         JOIN libraries_librarian l on l.id = poh.given_librarian_id
         JOIN libraries_readingroom rr on l.reading_room_id = rr.id and rr.library_id = r.issuer_library_id
WHERE r.id = 8;

-- #6
SELECT *
FROM readers_reader r
         JOIN lending_publicationsordershistory poh ON poh.reader_id = r.id
         JOIN publications_publication p on poh.publication_id = p.id
         JOIN libraries_librarian l on l.id = poh.given_librarian_id
         JOIN libraries_readingroom rr on l.reading_room_id = rr.id and rr.library_id != r.issuer_library_id
WHERE r.id = 8;

-- #7
SELECT *
FROM publications_literacywork lw
         JOIN publications_publication_literacy_works plw on lw.id = plw.literacywork_id
         JOIN publications_publication p on p.id = plw.publication_id
         JOIN lending_publicationsordershistory poh on p.id = poh.publication_id
         JOIN libraries_storagelocation_publications psl on p.id = psl.publication_id
         JOIN libraries_storagelocation sl on psl.storagelocation_id = sl.id
         JOIN libraries_readingroom rr on sl.reading_room_id = rr.id
         JOIN libraries_library library on rr.library_id = library.id
WHERE storagelocation_id = 5
  and poh.received_timestamp IS NULL;

-- #8
SELECT r.id, r.full_name, issue_date, issuer_id, issuer_library_id
FROM readers_reader r
         JOIN lending_publicationsordershistory poh ON r.id = poh.reader_id
         JOIN libraries_librarian l on l.id = poh.given_librarian_id OR l.id = poh.received_librarian_id
WHERE cast(poh.given_timestamp as date) BETWEEN '2022-01-01' AND '2023-01-01'
  AND l.id = 1
GROUP BY r.id;

-- #9
SELECT l.id, full_name, count(l.id) as readers_count
FROM libraries_librarian l
         JOIN (SELECT given_librarian_id as librarian_id
               FROM lending_publicationsordershistory poh
               WHERE cast(poh.given_timestamp as date) BETWEEN '2012-01-01' AND '2023-01-01'
               union all
               SELECT received_librarian_id
               FROM lending_publicationsordershistory poh
               WHERE cast(poh.given_timestamp as date) BETWEEN '2012-01-01' AND '2023-01-01') poh
              ON poh.librarian_id = l.id
GROUP BY l.id
ORDER BY readers_count DESC;

-- #10
SELECT r.id, full_name, issue_date, issuer_id, issuer_library_id
FROM lending_publicationsordershistory poh
         JOIN lending_lendingrestriction lr on lr.id = poh.lending_restriction_id
         JOIN readers_reader r on poh.reader_id = r.id
WHERE poh.received_timestamp IS NULL
  AND poh.given_timestamp + lr.time_limit < now();

-- #11
SELECT p.id, item_no, title, publisher, language, pages, publication_date
FROM libraries_publicationsflowhistory pfh
         JOIN publications_publication p on pfh.publication_id = p.id
WHERE cast(pfh.record_timestamp as date) BETWEEN '2015-03-17' AND '2025-03-21';

-- #12
SELECT l.id, l.full_name
FROM librarians l
         JOIN reading_room rr on l.reading_room_id = rr.id
         JOIN library lib on lib.id = rr.library_id
WHERE lib.title = 'Boston Public Library'
  AND rr.room_name = 'Reading room №1';

-- #13
SELECT r.full_name, MAX(rvh.last_order_visit_timestamp) last_visit_timestamp
FROM (SELECT reader_id, GREATEST(given_timestamp, received_timestamp) last_order_visit_timestamp
      FROM lending_publicationsordershistory) rvh
         JOIN readers_reader r ON r.id = rvh.reader_id
GROUP BY r.id
HAVING cast(MAX(rvh.last_order_visit_timestamp) as date) NOT BETWEEN '2023-01-01' AND '2024-01-01';

-- #14
SELECT p.item_no, p.title
FROM publications p
         JOIN publications_literary_works plw on p.id = plw.publication_id
         JOIN literary_works lw on plw.literary_work_id = lw.id
WHERE lw.title = 'On the K-theory of of local fields';

-- #15
SELECT DISTINCT p.item_no, p.title
FROM publications p
         JOIN publications_literary_works plw on p.id = plw.publication_id
         JOIN literary_works lw on plw.literary_work_id = lw.id
         JOIN literary_works_authors lwa on lw.id = lwa.literary_work_id
         JOIN author a on a.id = lwa.author_id
WHERE a.full_name = 'Alexander Pushkin';

-- #16
SELECT lw.title, count(lw.id) as orders_count
FROM publications_literacywork lw
         JOIN publications_publication_literacy_works plw on lw.id = plw.literacywork_id
         JOIN lending_publicationsordershistory poh on plw.publication_id = poh.publication_id
GROUP BY lw.id, lw.title
ORDER BY orders_count DESC, lw.title
LIMIT 5;