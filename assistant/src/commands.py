from assistant.src.errors.error_messages import (
    parse_input_error_messages,
    add_contact_error_messages,
    change_phone_error_messages,
    show_contact_error_messages,
    show_all_error_messages,
    add_birthday_error_messages,
    show_all_birthdays_error_messages,
    add_note_error_messages,
    show_all_notes_error_messages,
    change_birthday_error_messages,
    change_email_error_messages,
    change_address_error_messages,
    change_birthday_error_messages,
    find_by_tags_error_messages,
    invalid_per_days_error_message,
    find_by_phone_error_messages,
    find_by_email_error_messages,
    find_by_address_error_messages,
    delete_contact_error_messages,
    find_by_birthday_error_messages,
    change_tag_error_messages,
    delete_note_error_messages,
    show_note_error_messages,
    change_note_title_error_messages,
    change_note_content_error_messages,
    add_tag_error_messages
)
from assistant.src.errors.error_decorator import input_error
from assistant.src.models.address_book import AddressBook
from assistant.src.models.address import Address
from assistant.src.models.notes import Notes
from assistant.src.models.phone import Phone
from assistant.src.models.email import Email
from assistant.src.models.birthday import Birthday
from assistant.src.models.note import Note
from assistant.src.errors.errors import ValidationError
from assistant.src.functions import format_as_table
from assistant.src.constants import commands_description
from assistant.src.errors.errors import ValidationError
from assistant.src.errors.error_messages import invalid_phone_number_error_message

RED = "\33[91m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
RESET = "\033[0m"


@input_error(parse_input_error_messages)
def parse_input(user_input):
    """Parses the user input into a command and its arguments.

    Args:
        user_input (str): The user input string.

    Returns:
        tuple: A tuple containing the command and its arguments.
    """
    user_input.lstrip()
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error(add_note_error_messages)
def add_note(notes: Notes):
    """Adds a new note to the Notes object.

    Prompts the user to enter the title, content, and tags for the note.
    The note is then created using the provided information.

    Args:
        notes (Notes): The Notes object to which the note will be added.

    Returns:
        str: A confirmation message indicating that the note has been added.
    """
    note_title = input('Enter title: ')
    note_text = input('Enter note content: ')
    tags = input('Enter tags separated by comma: ')
    note_tags = [tag.strip() for tag in tags.split(',')]
    notes.create_note(note_title, note_text, note_tags)
    return f'{GREEN}Note added.{RESET}'


def validate_name(name: str) -> str:
    """Validates the input name string.

    Checks if the input name string is at least 1 character long.
    If the name is valid, it returns the name string without any modification.
    If the name is invalid, it raises a ValueError with an appropriate message.

    Args:
        name (str): The input name string to be validated.

    Returns:
        str: The validated name string.

    Raises:
        ValueError: If the name is empty or contains only whitespace characters.
                    The error message indicates that the name must be at least 1 character long.
    """
    if len(name.strip()) < 1:
        raise ValueError("Name must be at least 1 character long.")
    return name


def validate_phone(phone: str) -> str:
    """Validates the input phone number string.

    Attempts to validate the input phone number string using the Phone class's
    validate_and_get method. If the validation succeeds, it returns the validated
    phone number string. If the validation fails and raises a ValidationError,
    it raises a ValueError with the error message from the ValidationError.

    Args:
        phone (str): The input phone number string to be validated.

    Returns:
        str: The validated phone number string.

    Raises:
        ValueError: If the input phone number validation fails due to a ValidationError.
                    The error message is obtained from the ValidationError.
    """
    try:
        return Phone.validate_and_get(phone)
    except ValidationError as ve:
        raise ValueError(str(ve))


def validate_birthday(birthday: str) -> str:
    """Validates the input birthday string.

    Attempts to validate the input birthday string using the Birthday class's
    validate_and_get_value method. If the validation succeeds, it returns the validated
    birthday string. If the validation fails and raises a ValidationError,
    it raises a ValueError with the error message from the ValidationError.

    Args:
        birthday (str): The input birthday string to be validated.

    Returns:
        str: The validated birthday string.

    Raises:
        ValueError: If the input birthday validation fails due to a ValidationError.
                    The error message is obtained from the ValidationError.
    """
    try:
        validated_birthday = Birthday.validate_and_get_value(birthday)
        return validated_birthday
    except ValidationError as ve:
        raise ValueError(str(ve))


def validate_email(email: str) -> str:
    """Validates the input email string.

    Attempts to validate the input email string using the Email class's
    validate_and_get_email method. If the validation succeeds, it returns the validated
    email string. If the validation fails and raises a ValidationError,
    it raises a ValueError with the error message from the ValidationError.

    Args:
        email (str): The input email string to be validated.

    Returns:
        str: The validated email string.

    Raises:
        ValueError: If the input email validation fails due to a ValidationError.
                    The error message is obtained from the ValidationError.
    """
    try:
        validated_birthday = Email.validate_and_get_email(email)
        return validated_birthday
    except ValidationError as ve:
        raise ValueError(str(ve))


@input_error(add_tag_error_messages)
def add_tag(args, notes: Notes):
    """Adds a tag to a specific note.

    Adds a tag to the note specified by its ID. The function expects two arguments
    in the `args` list: the note ID and the tag to be added. If the length of `args`
    is not equal to 2, a ValueError is raised.

    Args:
        args (list): A list containing two elements: note ID and tag to be added.
        notes (Notes): An instance of the Notes class managing the notes.

    Returns:
        str: A message indicating that the tag has been added successfully.

    Raises:
        ValueError: If the length of `args` is not equal to 2.
    """
    if (len(args) != 2):
        raise ValueError
    note_id, tag = args
    notes.add_tag(note_id, tag)
    return f'{GREEN}Tag added.{RESET}'


@input_error(change_note_title_error_messages)
def change_title(args, notes: Notes):
    """Changes the title of a specific note.

    Changes the title of the note specified by its ID. The function expects one argument
    in the `args` list: the ID of the note whose title is to be changed. If the length
    of `args` is not equal to 1, a ValueError is raised. After obtaining the existing
    note based on the ID, the user is prompted to enter the new title. The function then
    updates the title of the note with the new title provided.

    Args:
        args (list): A list containing a single element: the ID of the note whose title
            is to be changed.
        notes (Notes): An instance of the Notes class managing the notes.

    Returns:
        str: A message indicating that the title of the note has been changed successfully.

    Raises:
        ValueError: If the length of `args` is not equal to 1.
    """
    if (len(args) != 1):
        raise ValueError
    note_id = args[0]
    existing_note = notes.validate_and_get_note(note_id)
    new_title = input('Enter new title: ')
    notes.change_title(existing_note, new_title)
    return f'{GREEN}Note title changed.{RESET}'


@input_error(change_note_content_error_messages)
def change_content(args, notes: Notes):
    """Changes the content of a specific note.

    Changes the content of the note specified by its ID. The function expects one argument
    in the `args` list: the ID of the note whose content is to be changed. If the length
    of `args` is not equal to 1, a ValueError is raised. After obtaining the existing
    note based on the ID, the user is prompted to enter the new content. The function then
    updates the content of the note with the new content provided.

    Args:
        args (list): A list containing a single element: the ID of the note whose content
            is to be changed.
        notes (Notes): An instance of the Notes class managing the notes.

    Returns:
        str: A message indicating that the content of the note has been changed successfully.

    Raises:
        ValueError: If the length of `args` is not equal to 1.
    """
    if (len(args) != 1):
        raise ValueError
    note_id = args[0]
    existing_note = notes.validate_and_get_note(note_id)
    new_content = input('Enter new content: ')
    notes.change_content(existing_note, new_content)
    return f'{GREEN}Note content changed.{RESET}'


@input_error(add_contact_error_messages)
def add_contact(book: AddressBook):
    """Adds a new contact to the address book.

    This function prompts the user to input various details of the contact,
    including name, phone number, email, birthday, and address. It validates
    each input according to specific criteria. The name and phone number are
    mandatory fields and must not be empty. The email, birthday, and address
    are optional fields. If the user enters an empty value for email, birthday,
    or address, the function skips the validation for that field.

    Args:
        book (AddressBook): An instance of the AddressBook class managing contacts.

    Returns:
        str: A message indicating that the contact has been successfully added.

    Raises:
        ValueError: If any of the input values fail validation.
    """
    validated_name = ''
    validated_email = ''
    validated_birthday = ''
    validated_address = ''

    while True:
        name_add = input('Enter name: ')
        if not name_add.strip():
            print("Name can't be empty.")
            continue
        try:
            validated_name = validate_name(name_add)
            break
        except ValueError as ve:
            print(ve)

    while True:
        phone_add = input('Enter phone: ')
        if not phone_add.strip():
            print("Phone can't be empty.")
            continue
        else:
            try:
                validated_phone = validate_phone(phone_add)
                break
            except ValueError as ve:
                print(ve)

    while True:
        email_add = input('Enter email: ')
        if not email_add.strip():
            break
        try:
            validated_email = validate_email(email_add)
            break
        except ValueError as ve:
            print(ve)

    while True:
        birthday_add = input('Enter birthday: ')
        if not birthday_add.strip():
            break
        try:
            validated_birthday = validate_birthday(birthday_add)
            break
        except ValueError as ve:
            print(ve)

    while True:
        address_add = input('Enter address: ')
        if not address_add.strip():
            break
        try:
            validated_address = address_add
            break
        except ValueError as ve:
            print(ve)

    book.create_record(validated_name, validated_phone,
                       validated_email, validated_birthday, validated_address)
    return f'{GREEN}Contact added.{RESET}'


@input_error(change_phone_error_messages)
def change_record_phone(args, book: AddressBook):
    """Changes the phone number of a contact in the address book.

    This function takes three arguments: name, old phone number, and new phone number.
    It verifies that three arguments are provided. Then, it calls the `change_record_phone`
    method of the AddressBook class to update the phone number of the specified contact.

    Args:
        args (list): A list containing three elements: name, old phone number, and new phone number.
        book (AddressBook): An instance of the AddressBook class managing contacts.

    Returns:
        str: A message indicating that the contact has been successfully updated.

    Raises:
        ValueError: If the number of arguments provided is not three.
    """
    if (len(args) != 3):
        raise ValueError
    name, old_phone, new_phone = args
    book.change_record_phone(name, old_phone, new_phone)
    return f'{GREEN}Contact updated.{RESET}'


@input_error(find_by_birthday_error_messages)
def find_by_brithday(args, book: AddressBook):
    """Finds contacts in the address book with a specific birthday.

    This function takes one argument: the birthday to search for. It then calls
    the `find_record_by_birthday` method of the AddressBook class to retrieve
    contacts that match the specified birthday. If no matching records are found,
    it returns a message indicating that no contact was found. Otherwise, it formats
    the matching records as a table using the `format_as_table` function and returns
    the formatted table.

    Args:
        args (list): A list containing one element: the birthday to search for.
        book (AddressBook): An instance of the AddressBook class managing contacts.

    Returns:
        str: A formatted table displaying the contacts with the specified birthday,
             or a message indicating that no contact was found.

    """
    birthday = args[0]
    matching_records = book.find_record_by_birthday(birthday)
    if not matching_records:
        return 'No contact found with this birthday'
    else:
        return format_as_table(matching_records, cell_width=20)


@input_error(find_by_phone_error_messages)
def find_by_phone(args, book: AddressBook):
    """Finds contacts in the address book with a specific phone number.

    This function takes one argument: the phone number to search for. It then calls
    the `find_record_by_phone` method of the AddressBook class to retrieve
    contacts that match the specified phone number. If no matching records are found,
    it returns a message indicating that no contact was found. Otherwise, it formats
    the matching records as a table using the `format_as_table` function and returns
    the formatted table.

    Args:
        args (list): A list containing one element: the phone number to search for.
        book (AddressBook): An instance of the AddressBook class managing contacts.

    Returns:
        str: A formatted table displaying the contacts with the specified phone number,
             or a message indicating that no contact was found.

    """
    phone = args[0]
    matching_records = book.find_record_by_phone(phone)
    if not matching_records:
        return 'No contact found with this phone number'
    else:
        return format_as_table(matching_records, cell_width=20)


@input_error(find_by_email_error_messages)
def find_by_email(args, book: AddressBook):
    """Finds contacts in the address book with a specific email address.

    This function takes one argument: the email address to search for. It then calls
    the `find_record_by_email` method of the AddressBook class to retrieve
    contacts that match the specified email address. If no matching records are found,
    it returns a message indicating that no contact was found. Otherwise, it formats
    the matching records as a table using the `format_as_table` function and returns
    the formatted table.

    Args:
        args (list): A list containing one element: the email address to search for.
        book (AddressBook): An instance of the AddressBook class managing contacts.

    Returns:
        str: A formatted table displaying the contacts with the specified email address,
             or a message indicating that no contact was found.

    """
    email = args[0]
    matching_records = book.find_record_by_email(email)
    if not matching_records:
        return 'No contact found with this email'
    else:
        return format_as_table(matching_records, cell_width=20)


@input_error(find_by_address_error_messages)
def find_by_address(args, book: AddressBook):
    """Finds contacts in the address book with a specific address.

    This function takes one argument: the address to search for. It then calls
    the `find_record_by_address` method of the AddressBook class to retrieve
    contacts that match the specified address. If no matching records are found,
    it returns a message indicating that no contact was found. Otherwise, it formats
    the matching records as a table using the `format_as_table` function and returns
    the formatted table.

    Args:
        args (list): A list containing one element: the address to search for.
        book (AddressBook): An instance of the AddressBook class managing contacts.

    Returns:
        str: A formatted table displaying the contacts with the specified address,
             or a message indicating that no contact was found.

    """
    address = args[0]
    matching_records = book.find_record_by_address(address)
    if not matching_records:
        return 'No contact found with this address'
    else:
        return format_as_table(matching_records, cell_width=20)


@input_error(show_contact_error_messages)
def show_contact(args, book: AddressBook):
    """Displays the details of a specific contact.

    This function takes one argument: the name of the contact to display.
    It then calls the `show_record` method of the AddressBook class to retrieve
    the details of the specified contact. The details are formatted as a table
    using the `format_as_table` function and returned.

    Args:
        args (list): A list containing one element: the name of the contact to display.
        book (AddressBook): An instance of the AddressBook class managing contacts.

    Returns:
        str: A formatted table displaying the details of the specified contact.

    Raises:
        ValueError: If the number of arguments provided is not equal to 1.

    """
    if (len(args) != 1):
        raise ValueError
    return format_as_table(book.show_record(args[0]), 40)


@input_error(show_all_error_messages)
def show_all_contacts(book: AddressBook):
    """Displays all contacts stored in the address book.

    This function retrieves all contacts stored in the specified AddressBook
    instance using the `get_record_contacts` method. If no contacts are found,
    it raises a ValueError. Otherwise, it formats the contacts as a table
    using the `format_as_table` function and returns the formatted table.

    Args:
        book (AddressBook): An instance of the AddressBook class managing contacts.

    Returns:
        str: A formatted table displaying all contacts stored in the address book.

    Raises:
        ValueError: If no contacts are found in the address book.

    """
    contacts = book.get_record_contacts()
    if not contacts:
        raise ValueError
    return format_as_table(contacts, 20)


@input_error(show_all_notes_error_messages)
def show_all_notes(notes: Notes):
    """Displays all notes stored in the Notes instance.

    This function retrieves all notes stored in the specified Notes instance
    using the `get_dict_notes` method. If no notes are found, it raises a ValueError.
    Otherwise, it formats the notes as a table using the `format_as_table` function
    and returns the formatted table.

    Args:
        notes (Notes): An instance of the Notes class managing notes.

    Returns:
        str: A formatted table displaying all notes stored in the Notes instance.

    Raises:
        ValueError: If no notes are found in the Notes instance.

    """
    note_list = notes.get_notes()
    if not notes:
        raise ValueError
    return format_as_table(notes.get_dict_notes(), 40)


@input_error(change_tag_error_messages)
def change_tag(args, notes: Notes):
    """Changes a tag associated with a specific note.

    This function modifies the tag associated with a specific note in the Notes instance.
    It takes three arguments: the ID of the note, the old tag to be replaced,
    and the new tag to replace it with. It then calls the `change_tag` method
    of the Notes instance to perform the tag change operation.

    Args:
        args (list): A list containing the ID of the note, the old tag, and the new tag.
        notes (Notes): An instance of the Notes class managing notes.

    Returns:
        str: A message confirming that the tag has been successfully changed.

    """
    id, old_tag, new_tag = args
    changed_note = notes.change_tag(id, old_tag, new_tag)
    return f'{GREEN}Tag changed.{RESET}'


@input_error(add_note_error_messages)
def find_by_title(args, notes: Notes):
    """Finds notes by their title.

    This function searches for notes with a specific title in the Notes instance.
    It takes two arguments: the title of the note to search for, and the Notes instance.
    It then calls the `find_record_title` method of the Notes instance to perform the search.

    Args:
        args (list): A list containing the title of the note to search for.
        notes (Notes): An instance of the Notes class managing notes.

    Returns:
        str: A formatted table displaying the notes with matching titles,
        or a message indicating that no notes were found with the specified title.

    """
    title = args[0]
    result = notes.find_record_title(title)
    if result:
        return format_as_table(result, 40)
    else:
        return f"{YELLOW}There are no notes for such title: [{title}]{RESET}"


@input_error(add_note_error_messages)
def find_by_content(args, notes: Notes):
    """Finds notes by their content.

    This function searches for notes containing specific text in their content.
    It takes two arguments: the text to search for, and the Notes instance.
    It then calls the `find_record_content` method of the Notes instance to perform the search.

    Args:
        args (list): A list containing the text to search for within note content.
        notes (Notes): An instance of the Notes class managing notes.

    Returns:
        str: A formatted table displaying the notes containing the specified text in their content,
        or a message indicating that no notes were found with the specified content.

    """
    text = args[0]
    result = notes.find_record_content(text)
    if result:
        return format_as_table(result, 40)
    else:
        return f"{YELLOW}There are no notes for such content: [{text}]{RESET}"


@input_error(find_by_tags_error_messages)
def find_by_tags(args, notes: Notes):
    """Finds notes by their tags.

    This function searches for notes based on the presence of specified tags.
    It takes two arguments: a list of tags to search for, and the Notes instance.
    The list of tags is extracted from the input arguments and split by commas.
    Then, it calls the `find_record_tags` method of the Notes instance to perform the search.

    Args:
        args (list): A list containing tags separated by commas.
        notes (Notes): An instance of the Notes class managing notes.

    Returns:
        str: A formatted table displaying the notes containing the specified tags,
        or a message indicating that no notes were found with the specified tags.

    """"""Finds notes by their tags.

    This function searches for notes based on the presence of specified tags.
    It takes two arguments: a list of tags to search for, and the Notes instance.
    The list of tags is extracted from the input arguments and split by commas.
    Then, it calls the `find_record_tags` method of the Notes instance to perform the search.

    Args:
        args (list): A list containing tags separated by commas.
        notes (Notes): An instance of the Notes class managing notes.

    Returns:
        str: A formatted table displaying the notes containing the specified tags,
        or a message indicating that no notes were found with the specified tags.

    """
    tags = [tag.strip() for arg in args for tag in arg.split(',')]
    result = notes.find_record_tags(tags)
    if result:
        return format_as_table(result, 40)
    else:
        return f"{YELLOW}There are no notes for such tags: [{', '.join(tags)}]{RESET}"


@input_error(add_note_error_messages)
def sort_by_tag(args, notes: Notes):
    """Sorts notes by tags.

    This function sorts notes based on two specified tags.
    It takes two arguments: tag1 and tag2, representing the tags to sort by,
    and the Notes instance managing the notes.
    It then calls the `sort_record_tag` method of the Notes instance to perform the sorting.

    Args:
        args (list): A list containing two tags to sort by.
        notes (Notes): An instance of the Notes class managing notes.

    Returns:
        str: A formatted table displaying the sorted notes based on the specified tags.

    """
    tag1, tag2 = args
    result = notes.sort_record_tag(tag1, tag2)
    return format_as_table(result, 40)


@input_error(show_note_error_messages)
def show_note(args, notes: Notes):
    """Displays a single note.

    This function retrieves and displays a single note based on the provided note ID.
    It takes two arguments: args, a list containing a single note ID,
    and notes, an instance of the Notes class managing the notes.
    It then calls the `show_note` method of the Notes instance to retrieve the note details,
    and formats the result as a table using the `format_as_table` function.

    Args:
        args (list): A list containing a single note ID.
        notes (Notes): An instance of the Notes class managing notes.

    Returns:
        str: A formatted table displaying the details of the specified note.

    Raises:
        ValueError: If the number of arguments is not equal to 1.

    """
    if (len(args) != 1):
        raise ValueError
    return format_as_table(notes.show_note(args[0]), 40)


@input_error(delete_note_error_messages)
def delete_note(args, notes: Notes):
    """Deletes a note.

    This function deletes a note specified by its ID.
    It takes two arguments: args, a list containing a single note ID,
    and notes, an instance of the Notes class managing the notes.
    It then calls the `delete_note` method of the Notes instance to delete the note.

    Args:
        args (list): A list containing a single note ID.
        notes (Notes): An instance of the Notes class managing notes.

    Returns:
        str: A message confirming the deletion of the note.

    Raises:
        ValueError: If the number of arguments is not equal to 1.

    """
    if (len(args) != 1):
        raise ValueError
    notes.delete_note(args[0])
    return f'{GREEN}The note was deleted.{RESET}'


@input_error(add_birthday_error_messages)
def add_birthday(args, book: AddressBook):
    """Adds a birthday to a contact.

    This function adds a birthday to the contact specified by their name.
    It takes two arguments: args, a list containing the name and birthday,
    and book, an instance of the AddressBook class managing contacts.
    It then calls the `add_record_birthday` method of the AddressBook instance to add the birthday.

    Args:
        args (list): A list containing the name and birthday.
        book (AddressBook): An instance of the AddressBook class managing contacts.

    Returns:
        str: A message confirming the addition of the birthday.

    """
    name, birthday = args
    book.add_record_birthday(name, birthday)
    return f'{GREEN}Birthday added.{RESET}'


@input_error(change_birthday_error_messages)
def change_birthday(args, book: AddressBook):
    """Changes the birthday of a contact.

    This function changes the birthday of the contact specified by their name.
    It takes two arguments: args, a list containing the name and new birthday,
    and book, an instance of the AddressBook class managing contacts.
    It then calls the `change_record_birthday` method of the AddressBook instance to update the birthday.

    Args:
        args (list): A list containing the name and new birthday.
        book (AddressBook): An instance of the AddressBook class managing contacts.

    Returns:
        str: A message confirming the change of the birthday.

    Raises:
        ValueError: If the number of arguments is not equal to 2.

    """
    if (len(args) != 2):
        raise ValueError
    name, birthday = args
    book.change_record_birthday(name, birthday)
    return f'{GREEN}Birthday changed.{RESET}'

@input_error(change_email_error_messages)
def change_email(args, book: AddressBook):
    """Changes the email address of a contact.

    This function changes the email address of the contact specified by their name.
    It takes two arguments: args, a list containing the name and new email address,
    and book, an instance of the AddressBook class managing contacts.
    It then calls the `change_record_email` method of the AddressBook instance to update the email address.

    Args:
        args (list): A list containing the name and new email address.
        book (AddressBook): An instance of the AddressBook class managing contacts.

    Returns:
        str: A message confirming the change of the email address.

    Raises:
        ValueError: If the number of arguments is not equal to 2.

    """
    if len(args) != 2:
        raise ValueError("Invalid number of arguments")
    name, new_email = args
    book.change_record_email(name, new_email)
    return f'Email for contact {name} changed to {new_email}'


@input_error(change_address_error_messages)
def change_address(args, book: AddressBook):
    """Changes the address of a contact.

    This function changes the address of the contact specified by their name.
    It takes two arguments: args, a list containing the name and new address,
    and book, an instance of the AddressBook class managing contacts.
    It then calls the `change_record_address` method of the AddressBook instance to update the address.

    Args:
        args (list): A list containing the name and new address.
        book (AddressBook): An instance of the AddressBook class managing contacts.

    Returns:
        str: A message confirming the change of the address.

    Raises:
        ValueError: If the number of arguments is not equal to 2.

    """
    if len(args) != 2:
        raise ValueError("Invalid number of arguments")
    name, new_address = args
    book.change_record_address(name, new_address)
    return f'Address for contact {name} changed to {new_address}'


@input_error(show_all_birthdays_error_messages)
def show_all_birthdays(args, book: AddressBook):
    """Displays upcoming birthdays within a specified number of days.

    This function displays the upcoming birthdays within a specified number of days.
    It takes two arguments: args, a list containing the number of days, 
    and book, an instance of the AddressBook class managing contacts.
    It first validates the number of days provided and then retrieves the upcoming birthdays 
    using the `get_record_birthdays_per_week` method of the AddressBook instance.

    Args:
        args (list): A list containing the number of days.
        book (AddressBook): An instance of the AddressBook class managing contacts.

    Returns:
        str: A formatted table of upcoming birthdays within the specified number of days,
             or a message indicating no birthdays within the specified timeframe.

    Raises:
        ValueError: If the number of arguments is not equal to 1, 
                    or if the provided number of days is invalid.
        KeyError: If the AddressBook instance is empty.
    """
    days = args[0].strip()
    if len(args) != 1:
        raise ValueError()
    if not days.isdigit():
        raise ValidationError(invalid_per_days_error_message)
    per_days = int(days)
    if per_days < 1 or per_days > 365:
        raise ValidationError(invalid_per_days_error_message)
    if not book:
        raise KeyError
    birthdays = book.get_record_birthdays_per_week(per_days)
    return format_as_table(birthdays, 40) if birthdays else 'No birthdays for next {days} days.'

@input_error([])
def show_help():
    """Displays help information for available commands.

    This function retrieves the help information for available commands
    and formats it into a table using the `format_as_table` function.

    Returns:
        str: A formatted table displaying help information for available commands.
    """
    return format_as_table(commands_description, 20)


@input_error(delete_contact_error_messages)
def delete_contact(args, book: AddressBook):
    """Deletes a contact from the address book.

    Args:
        args (list): A list containing the name of the contact to be deleted.
        book (AddressBook): The AddressBook object containing the contacts.

    Returns:
        str: A message indicating whether the contact was deleted successfully or not.
    """
    name = args[0]
    deleted = book.delete(name)
    if deleted:
        return f"Contact '{name}' deleted successfully."
    else:
        return f"Contact '{name}' not found."