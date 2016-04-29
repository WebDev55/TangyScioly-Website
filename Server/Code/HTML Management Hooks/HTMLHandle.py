import bs4  #Used for HTML document parsing


class htmlTemplate:
    """This class is used to interface with a HTML template.

    This class SHOULD NOT be used with a full-finished HTML document.
    Rather, use this class to develop HTML components (templates) that are
    later incorporated into a complete HTML document.

    Attrs:
    self.name -- name of the template.
    self.parsed_doc -- BeautifulSoup of template's HTML.

    Methods:
    self.insert_in_tag() -- add HTML content inside of a specific HTML tag.
    self.insert_in_section() -- add HTML content inside of specific section
    of the template.
    self.generate_html() -- generate a string of the template's HTML.
    """

    def __init__(self, file_address):
        """Initializes an instance of the HTMLTemplate class.

        Creates an instance of the HTMLTemplate class.

        Positional Arguments:
        file_address -- file address of the template.
        """

        self.name = [:file_address[file_address.index(".")]]
        raw_html = ""
        with open(file_address, "rt") as template_file:
            for i in template_file.readlines():
                raw_html += i

        #First creation of document
        self.parsed_doc = bs4.BeautifulSoup(raw_html, "html.parser")
        #Getting actual template
        self.parsed_doc = self.parsed_doc.find_all_next(string = lambda text:isinstance(text, Comment) and str(text) == "BEGIN_TEMPLATE")
        self.parsed_doc = self.parsed_doc.find_all_previous(string = lambda text:isinstance(text, Comment) and str(text) == "END_TEMPLATE")

    def insert_in_tag(self, tag, content):
        """Inserts content within a specific HTML tag.

        Inserts content into a tag in the document.

        Positional Arguments:
        tag -- specific tag that content is to be inserted into.
        content -- content that is going to be inserted.
        """
        tag = self.parsed_doc.find(tag)
        tag.insert(0, content)

    def insert_in_section(self, section_class, content):
        """Inserts content within a specific section of the HTML.

        Inserts content into a section of the HTML document.

        Positional Arguments:
        section_class -- class of the section that the content will be inserted into.
        content -- the content that is going to be inserted.
        """
        section = self.parsed_doc.find(class_ = section_class)
        section.insert(0, content)

    def generateHTML(self):
        """Generates a string of the HTML.

        Generates a string that contains HTML of the document.

        Returns:
        self.parsed_doc.prettify() - string of the beautified HTML.
        """
        return self.parsed_doc.prettify()
