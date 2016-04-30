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

                #Rules can only exist if there is no markup above and there is beneath (it is at the top of the file), or vice versa.
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
                raw_rule = raw_markup[rule_start + 1:rule_close].split(";")
            else:
                raise Markup_Syntax_Error("Rule closure not found.")

            #Generating rule
            self.rules = {}
            for i in raw_rule:
                rule_header = "".join([c for c in i[:i.index(":")] if c != " "])
                if not rule_header in self.rules.keys():
                    rule_body = ["".join([l for l in c if l != " "]) for c in i[i.index(":") + 1:len(i) - 1].split(",")]
                    self.rules[rule_header] = rule_body
                else:
                    raise Markup_Syntax_Error("Two or more rules cannot have the same name.")

        #Getting insert headers(if they exist)

class StandardShippedRules:
    builtins = {
        "NO_CLOSE": (lambda string: string),
        "CONVERT_TO_UNICODE": (lambda string: unicode(string)),
        "CONVERT_TO_COMMENT": (lambda string: "<!--" + string + "-->"),
        "DEL": (lambda string: "")
        #Add more
    }

class Rule(StandardShippedRules):
    def __init__(self, raw_rule):
        #Restructure
        raw_rule = raw_rule.split(":")
        self.rule_header = "".join([i for i in raw_rule[0] if i != " "]).upper()
        self.rule_applicants = list(set([i for i in raw_rule[1].split(",") if i != " "]))
        if self.rule_header in super(Rule, self).builtins.keys():
            self.rule = super(Rule, self).builtins[self.rule_header]
        else:
            self.rule = pass

    def __str__(self):
        return str(self.rule_header) + ": [" + "".join([i + ", " for index, i in enumerate(self.rule_applicants) if index < len(self.rule_applicants) - 1 else i]) + "]"

    def applyRule(self, string):
        pass
