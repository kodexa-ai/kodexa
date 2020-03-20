from collections import OrderedDict


class TaggedTableToDataStore:

    def __init__(self, row_tag_re, column_tag_re, data_store, spacer=" "):
        self.row_tag_re = row_tag_re
        self.column_tag_re = column_tag_re
        self.data_store = data_store
        self.spacer = spacer

    def get_name(self):
        return "Tagged Table to Data Store"

    def process(self, document, context):

        rows = self.process_node(document.get_root())

        for row in rows:
            context.get_store(self.data_store).add(row)
        return document

    def process_node(self, node):
        all_rows = []

        for line in node.findall(tag_name_re=self.row_tag_re):
            row = OrderedDict()
            for col in line.findall(tag_name_re=self.column_tag_re):
                if col.get_tags()[0] not in row:
                    row[col.get_tags()[0]] = []
                row[col.get_tags()[0]].append(col.get_all_content())

            all_rows.append(row)

        max_cols = 0

        for row in all_rows:
            if len(row) > max_cols:
                max_cols = len(row)

        final_rows = []

        for row in all_rows:
            final_row = []
            for key, value in row.items():
                final_row.append(self.spacer.join(value))
            for n in range(len(final_row), max_cols):
                final_row.append(None)
            final_rows.append(final_row)

        return final_rows
