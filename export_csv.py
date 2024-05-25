from datetime_management import timestamp_to_readable
import gui
import csv


def export_to_csv():
    results_list = gui.last_search_info
    if results_list is None or len(results_list) == 0:
        return
    with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['ID', 'Title', 'Authors', 'Exits', 'Difficulty', 'Submissions', 'Earliest Submission',
                         'Latest Submission', 'Acceptances', 'Earliest Acceptance', 'Latest Acceptance', 'Demo',
                         'Hall of Fame'])
        for result in results_list:
            formatted_authors = ', '.join(eval(result.authors))
            formatted_submissions = ', '.join(map(str, eval(result.submissions)))
            formatted_acceptances = ', '.join(map(str, eval(result.acceptances)))
            list_to_write = [result.id, result.title, formatted_authors, result.exits, result.difficulty,
                             formatted_submissions, timestamp_to_readable(result.earliest_submission),
                             timestamp_to_readable(result.latest_submission), formatted_acceptances,
                             timestamp_to_readable(result.earliest_acceptance),
                             timestamp_to_readable(result.latest_acceptance), result.demo, result.hall_of_fame]
            writer.writerow(list_to_write)
