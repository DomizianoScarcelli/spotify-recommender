def format_markdown_table(input_table):
    rows = input_table.strip().split('\n')

    # Remove leading/trailing spaces and separators from each row
    rows = [row.strip('|').strip() for row in rows]

    # Find the maximum number of columns in the table
    max_columns = max(len(row.split('|')) for row in rows)

    # Ensure each row has the same number of columns
    formatted_rows = []
    for row in rows:
        columns = row.split('|')
        if len(columns) < max_columns:
            # Add missing columns with empty values
            columns += [''] * (max_columns - len(columns))
        elif len(columns) > max_columns:
            # Trim extra columns
            columns = columns[:max_columns]
        formatted_rows.append(columns)

    # Determine the maximum width of each column
    column_widths = [max(len(columns[i]) for columns in formatted_rows) for i in range(max_columns)]

    # Generate the formatted table with proper spacing and aligned separators
    formatted_table = []
    for row in formatted_rows:
        formatted_row = '|'
        for i, column in enumerate(row):
            formatted_row += ' ' + column.ljust(column_widths[i]) + ' |'
        formatted_table.append(formatted_row)

    return '\n'.join(formatted_table)

def convert_pyspark_to_markdown(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    # Extract table content
    rows = content.strip().split('\n')
    headers = [header.strip() for header in rows[1].split('|')[1:-1]]
    separator = ['-' * (len(header) + 2) for header in headers]
    data_rows = [data.strip() for data in rows[3:-1]]

    # Convert table to Markdown format
    markdown_table = []
    markdown_table.append('| ' + ' | '.join(headers) + ' |')
    markdown_table.append('| ' + ' | '.join(separator) + ' |')
    final_table = '\n'.join(['| ' + ' | '.join(row.split('|')[1:-1]).strip() + ' |' for row in data_rows])
    final_table = format_markdown_table(final_table)
    markdown_table.extend([final_table])

    # Write Markdown table to the output file
    with open(output_file, 'w') as f:
        f.write('\n'.join(markdown_table))

INPUT_TABLES_PATH = "./data/input_tables.txt"
OUTPUT_TABLES_PATH = "./data/output_tables.md"
convert_pyspark_to_markdown(INPUT_TABLES_PATH, OUTPUT_TABLES_PATH)