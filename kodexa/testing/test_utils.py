def print_data_table(context, store_name):
    """
    A small helper to support working with a store in a test

    :param context:
    :param store_name:
    :return:
    """
    if store_name in context.get_store_names():
        print(f"\n{store_name}\n")
        data_table = context.get_store(store_name)
        from texttable import Texttable
        table = Texttable(max_width=1000).header(data_table.columns)
        table.add_rows(data_table.rows, header=False)
        print(table.draw() + "\n")
    else:
        print(f"\n{store_name} - MISSING\n")
