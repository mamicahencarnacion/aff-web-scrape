"""
    Created by Ma. Micah Encarnacion on 09/07/2020
"""
import csv
import operator

sample = ["Achichi", "Eishijart", "eunhae9", "EunHaekk", "Eunnhee", "Hxnxbxnxnx", "Jimbam", "mahyukkie", "msmf88", "norahd", "sjlurves", "allrisestrawberry"]


for s in sample:
    norahd = set()
    with open('subscriptions.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1

            if row["username"] == "norahd":
                norahd.add(row["story_id"])

            line_count += 1
        print(f'Processed {line_count} lines.')

    norahd_list = list(norahd)
    tags = []
    with open('stories.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0

        for row in csv_reader:

            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1

            eh_tags = row["tags"].split(",")
            for eh_tag in eh_tags:
                if eh_tag not in tags:
                    tags.append(eh_tag)

            line_count += 1
            if line_count > 718:
                break
        print(f'Processed {line_count} lines.')

    stories_tags = {}
    with open('stories.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0

        with open(f'{s}_stories.csv', mode='w') as subscriptions_file:
            fieldnames = ['story_id', 'title', 'author', 'chapters', 'words', "read"]
            fieldnames.extend(tags)
            writer = csv.DictWriter(subscriptions_file, fieldnames=fieldnames)

            writer.writeheader()

        for row in csv_reader:

            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1

            story_details = {
                    "story_id": row["id"],
                    "title": row["title"].replace("'", ""),
                    "author": row["author"],
                    "chapters": row["chapters"],
                    "words": row["words"],
                    "read": "Yes" if row["id"] in norahd_list else "No"
            }

            for tag in tags:
                stories_tags[tag] = 1 if tag in row["tags"].split(",") else 0

            story_details.update(stories_tags)

            with open(f'{s}_stories.csv', mode='a') as subscriptions_file:
                fieldnames = ['story_id', 'title', 'author', 'chapters', 'words', "read"]
                fieldnames.extend(tags)
                writer = csv.DictWriter(subscriptions_file, fieldnames=fieldnames)

                writer.writerow(story_details)

            line_count += 1
            if line_count > 718:
                break
        print(f'Processed {line_count} lines.')
    print(tags)
    print(len(tags))

    # with open(f'stories.csv', mode='r') as csv_file:
    #     csv_reader = csv.DictReader(csv_file)
    #     line_count = 0
    #
    #     with open(f'stories_processed.csv', mode='w') as subscriptions_file:
    #         fieldnames = ['story_id', 'title', 'author', 'chapters', 'words']
    #         fieldnames.extend(tags)
    #         writer = csv.DictWriter(subscriptions_file, fieldnames=fieldnames)
    #
    #         writer.writeheader()
    #
    #     for row in csv_reader:
    #         if line_count == 0:
    #             print(f'Column names are {", ".join(row)}')
    #
    #         line_count += 1
    #         if line_count <= 718:
    #             continue
    #
    #         story_details = {
    #                 "story_id": row["id"],
    #                 "title": row["title"].replace("'", ""),
    #                 "author": row["author"],
    #                 "chapters": row["chapters"],
    #                 "words": row["words"],
    #         }
    #
    #         for tag in tags:
    #             stories_tags[tag] = 1 if tag in row["tags"].split(",") else 0
    #
    #         story_details.update(stories_tags)
    #
    #         with open(f'stories_processed.csv', mode='a') as subscriptions_file:
    #             fieldnames = ['story_id', 'title', 'author', 'chapters', 'words']
    #             fieldnames.extend(tags)
    #             writer = csv.DictWriter(subscriptions_file, fieldnames=fieldnames)
    #
    #             writer.writerow(story_details)
    #
    #     print(f'Processed {line_count} lines.')
