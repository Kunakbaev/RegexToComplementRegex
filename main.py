from regex_complement import regex_to_complement_regex


# ALPHABET = frozenset("abcdefghijklmnopqrstuvwxyz")
ALPHABET = frozenset("ab")


def main():
    regex = input("Please input your regex: ")
    print(f"Your regex: {regex}")

    complement_regex = regex_to_complement_regex(
        regex,
        ALPHABET,
        generate_images=True,
    )
    print(f"Complement regex: {complement_regex}")


if __name__ == "__main__":
    main()
