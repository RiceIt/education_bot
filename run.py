from parser.models import select_program, insert_program, send_notifications
from parser.platforms import AbstractPlatform, FindAPhD, Euraxess


def main():
    platforms = (FindAPhD,)

    for platform in platforms:
        program_list = platform.get_program_list()
        for program_soup in program_list[:2]:
            created, program = create_program(platform(program_soup))
            if created:
                insert_program(program)
                send_notifications(program)
                print(program.url)
                print(program.slug)
                print(program.title)
                print(program.location)
                print(program.institute)
                print(program.department)
                print(program.type)
                print(program.funding)
                print(program.subjects)
                print(program.description)
                print()


def create_program(platform: AbstractPlatform):
    platform.parse_url()
    platform.parse_slug()
    # if select_program(platform.id_in_platform):
    #     return False, None
    platform.parse_title()
    platform.parse_location()
    platform.parse_institute()
    platform.parse_department()
    platform.parse_type()
    platform.parse_funding()
    platform.parse_subjects()
    platform.parse_description()
    return True, platform


if __name__ == '__main__':
    main()
