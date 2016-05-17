from Markup_Builtins import *


class Markup:
    """
    Markup class is the interpreter, generates complex tree of four different objects:
     -Comments
     -Rules
     -Insert_Headers
     -Tags (aka the actual content)

     Only tags are required to make an actual document. The rest are optional. If no tags are found then nothing
     will be generated, even if there are components of everything else.
    """

    def __init__(self, file_address):
        #Getting raw markup from file
        self.name = file_address[:file_address.index(".")]
        raw_markup = []
        with open(file_address, "rt") as markup_file:
            for i in markup_file.readlines():
                raw_markup.extend(list(i.replace('""', "''")))
        raw_markup_packed = enumerate(raw_markup)

        #Getting rules (if they exist)
        self.rules = None
        for index, i in raw_markup_packed:
            #Searching for a bracket that is not in the middle of the document
            if i == "{":
                #Checking above
                markup_above = False
                if index > 0:
                    content_above = raw_markup[0:index].split("\n")
                    for c in content_above:
                        for l in c:
                            if l == "#":
                                break
                            elif l != " ":
                                markup_above = True
                                break
                        if markup_above:
                            break

                #Checking below only if there is code above
                if markup_above:
                    markup_below = False
                    if index < len(raw_markup):
                        content_below = raw_markup[index + 1:].split("\n")
                        for c in content_below:
                            for l in c:
                                if l == "#":
                                    break
                                elif l != " ":
                                    markup_below = True
                                    break
                            if markup_below:
                                break

                #Rules only exist if there is no markup above and there is beneath, or vice versa.
                if not markup_above and markup_below or markup_above and not markup_below:
                    self.rules = True
                    rule_start = index
                    break
                else:
                    raise Markup_Syntax_Error("Markup file must contain tags.")
        if self.rules:
            #Finding the end of the rule
            rule_close = [index for index, i in enumerate(raw_markup[rule_start + 1:]) if i == "}"]
            if len(rule_close) > 0:
                rule_close = rule_close[0]
                raw_rules = ["".join(i) for i in raw_markup[rule_start + 1:rule_close].split(";")]
            else:
                raise Markup_Syntax_Error("Rule closure not found.")

            #Generating rule
            self.rules = []
            for i in raw_rules:
                rule = Rule(i)
                if not rule.rule_header in self.rules:
                    self.rules.append(rule)
                else:
                    raise Markup_Syntax_Error("Two or more rules cannot have the same name.")

        #Getting Insert Headers (if they exist)
        self.insert_headers = None
        initial_start = rule_close[0] if self.rules else 0
        for index, i in enumerate(raw_markup[initial_start:]):
            if i == "/":
                insert_header_begin = 0
                insert_header_end = []
                for l, c in enumerate(raw_markup[index + 1:]):
                    if c == "/" and insert_header_begin < 2:
                        insert_header_begin.append(l)
                    elif c == "\\" and insert_header_begin == 2 and len(insert_header_end) < 2:
                        insert_header_end.append(l)
                if not self.insert_headers:
                    self.insert_headers = [Insert_Header(raw_markup[index:insert_header_end[1] + 1])]
                else:
                    self.insert_headers.append(Insert_Header(raw_markup[index:insert_header_end[1] + 1]))

        #Now getting acutal content(markup tags)
        if self.insert_headers:
            initial_start = insert_header_end[1] + 1
        elif self.rules:
            initial_start = rule_close[0]
        else:
            initial_start = 0
