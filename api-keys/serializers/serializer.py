
class Serializer:
    def __init__(self, **kwargs):
        self.data = kwargs
        self.errors = {}
        self.success = True

    def assign_error(self, key, msg):
        self.success = False
        if key not in self.errors.keys():
            self.errors[key] = [msg]
        else:
            self.errors[key].append(msg)

    def validate(self):
        for key in self.data.keys():
            if not self.data[key]:
                self.assign_error(key, " ".join(key.split(r"_")).title() + " required")
        return self.success

    def check_name_length(self, key, min_char=3, max_char=32):
        if self.data[key] and min_char > len(self.data[key]) < max_char:
            self.assign_error(key, " ".join(key.split(r"_")).title() + " must be between {} and {}".format(min_char, max_char))
