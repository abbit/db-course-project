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
SELECT r.id, full_name
FROM readers r
         JOIN publications_orders_history poh ON r.id = poh.reader_id
         JOIN publications_literary_works plw ON poh.publication_id = plw.publication_id
         JOIN literary_works lw ON plw.literary_work_id = lw.id
WHERE lw.title = '1984';

-- #3
SELECT r.id, full_name
FROM readers r
         JOIN publications_orders_history poh ON r.id = poh.reader_id
         JOIN publications p ON poh.publication_id = p.id
WHERE p.title = 'Crime and Punishment';

-- #4
SELECT r.id, r.full_name
FROM readers r
         JOIN publications_orders_history poh ON r.id = poh.reader_id
         JOIN publications_literary_works plw ON poh.publication_id = plw.publication_id
         JOIN literary_works lw ON plw.literary_work_id = lw.id
WHERE poh.given_timestamp BETWEEN '2022-01-01' AND '2023-01-01';

-- #5
SELECT p.id, p.title, r.id, r.full_name
FROM readers r
         JOIN publications_orders_history poh ON poh.reader_id = r.id
         JOIN librarians l on l.id = poh.given_librarian_id
         JOIN library on r.issue_library_id = library.id AND library.id = r.issue_library_id
         JOIN publications p on poh.publication_id = p.id
WHERE r.full_name = 'John Knapp';

-- #6
SELECT p.id, p.title, r.id, r.full_name
FROM readers r
         JOIN publications_orders_history poh ON poh.reader_id = r.id
         JOIN librarians l on l.id = poh.given_librarian_id
         JOIN library on r.issue_library_id = library.id AND library.id != r.issue_library_id
         JOIN publications p on poh.publication_id = p.id
WHERE r.full_name = 'John Knapp';

-- #7
SELECT lw.title
FROM literary_works lw
         JOIN publications_literary_works plw on lw.id = plw.literary_work_id
         JOIN publications p on p.id = plw.publication_id
         JOIN publications_orders_history poh on p.id = poh.publication_id
         JOIN publications_storage_locations psl on p.id = psl.publication_id
         JOIN storage_locations sl on psl.storage_location_id = sl.id
         JOIN reading_room rr on sl.reading_room_id = rr.id
         JOIN library on rr.library_id = library.id
WHERE library.title = 'Boston Athenaeum'
  AND sl.rack_no = 1
  AND sl.shelf_no = 1;

-- #8
SELECT r.id, r.full_name
FROM readers r
         JOIN publications_orders_history poh ON r.id = poh.reader_id
         JOIN librarians l on l.id = poh.given_librarian_id OR l.id = poh.received_librarian_id
WHERE poh.given_timestamp BETWEEN '2022-01-01' AND '2023-01-01'
  AND l.full_name = 'Jennifer Powell'
GROUP BY r.id;

-- #9
SELECT l.id, full_name, count(l.id) as readers_count
FROM librarians l
         JOIN (SELECT given_librarian_id as librarian_id
               FROM publications_orders_history poh
               WHERE poh.given_timestamp BETWEEN '2012-01-01' AND '2023-01-01'
               union all
               SELECT received_librarian_id
               FROM publications_orders_history poh
               WHERE poh.given_timestamp BETWEEN '2012-01-01' AND '2023-01-01') poh
              ON poh.librarian_id = l.id
GROUP BY l.id
ORDER BY readers_count DESC;

-- #10
SELECT r.id, r.full_name
FROM publications_orders_history poh
         JOIN lending_restrictions lr on lr.id = poh.lending_restriction_id
         JOIN readers r on poh.reader_id = r.id
WHERE poh.received_timestamp IS NULL
  AND poh.given_timestamp + lr.time_limit < now();

-- #11
SELECT p.id, item_no, title, publisher, language, pages, publication_date
FROM publications_flow_history pfh
         JOIN publications p on pfh.publication_id = p.id
WHERE pfh.timestamp_ BETWEEN '2015-03-17' AND '2015-03-21';

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
      FROM publications_orders_history) rvh
         JOIN readers r ON r.id = rvh.reader_id
GROUP BY r.id
HAVING MAX(rvh.last_order_visit_timestamp) NOT BETWEEN '2020-01-01' AND '2023-01-01';

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
FROM literary_works lw
         JOIN publications_literary_works plw on lw.id = plw.literary_work_id
         JOIN publications_orders_history poh on plw.publication_id = poh.publication_id
GROUP BY lw.id, lw.title
ORDER BY orders_count DESC, lw.title
LIMIT 5;