from src.errors.error_messages import (
    parse_input_error_messages,
    add_contact_error_messages,
    change_contact_error_messages,
    show_phone_error_messages,
    show_all_error_messages,
    add_birthday_error_messages,
    show_birthday_error_messages,
    show_all_birthdays_error_messages,
    invalid_per_days_error_message,
    add_note_error_messages,
    show_all_notes_error_messages,
    change_birthday_error_messages
)
from src.errors.error_decorator import input_error
from src.models.address_book import AddressBook
from src.models.notes import Notes
from src.errors.errors import ValidationError
from src.functions import format_as_table
from src.constants import commands_description

RED = "\33[91m"
BLUE = "\33[94m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
PURPLE = '\033[0;35m' 
CYAN = "\033[36m"
END = "\033[0m"

@input_error(parse_input_error_messages)
def parse_input(user_input):
    user_input.lstrip()
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error(add_note_error_messages)
def add_note(notes: Notes):
    note_title = input('Enter title: ')
    note_text = input('Enter note content: ')
    tags = input('Enter tags separated by comma: ')
    note_tags = [tag.strip() for tag in tags.split(',')]
    notes.create_note(note_title, note_text, note_tags)
    return f'{GREEN}Note added.'


@input_error(add_contact_error_messages)
def add_contact(args, book: AddressBook):
    name, phone = args
    book.create_record(name, phone)
    return f'{GREEN}Contact added.'


@input_error(change_contact_error_messages)
def change_contact(args, book: AddressBook):
    name, phone = args
    book.change_record_phone(name, phone)
    return f'{GREEN}Contact updated.'


@input_error(show_phone_error_messages)
def show_phone(args, book: AddressBook):
    if (len(args) != 1):
        raise ValueError
    return book.show_record_phone(args[0])


@input_error(show_all_error_messages)
def show_all_contacts(book: AddressBook):
    contacts = book.get_record_contacts()
    if not contacts:
        raise ValueError
    return '\n'.join(contacts)


@input_error(show_all_notes_error_messages)
def show_all_notes(notes: Notes):
    note_list = notes.get_notes()
    if not notes:
        raise ValueError
    return format_as_table(notes.get_dict_notes(), 40)

'''
    'change-tag <ID> <old_tag> <new_tag>',  done
    'show-note <ID>,  done
    'delete-note <ID>,   done          
                      'find-by-title <title>',
                      'find-by-content <content>',
                      'sort-by-tag <tag> <tag>',
'''
@input_error(add_note_error_messages)
def change_tag(args,notes: Notes):
    id, old_tag, new_tag = args
    changed_note = notes.change_existing_tag(id, old_tag, new_tag)
    return f'{GREEN}Tag changeed. {changed_note}'

@input_error(add_note_error_messages)
def find_by_title(args,notes: Notes):
    title = args[0]
    result = notes.find_title(title)
    return f'{GREEN}Result of search by title: {result}'

@input_error(add_note_error_messages)
def find_by_content(args,notes: Notes):
    text = args[0]
    result = notes.find_content(text)
    return f'{GREEN}Result of search by content: {result}'

@input_error(add_note_error_messages)
def sort_by_tag(args,notes: Notes):
    tag1, tag2 = args
    result = notes.sort_tag(tag1, tag2)
    return f'{GREEN}Result of sort by tag: {result}'

@input_error(add_note_error_messages)
def show_note(args,notes: Notes):
    if (len(args) != 1):
        raise ValueError
    notes.show_exist_note(args[0])
    return f'{GREEN}Here the note.'

@input_error(add_note_error_messages)
def delete_note(args,notes: Notes):
    if (len(args) != 1):
        raise ValueError
    notes.delete_exist_note(args[0])
    return f'{GREEN}The note was deletad. {notes}'


@input_error(add_birthday_error_messages)
def add_birthday(args, book: AddressBook):
    name, birthday = args
    book.add_record_birthday(name, birthday)
    return f'{GREEN}Birthday added.'

@input_error(change_birthday_error_messages)
def change_birthday(args, book: AddressBook):
    if (len(args) != 2):    
        raise ValueError
    name, birthday = args
    book.change_record_birthday(name, birthday)
    return f'{GREEN}Birthday changed.'


@input_error(show_birthday_error_messages)
def show_birthday(args, book: AddressBook):
    if (len(args) != 1):
        raise ValueError
    return book.show_record_birthday(args[0])


@input_error(show_all_birthdays_error_messages)
def show_all_birthdays(args, book: AddressBook):
    days = args[0].strip()
    if len(args) != 1:
       raise ValueError()
    if not days.isdigit():
       raise ValidationError(invalid_per_days_error_message)  
    per_days = int(days)
    if per_days < 1 or per_days > 365:
        raise ValidationError(invalid_per_days_error_message)
    if not book:
        raise KeyError() 
    birthdays = book.get_record_birthdays_per_week(per_days)
    return format_as_table(birthdays, 40) if birthdays else 'No birthdays for next {days} days.'


@input_error([])
def show_help():
    return format_as_table(commands_description, 40)
