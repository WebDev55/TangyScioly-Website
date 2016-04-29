class Markup:
    """
    """

    def __init__(self, file_address):
        self.name = file_address[:file_address.index(".")]
        raw_markup = []
        with open(file_address, "rt") as markup_file:
            for i in markup_file.readlines():
                raw_markup.extend(list(i.strip().replace('""', "''")))
        raw_markup_packed = enumerate(raw_markup)

        #Getting rules
        self.rules = None
        for index, i for i in raw_markup_packed:
            if i == "{" and index > 0:
                if not "(" in raw_markup[0:index]:
                    self.rules = {}
                    rule_start = index
                    rule_end = None
                    break
            elif i == "}" and len(raw_markup) - index > 2:
                for j in range(index, len(raw_markup)):
                    if j != 
