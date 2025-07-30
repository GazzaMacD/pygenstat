from textnode import TextType, TextNode


def main():
    test_node = TextNode(
        "This is some anchor text", TextType["LINK"].value, "https://www.boot.dev"
    )
    print(test_node)


if __name__ == "__main__":
    main()
