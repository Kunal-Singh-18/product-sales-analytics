def display_sales_results(results):

    print("\n" + "=" * 50)
    print("SALES RESULTS".center(50))
    print("=" * 50)

    print(f"Page              : {results['page']}")
    print(f"Page Size         : {results['page_size']}")
    print(f"Records Returned  : {results['records_returned']}")
    print(f"Total Records     : {results['total_records']}")
    print(f"Total Pages       : {results['total_pages']}")

    if not results["sales"]:
        print("\nNo records found.")
        return

    print("\n" + "=" * 50)

    for index, sale in enumerate(results["sales"], start=1):

        print(f"\nRecord {index}")
        print("-" * 50)

        for key, value in sale.items():

            label = key.replace("_", " ").title()

            print(f"{label:<22}: {value}")


def display_analytics_results(results):

    print("\n" + "=" * 50)
    print("ANALYTICS RESULTS".center(50))
    print("=" * 50)

    print(
        f"Metric    : "
        f"{results['metric'].replace('_', ' ').title()}"
    )

    if results["group_by"]:

        print(
            f"Group By  : "
            f"{results['group_by'].replace('_', ' ').title()}"
        )

    data = results["results"]

    if not data:

        print("\nNo results found.")
        return

    print("\n" + "=" * 50)

    for index, row in enumerate(data, start=1):

        print(f"\nRecord {index}")
        print("-" * 50)

        for key, value in row.items():

            label = key.replace("_", " ").title()

            print(f"{label:<22}: {value}")


def display_summary_results(summary):

    print("\n" + "=" * 50)
    print("GENERAL SUMMARY".center(50))
    print("=" * 50)

    for metric, result in summary.items():

        label = metric.replace("_", " ").title()

        if not result:

            value = "No Data"

        else:

            value = result[0][metric]

        print(f"{label:<30}: {value}")