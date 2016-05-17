#Builtin rules
class StandardShippedRules:
    builtins = {
        #Fix
        "NO_CLOSE": (lambda string: (string, False)),
        "CONVERT_TO_UNICODE": (lambda string: (unicode(string), True)),
        "CONVERT_TO_COMMENT": (lambda string: ("<!--" + string + "-->", False)),
        "DEL": (lambda string: ("", False))
        #Add more
    }

#Markup rule
class Rule(StandardShippedRules):
    def __init__(self, raw_rule):
        #Restructure
        raw_rule = raw_rule.split(":")
        self.rule_header = "".join([i for i in raw_rule[0] if i != " "]).upper()
        if self.rule_header in super().builtins.keys():
            #Fix for custom rules
            self.rule_applicants = list(set([i for i in raw_rule[1].split(",") if i != " "]))
            self.rule = super().builtins[self.rule_header]
        else:
            #Perhaps remove due to security flaws
            self.rule_applicants = None
            if os.path.isfile(self.rule_applicants[0]):
                with open(self.rule_applicants[0], "rt") as rule_file:
                    self.rule = "".join([i.strip() for i in rule_file.readlines()])
                self.rule = (lambda string: eval(self.rule))
            else:
                self.rule = (lambda string: eval(self.rule_applicants))

    def __str__(self):
        if self.rule_applicants:
            return str(self.rule_header) + ": [" + "".join([i + ", " for index, i in enumerate(self.rule_applicants) if index < len(self.rule_applicants) - 1 else i]) + "]"
        else:
            return str(self.rule_header) + ": [" + self.rule_applicants[0] + "]"

    def applyRule(self, string):
        return self.rule(string)


class Insert_Header:
    def __init__(self, raw_insert_header):
        self.insert_class = raw_insert_header[4:len(raw_insert_header) - 4]

    def __str__(self):
        return "///" + self.header + "\\\\\\"


class Tag:
    def __init__(self, raw_tag, applied_rules):
        #Getting name of tag
        for index, i in enumerate(raw_tag):
            if i == "(":
                start_indice = index
                for index, i in enumerate(raw_tag[start_indice:]):
                    if i != " ":
                        start_indice = index
                        break
                for index, i in enumerate(raw_tag[start_indice:]):
                    if i == " ":
                        end_indice = index
                        break
                break
        self.name = raw_tag[start_indice:end_indice]

        #Getting tag attributes
        start_indice = end_indice + 1
        for index, i in enumerate(raw_tag[end_indice:]):
            if i == ")":
                end_indice = index
        tag_attrs = raw_tag[start_indice:end_indice].split("::")
        if set(sorted(tag_attrs)) != set([" "]):
            self.tag_attrs = {}
            for i in tag_attrs:
                attr_name = "".join([c for c in i[:i.index("=")] if c != " "])
                attr_content_bounds = [index for index, c in enumerate(i[i.index("="):]) if c == "'"]
                self.tag_attrs[attr_name] = i[attr_content_bounds[0] + 1:attr_content_bounds[1]]
        else:
            self.tag_attrs = None

        #Getting tag content
        self.tag_content = None
        for index, i in enumerate(raw_tag[end_indice + 1:]):
            if i == "[":
                if raw_tag[index + 1] != "]":
                    start_indice = index + 1
                    self.tag_content = True
                    break
        if self.tag_content:
            for i in range(len(raw_tag) - 1, 0, -1):
                if raw_tag[i] == "]":
                    end_indice = i
                    break
            self.tag_content = raw_tag[start_indice:end_indice]

        #Applied tag rules
        self.applied_rules = applied_rules

    def generateHTMLTag(self):
        if self.applied_rules:
            for i in self.applied_rules:
                i.applyRule(self)
        htmlString = "<" + self.name
        if self.tag_attrs:
            for k, v in self.tag_attrs.items():
                htmlString += " " + k + "=" + v
        htmlString += ">" + self.tag_content + "</" + self.name + ">"
        return htmlString

#Comment class is a sublclass of string
class Comment(str):
    def __new__(self, raw_comment):
        return super().__new__(self, raw_comment[2:])
    def generateHTML(self):
        return "<!--" + super().__str__() + "-->"
