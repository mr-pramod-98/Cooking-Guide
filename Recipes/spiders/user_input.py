from fuzzywuzzy import process


class UserInput:

    def read(self):

        item = input("enter the item name :")
        return item


class Filter:

    def optimize_search_result(self, string, reference):

        # reference -> {title : url}
        choices = []
        optimized_result = {}

        # CREATING A LIST USING THE keys IN THE "reference"
        for key in reference.keys():
            choices.append(key)

        # GETTING RELEVENT SEARCH RESULTS
        # result -> [(title, probability)]
        results = process.extract(string, choices, limit=5)

        # OPTIMIZING THE SEARCH RESULTS
        # optimized_result -> {title : url}
        for item in results:
            if item[1] > 70:
                optimized_result[item[0]] = reference[item[0]]

        return optimized_result
