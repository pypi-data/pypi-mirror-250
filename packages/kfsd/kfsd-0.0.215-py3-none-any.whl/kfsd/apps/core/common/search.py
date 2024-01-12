from django.db.models import Q
from functools import reduce
import operator


class SearchQuery():
    def __init__(self, op):
        self.__op = op
        self.__items = []

    def add(self, fieldName, fieldType, fieldValue):
        item = {
            "field": fieldName,
            "type": fieldType,
            "value": fieldValue
        }
        self.__items.append(item)

    def get(self):
        return {
            "op": self.__op,
            "items": self.__items
        }


class SearchQueries():
    ATTR_SEARCH_OP_KEY = "op"
    ATTR_SEARCH_OR_KEY = "or"
    ATTR_SEARCH_AND_KEY = "and"
    ATTR_SEARCH_ITEMS_KEY = "items"
    ATTR_SEARCH_QUERIES_KEY = "queries"
    ATTR_SEARCH_FIELD_KEY = "field"
    ATTR_SEARCH_VAL_TYPE_KEY = "type"
    ATTR_SEARCH_VAL_TYPE_LIST_VALUE = "list"
    ATTR_SEARCH_VAL_KEY = "value"

    def __init__(self, op):
        self.__op = op
        self.__queries = []

    def add(self, query):
        self.__queries.append(query)

    def get(self):
        return {
            "op": self.__op,
            "queries": self.__queries
        }

    def parseSearchItemSet(self, itemsStore, searchItems):
        for item in searchItems:
            searchField = item[self.ATTR_SEARCH_FIELD_KEY]
            searchValType = item[self.ATTR_SEARCH_VAL_TYPE_KEY]
            searchVal = item[self.ATTR_SEARCH_VAL_KEY]
            query = {searchField: searchVal if searchValType == self.ATTR_SEARCH_VAL_TYPE_LIST_VALUE else searchVal[0]}
            itemsStore.append(Q(**query))

    def parseSearchSet(self, queriesStore, queries):
        for query in queries:
            op = query[self.ATTR_SEARCH_OP_KEY]
            items = query[self.ATTR_SEARCH_ITEMS_KEY]
            searchItemsStore = []
            self.parseSearchItemSet(searchItemsStore, items)
            searchItemsQuery = reduce(operator.and_ if op == self.ATTR_SEARCH_AND_KEY else operator.or_, (query for query in searchItemsStore))
            queriesStore.append(searchItemsQuery)

    def toFilterQueries(self):
        searchStore = []
        searchInput = self.get()
        if self.get():
            searchOp = searchInput[self.ATTR_SEARCH_OP_KEY]
            queries = searchInput[self.ATTR_SEARCH_QUERIES_KEY]
            self.parseSearchSet(searchStore, queries)
            return reduce(operator.and_ if searchOp == self.ATTR_SEARCH_AND_KEY else operator.or_, (query for query in searchStore))
        return None

    @staticmethod
    def generate(op, *subqueries):
        searchQueries = SearchQueries(op)
        for query in subqueries:
            if query:
                searchQueries.add(query.get())
        return searchQueries
