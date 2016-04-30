class Markup:
    """
    """

    def __init__(self, file_address):
        self.name = file_address[:file_address.index(".")]
        raw_markup = []
        with open(file_address, "rt") as markup_file:
            for i in markup_file.readlines():
                raw_markup.extend(list(i.replace('""', "''")))
        raw_markup_packed = enumerate(raw_markup)

        #Getting rules
        self.rules = None
        for index, i for i in raw_markup_packed:
            if i == "{":
                if index > 0:
                    #Check first to see if there is no markup above (which means there has to be some below)
                    content_above = [[c for l, c in enumerate(j) if c != " " or l > 0 and "#" in j[0:l]] for j in raw_markup[0:index].split("\n")]
                    valid_position = True
                    for c in content_above:
                        for l, k in enumerate(c):
                            if k == "(":
                                if l > 0 and not "#" in c[0:l]:
                                    valid_position = False
                                    break
                                else:
                                    valid_position = False
                                    break
                            elif k == "/":
                                if l + 2 < len(c) - 1:
                                    if c[l + 1:l + 3] == "//":
                                        if l == 0:
                                            valid_position = False
                                            break
                                        elif not "#" in c[0:l]:
                                            valid_position = False
                                            break
                                elif l > 0 and not "#" in c[0:l]:
                                    valid_position = False
                                    break
                                else:
                                    valid_position = False
                                    break

                    #If not valid, then check to see if there is markup below.
                    if not valid_position:
                        valid_position = True
                        if index < len(raw_markup) - 1:
                            rule_close = None
                            for l, c in enumerate(raw_markup[index + 1:]):
                                if c == "}":
                                    rule_close = l
                                    break
                            if rule_close:
                                content_below = [[c for l, c in enumerate(j) if c != " " or l > 0 and "#" in j[0:l]] for j in raw_markup[index + 1:].split("\n")]
                                for c in content_below:
                                    for l, k in enumerate(c):
                                        #First check for tags.
                                        if k == "(":
                                            if l > 0 and not "#" in c[0:l]:
                                                valid_position = False
                                                break
                                            else:
                                                valid_position = False
                                                break
                                        #Now checking for Insert Headers
                                        elif k == "/":
                                            if l + 2 < len(c) - 1:
                                                if c[l + 1:l + 3] == "//":
                                                    if l == 0:
                                                        valid_position = False
                                                        break
                                                    else:
                                                        if not "#" in c[0:l]:
                                                            valid_position = False
                                                            break
                                            elif l > 0 and not "#" in c[0:l]:
                                                valid_position = False
                                                break
                                            else:
                                                valid_position = False
                                                break
                            else:
                                valid_position = False

                    #If rule is in a valid location, parse rules.
                    if valid_position:
                        rule_contents = raw_markup[index:rule_close]
                        #TODO: Add rule generation.
