from django.shortcuts import render
from .forms import *
from .tables import *

__all__ = [
    'readers_with_literacy_work',
    'readers_with_publication',
    'readers_and_publications_in_date_range',
    'publications_from_readers_issuer_library',
    'publications_not_from_readers_issuer_library',
    'literacy_works_from_storage_location',
    'readers_served_by_librarian_in_date_range',
    'librarians_readers_served_in_date_range',
    'readers_with_outdated_orders',
    'literacy_works_flow_in_date_range',
    'readers_not_seen_in_date_range',
    'top_5_books_by_polularity',
]

links = [link.replace('_', ' ') for link in __all__]


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def index(request):
    return render(request, 'index.html', {'links': links})


def readers_with_literacy_work(request):
    query_name = 'readers_with_literacy_work'
    table = None
    if request.method == 'POST':
        form = LiteracyWorkChoiceForm(request.POST)
        if form.is_valid():
            literacy_work_id = form.cleaned_data['literacy_work'].pk
            readers = Reader.objects.raw("""
SELECT r.id, full_name, issue_date, issuer_id, issuer_library_id
FROM readers_reader r
         JOIN lending_publicationsordershistory poh ON r.id = poh.reader_id
         JOIN publications_publication_literacy_works plw ON poh.publication_id = plw.publication_id
         JOIN publications_literacywork lw ON plw.literacywork_id = lw.id
WHERE lw.id = %s
            """, [literacy_work_id])
            table = ReaderTable(readers)
    else:
        form = LiteracyWorkChoiceForm()

    return render(request, 'form_and_table.html',
                  {'links': links,
                   'title': query_name.replace('_', ' '),
                   'url_name': query_name, 'form': form,
                   'table': table}
                  )


def readers_with_publication(request):
    query_name = 'readers_with_publication'
    table = None
    if request.method == 'POST':
        form = PublicationChoiceForm(request.POST)
        if form.is_valid():
            publication_id = form.cleaned_data['publication'].pk
            readers = Reader.objects.raw("""
SELECT r.id, full_name
FROM readers_reader r
         JOIN lending_publicationsordershistory poh ON r.id = poh.reader_id
         JOIN publications_publication p ON poh.publication_id = p.id
WHERE p.id = %s
            """, [publication_id])
            table = ReaderTable(readers)
    else:
        form = PublicationChoiceForm()

    return render(request, 'form_and_table.html',
                  {'links': links,
                   'title': query_name.replace('_', ' '),
                   'url_name': query_name, 'form': form,
                   'table': table}
                  )


def readers_and_publications_in_date_range(request):
    query_name = 'readers_and_publications_in_date_range'
    table = None
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date'].isoformat()
            end_date = form.cleaned_data['end_date'].isoformat()
            readers = Reader.objects.raw("""
SELECT DISTINCT r.id, full_name, issue_date, issuer_id, issuer_library_id,  p.title as publication_title
FROM readers_reader r
         JOIN lending_publicationsordershistory poh ON r.id = poh.reader_id
         JOIN publications_publication_literacy_works plw ON poh.publication_id = plw.publication_id
         JOIN publications_publication p ON poh.publication_id = p.id
         JOIN publications_literacywork lw ON plw.literacywork_id = lw.id
WHERE cast(poh.given_timestamp as date) BETWEEN %s AND %s
            """, [start_date, end_date])
            table = ReaderAndPublicationTable(readers)
    else:
        form = DateRangeForm()

    return render(request, 'form_and_table.html',
                  {'links': links,
                   'title': query_name.replace('_', ' '),
                   'url_name': query_name,
                   'form': form,
                   'table': table}
                  )


def publications_from_readers_issuer_library(request):
    query_name = 'publications_from_readers_issuer_library'
    table = None
    if request.method == 'POST':
        form = ReaderChoiceForm(request.POST)
        if form.is_valid():
            reader_id = form.cleaned_data['reader'].pk
            publications = Publication.objects.raw("""
SELECT p.id, item_no, p.title, publisher, language, pages, publication_date, count
FROM readers_reader r
         JOIN lending_publicationsordershistory poh ON poh.reader_id = r.id
         JOIN publications_publication p on poh.publication_id = p.id
         JOIN libraries_librarian l on l.id = poh.given_librarian_id
         JOIN libraries_readingroom rr on l.reading_room_id = rr.id and rr.library_id = r.issuer_library_id
WHERE r.id = %s
            """, [reader_id])
            table = PublicationTable(publications)
    else:
        form = ReaderChoiceForm()

    return render(request, 'form_and_table.html',
                  {'links': links,
                   'title': query_name.replace('_', ' '),
                   'url_name': query_name, 'form': form,
                   'table': table}
                  )


def publications_not_from_readers_issuer_library(request):
    query_name = 'publications_not_from_readers_issuer_library'
    table = None
    if request.method == 'POST':
        form = ReaderChoiceForm(request.POST)
        if form.is_valid():
            reader_id = form.cleaned_data['reader'].pk
            publications = Publication.objects.raw("""
SELECT p.id, item_no, p.title, publisher, language, pages, publication_date, count
FROM readers_reader r
         JOIN lending_publicationsordershistory poh ON poh.reader_id = r.id
         JOIN publications_publication p on poh.publication_id = p.id
         JOIN libraries_librarian l on l.id = poh.given_librarian_id
         JOIN libraries_readingroom rr on l.reading_room_id = rr.id and rr.library_id != r.issuer_library_id
WHERE r.id = %s
            """, [reader_id])
            table = PublicationTable(publications)
    else:
        form = ReaderChoiceForm()

    return render(request, 'form_and_table.html',
                  {'links': links,
                   'title': query_name.replace('_', ' '),
                   'url_name': query_name, 'form': form,
                   'table': table}
                  )


def literacy_works_from_storage_location(request):
    query_name = 'literacy_works_from_storage_location'
    table = None
    if request.method == 'POST':
        form = StorageLocationChoiceForm(request.POST)
        if form.is_valid():
            storage_location_id = form.cleaned_data['storage_location'].pk
            literacy_works = LiteracyWork.objects.raw("""
SELECT lw.id, lw.title
FROM publications_literacywork lw
         JOIN publications_publication_literacy_works plw on lw.id = plw.literacywork_id
         JOIN publications_publication p on p.id = plw.publication_id
         JOIN lending_publicationsordershistory poh on p.id = poh.publication_id
         JOIN libraries_storagelocation_publications psl on p.id = psl.publication_id
         JOIN libraries_storagelocation sl on psl.storagelocation_id = sl.id
         JOIN libraries_readingroom rr on sl.reading_room_id = rr.id
         JOIN libraries_library library on rr.library_id = library.id
WHERE storagelocation_id = %s and poh.received_timestamp IS NULL
            """, [storage_location_id])
            table = LiteracyWorkTable(literacy_works)
    else:
        form = StorageLocationChoiceForm()

    return render(request, 'form_and_table.html',
                  {'links': links,
                   'title': query_name.replace('_', ' '),
                   'url_name': query_name, 'form': form,
                   'table': table}
                  )


def readers_served_by_librarian_in_date_range(request):
    query_name = 'readers_served_by_librarian_in_date_range'
    table = None
    if request.method == 'POST':
        form = LibrarianAndDateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date'].isoformat()
            end_date = form.cleaned_data['end_date'].isoformat()
            librarian_id = form.cleaned_data['librarian'].pk
            readers = Reader.objects.raw("""
SELECT r.id, r.full_name, issue_date, issuer_id, issuer_library_id
FROM readers_reader r
         JOIN lending_publicationsordershistory poh ON r.id = poh.reader_id
         JOIN libraries_librarian l on l.id = poh.given_librarian_id OR l.id = poh.received_librarian_id
WHERE cast(poh.given_timestamp as date) BETWEEN %s AND %s
  AND l.id = %s
GROUP BY r.id
            """, [start_date, end_date, librarian_id])
            table = ReaderTable(readers)
    else:
        form = LibrarianAndDateRangeForm()

    return render(request, 'form_and_table.html',
                  {'links': links,
                   'title': query_name.replace('_', ' '),
                   'url_name': query_name, 'form': form,
                   'table': table}
                  )


def librarians_readers_served_in_date_range(request):
    query_name = 'librarians_readers_served_in_date_range'
    table = None
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date'].isoformat()
            end_date = form.cleaned_data['end_date'].isoformat()
            librarians = Librarian.objects.raw("""
SELECT l.id, full_name, count(l.id) as readers_count
FROM libraries_librarian l
         JOIN (SELECT given_librarian_id as librarian_id
               FROM lending_publicationsordershistory poh
               WHERE cast(poh.given_timestamp as date) BETWEEN %s AND %s
               union all
               SELECT received_librarian_id
               FROM lending_publicationsordershistory poh
               WHERE cast(poh.given_timestamp as date) BETWEEN %s AND %s) poh
              ON poh.librarian_id = l.id
GROUP BY l.id
ORDER BY readers_count DESC
            """, [start_date, end_date, start_date, end_date])
            table = LibrarianWithReadersCount(librarians)
    else:
        form = DateRangeForm()

    return render(request, 'form_and_table.html',
                  {'links': links,
                   'title': query_name.replace('_', ' '),
                   'url_name': query_name,
                   'form': form,
                   'table': table}
                  )


def readers_with_outdated_orders(request):
    query_name = 'readers_with_outdated_orders'
    readers = Reader.objects.raw("""
SELECT r.id, full_name, issue_date, issuer_id, issuer_library_id
FROM lending_publicationsordershistory poh
         JOIN lending_lendingrestriction lr on lr.id = poh.lending_restriction_id
         JOIN readers_reader r on poh.reader_id = r.id
WHERE poh.received_timestamp IS NULL
  AND poh.given_timestamp + lr.time_limit < now()
            """)
    table = ReaderTable(readers)

    return render(request, 'form_and_table.html',
                  {'links': links,
                   'title': query_name.replace('_', ' '),
                   'url_name': query_name,
                   'table': table}
                  )


def literacy_works_flow_in_date_range(request):
    query_name = 'literacy_works_flow_in_date_range'
    table = None
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date'].isoformat()
            end_date = form.cleaned_data['end_date'].isoformat()
            readers = Reader.objects.raw("""
SELECT p.id, item_no, title, publisher, language, pages, publication_date
FROM libraries_publicationsflowhistory pfh
         JOIN publications_publication p on pfh.publication_id = p.id
WHERE cast(pfh.record_timestamp as date) BETWEEN %s AND %s
            """, [start_date, end_date])
            table = LiteracyWorkTable(readers)
    else:
        form = DateRangeForm()

    return render(request, 'form_and_table.html',
                  {'links': links,
                   'title': query_name.replace('_', ' '),
                   'url_name': query_name,
                   'form': form,
                   'table': table}
                  )


def readers_not_seen_in_date_range(request):
    query_name = 'readers_not_seen_in_date_range'
    table = None
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date'].isoformat()
            end_date = form.cleaned_data['end_date'].isoformat()
            readers = Reader.objects.raw("""
SELECT r.id, full_name, issue_date, issuer_id, issuer_library_id, MAX(rvh.last_order_visit_timestamp) last_visit_timestamp
FROM (SELECT reader_id, GREATEST(given_timestamp, received_timestamp) last_order_visit_timestamp
      FROM lending_publicationsordershistory) rvh
         JOIN readers_reader r ON r.id = rvh.reader_id
GROUP BY r.id
HAVING cast(MAX(rvh.last_order_visit_timestamp) as date) NOT BETWEEN %s AND %s
            """, [start_date, end_date])
            table = ReaderTable(readers)
    else:
        form = DateRangeForm()

    return render(request, 'form_and_table.html',
                  {'links': links,
                   'title': query_name.replace('_', ' '),
                   'url_name': query_name, 'form': form,
                   'table': table}
                  )


def top_5_books_by_polularity(request):
    query_name = 'top_5_books_by_polularity'
    literacy_works = LiteracyWork.objects.raw("""
SELECT lw.id, lw.title, count(lw.id) as orders_count
FROM publications_literacywork lw
         JOIN publications_publication_literacy_works plw on lw.id = plw.literacywork_id
         JOIN lending_publicationsordershistory poh on plw.publication_id = poh.publication_id
GROUP BY lw.id, lw.title
ORDER BY orders_count DESC, lw.title
LIMIT 5
            """)
    table = LiteracyWorksWithOrdersCount(literacy_works)

    return render(request, 'form_and_table.html',
                  {'links': links,
                   'title': query_name.replace('_', ' '),
                   'url_name': query_name,
                   'table': table}
                  )
