from kodexa import Pipeline, RemoteAction


def test_to_yaml():
    # Create the pipeline

    pipeline = Pipeline.from_file('examples/USBankSample.pdf')
    pipeline.add_step(RemoteAction(slug='kodexa/pdf-parser',
                                   options={"layout_analysis_options": {"rollup": "word", "space_multiplier": 1},
                                            "analyze_layout": True},
                                   attach_source=True))

    col_space_multiplier = 3.0
    page_number_re = ".*Page \d+ of \d+$"

    transactions_header_re = '^Date\s+Description.*\s+Amount$'
    continued_re = '^.*\(continued\)$'

    # Extract Other Deposits
    other_deposits_table_tag_name = "Other Deposits"
    other_deposits_re = '^Other Deposits$'
    total_other_deposits_re = '^Total Other Deposits.*\d{2}$'
    balance_re = '^BALANCE YOUR ACCOUNT$'
    pipeline.add_step(RemoteAction(slug='kodexa/pattern-table-tagger',
                                   options={"col_space_multiplier": col_space_multiplier,
                                            "tag_to_apply": other_deposits_table_tag_name,
                                            "page_start_re": other_deposits_re,
                                            "page_end_re": total_other_deposits_re,
                                            "table_start_re": transactions_header_re,
                                            "table_end_re": balance_re,
                                            "col_marker_re": transactions_header_re,
                                            "extract": True,
                                            "extract_options": {'store_name': other_deposits_table_tag_name,
                                                                'header_lines_count': 1,
                                                                'first_col_has_text': True}
                                            }))

    # Extract Card Withdrawals
    card_withdrawals_table_tag_name = "Card Withdrawals"
    card_withdrawals_re = '^Card Withdrawals$'
    subtotal_card_withdrawals_re = '^Card \d{4} Withdrawals Subtotal.*\d{2}.$'
    total_card_withdrawals_re = '^Total Card Withdrawals.*\d{2}.$'
    pipeline.add_step(RemoteAction(slug='kodexa/pattern-table-tagger',
                                   options={"col_space_multiplier": col_space_multiplier,
                                            "tag_to_apply": card_withdrawals_table_tag_name,
                                            "page_start_re": card_withdrawals_re,
                                            "page_end_re": total_card_withdrawals_re,
                                            "table_start_re": transactions_header_re,
                                            "table_end_re": subtotal_card_withdrawals_re,
                                            "col_marker_re": transactions_header_re,
                                            "extract": True,
                                            "extract_options": {'store_name': card_withdrawals_table_tag_name,
                                                                'header_lines_count': 1,
                                                                'first_col_has_text': True}
                                            }))

    # Extract Other Withdrawals
    other_withdrawals_table_tag_name = "Other Withdrawals"
    other_withdrawals_re = '^Other Withdrawals$'
    total_other_withdrawals_re = '^Total Other Withdrawals.*\d{2}.$'
    pipeline.add_step(RemoteAction(slug='kodexa/pattern-table-tagger',
                                   options={"col_space_multiplier": col_space_multiplier,
                                            "tag_to_apply": other_withdrawals_table_tag_name,
                                            "page_start_re": other_withdrawals_re,
                                            "page_end_re": total_other_withdrawals_re,
                                            "table_start_re": transactions_header_re,
                                            "table_end_re": '',
                                            "col_marker_re": transactions_header_re,
                                            "extract": True,
                                            "extract_options": {'store_name': other_withdrawals_table_tag_name,
                                                                'header_lines_count': 1,
                                                                'first_col_has_text': True}
                                            }))

    # Extract Checks
    checks_table_tag_name = "Checks"
    check_transactions_re = '^Check Date .* Ref Number Amount$'
    checks_re = '^Checks Presented Conventionally$'
    checks_paid_re = '.*Conventional Checks Paid.*\d{2}.$'

    pipeline.add_step(RemoteAction(slug='kodexa/pattern-table-tagger',
                                   options={"col_space_multiplier": col_space_multiplier,
                                            "tag_to_apply": checks_table_tag_name,
                                            "page_start_re": checks_re,
                                            "page_end_re": checks_paid_re,
                                            "table_start_re": check_transactions_re,
                                            "table_end_re": '',
                                            "col_marker_re": check_transactions_re,
                                            "extract": True,
                                            "extract_options": {'store_name': checks_table_tag_name,
                                                                'header_lines_count': 1,
                                                                'first_col_has_text': True,
                                                                'tables_in_page_count': 2}
                                            }))

    print(pipeline.to_yaml())


def test_function_step_to_yaml():
    pipeline = Pipeline.from_file('test')

    def do_it(document):
        print("hello")
        return document

    pipeline.add_step(do_it)
    print(pipeline.to_yaml())
