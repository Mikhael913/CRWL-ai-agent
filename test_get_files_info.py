from functions.get_files_info import get_files_info


def main() -> None:
    print("Result for current directory:")
    print(get_files_info("calculator", "."))

    print("\nResult for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))

    print("\nResult for '/bin':")
    print(get_files_info("calculator", "/bin"))

    print("\nResult for '../':")
    print(get_files_info("calculator", "../"))

if __name__ == "__main__":
    main()
