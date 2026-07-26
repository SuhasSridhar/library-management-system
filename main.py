from enums import Member_Type
from Library.Library import Library


def main():
    library = Library()

    # Add a title and a few copies for the same
    clean_architecture = library.add_book(
        "Clean Architecture",
        "Robert",
        "1234",
        ["CA-1001", "CA-1002", "CA-1003"]
    )
    
    print(f"Title: {clean_architecture.title}")
    print(f"Copies: {len(clean_architecture.copies)}")

    for copy in clean_architecture.copies.values():
       print(copy.barcode)

    print('check availability for the title')
    copies_available = clean_architecture.get_available_copy()
    print(f"Available Book for the title {clean_architecture.title} are {copies_available}")

    # Add students
    member = library.add_member(
        "STU1001",
        "Joshua",
        Member_Type.STUDENT
    )

    print(f"Member Name is {member.name} and Member Id is {member.member_id}")

    checkout_successful = library.borrow("STU1001", "1234")
    if checkout_successful:
        print('Checkout successful')
    else :
        print('Checkout Failed, No available copies exist for this title')

if __name__ == "__main__":
    main()