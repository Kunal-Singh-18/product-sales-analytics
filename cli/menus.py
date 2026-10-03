import sys
from cli.display import display_analytics_results,display_sales_results,display_summary_results
from cli.visualizations import visualize_results
from cli.api_client import (
    register_user,
    login_user,
    get_sales,
    get_analytics)
from api.constants import (
    METRICS,
    ALLOWED_GROUP_BY_FIELDS,
    RANKING_BASES
)

SALES_FILTERS = [
        ("customer_id", "Customer ID"),
        ("customer_name", "Customer Name"),
        ("city", "City"),
        ("product", "Product"),
        ("category", "Category"),
        ("payment_mode", "Payment Mode"),
        ("order_status", "Order Status"),
        ("customer_type", "Customer Type"),
        ("gender", "Gender"),
        ("sales_channel", "Sales Channel"),
        ("min_amount", "Minimum Amount"),
        ("max_amount", "Maximum Amount"),
        ("min_quantity", "Minimum Quantity"),
        ("max_quantity", "Maximum Quantity"),
        ("min_age", "Minimum Age"),
        ("max_age", "Maximum Age"),
        ("min_rating", "Minimum Rating"),
        ("max_rating", "Maximum Rating"),
        ("year", "Year"),
        ("month", "Month"),
        ("start_date", "Start Date (YYYY-MM-DD)"),
        ("end_date", "End Date (YYYY-MM-DD)"),
        ("limit", "Limit"),
        ("offset", "Offset")
    ]

ANALYTICS_FILTERS = SALES_FILTERS[:-2]

session = {
    "token": None,
    "username": None,
    "role": None
}


def startup_menu():

    while True:

        print("\n" + "=" * 50)
        print("PRODUCT SALES ANALYTICS SYSTEM".center(50))
        print("=" * 50)

        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            register_menu()

        elif choice == "2":
            login_menu()

        elif choice == "3":
            print("\nThank you for using the Product Sales Analytics System.")
            return

        else:
            print("\nInvalid choice. Please try again.")



def register_menu():

    print("\n" + "=" * 50)
    print("REGISTER".center(50))
    print("=" * 50)

    username = input("Username : ").strip()
    password = input("Password : ").strip()

    while True:

        print("\nSelect Role")
        print("1. Viewer")
        print("2. Analyst")

        choice = input("\nChoice : ").strip()

        if choice == "1":
            role = "viewer"
            break

        elif choice == "2":
            role = "analyst"
            break

        else:
            print("\nInvalid choice. Please select 1 or 2.")

    result = register_user(username,password,role)

    if not result["success"]:
        print(f"\n{result['message']}")
        input("\nPress Enter to continue...")
        return

    response = result["response"]

    if response.status_code == 201:

        print(f"\n{response.json()['message']}")

    elif response.status_code == 409:

        print(f"\n{response.json()['detail']}")

    elif response.status_code == 422:

        print()

        for error in response.json()["detail"]:
            print(f"- {error['msg']}")

    else:

        print("\nAn unexpected server error occurred.")

    input("\nPress Enter to continue...")

def login_menu():

    print("\n" + "=" * 50)
    print("LOGIN".center(50))
    print("=" * 50)

    username = input("Username : ").strip()
    password = input("Password : ").strip()

    result = login_user(username, password)

    if not result["success"]:
        print(f"\n{result['message']}")
        input("\nPress Enter to continue...")
        return

    response = result["response"]

    if response.status_code == 200:

        response_data = response.json()

        session["token"] = response_data["access_token"]
        session["username"] = response_data["username"]
        session["role"] = response_data["role"]

        print(
            f"\nWelcome {session['username']} "
            f"({session['role']})!"
        )

        home_menu()

        return

    elif response.status_code == 401:

        print(f"\n{response.json()['detail']}")

    else:

        print("\nAn unexpected server error occurred.")

    input("\nPress Enter to continue...")


def home_menu():

    while True:

        print("\n" + "=" * 50)
        print("HOME".center(50))
        print("=" * 50)

        print(f"Logged in as : {session['username']}")
        print(f"Role         : {session['role'].capitalize()}")

        print("\n1. Sales")
        print("2. Analytics")
        print("3. Logout")
        print("4. Exit")

        choice = input("\nEnter your choice : ").strip()

        if choice == "1":

            sales_menu()

        elif choice == "2":

            if session["role"] != "analyst":

                print("\nYou do not have permission to access Analytics.")

                input("\nPress Enter to continue...")

                continue

            analytics_menu()

        elif choice == "3":

            session["token"] = None
            session["username"] = None
            session["role"] = None

            print("\nLogged out successfully.")

            return

        elif choice == "4":

            print("\nThank you for using the Product Sales Analytics System.")

            sys.exit()

        else:

            print("\nInvalid choice. Please try again.")

def sales_menu():

    while True:

        print("\n" + "=" * 50)
        print("SALES".center(50))
        print("=" * 50)

        print("1. View All Sales")
        print("2. Search Sales")
        print("3. Back")

        choice = input("\nEnter your choice : ").strip()

        if choice == "1":

            result = get_sales(session["token"])

        elif choice == "2":

            print("\nChoose your filters.")
            print("\nLeave blank to skip any filter.\n")

            params = {}

            for key, label in SALES_FILTERS:

                while True:

                    value = input(f"{label:<25}: ").strip()

                    if value == "":
                        break

                    try:

                        if key in (
                            "customer_id",
                            "year",
                            "month",
                            "min_quantity",
                            "max_quantity",
                            "min_age",
                            "max_age",
                            "min_rating",
                            "max_rating",
                        ):
                            value = int(value)

                        elif key in (
                            "min_amount",
                            "max_amount",
                        ):
                            value = float(value)

                    except ValueError:

                        print(f"Invalid value for {label}.")
                        continue

                    params[key] = value
                    break

            result = get_sales(session["token"], params)

        elif choice == "3":

            return

        else:

            print("\nInvalid choice. Please try again.")
            continue

        if not result["success"]:

            print(f"\n{result['message']}")
            input("\nPress Enter to continue...")
            continue

        response = result["response"]

        if response.status_code == 200:

            results=response.json()

            display_sales_results(results)

            while True:

                print("\n1. Return to Sales menu")
                print("2. Back")

                option = input("\nEnter your choice : ").strip()

                if option == "1":

                    break

                elif option == "2":

                    return

                else:

                    print("\nInvalid choice.")

        elif response.status_code in (400, 401, 403):

            print(f"\n{response.json()['detail']}")

        elif response.status_code == 422:

            print()

            for error in response.json()["detail"]:
                print(f"- {error['msg']}")

        else:

            print("\nAn unexpected server error occurred.")

        input("\nPress Enter to continue...")


def analytics_menu():

    while True:

        print("\n" + "=" * 50)
        print("ANALYTICS".center(50))
        print("=" * 50)

        print("1. General Summary")
        print("2. Custom Analytics")
        print("3. Back")

        choice = input("\nEnter your choice : ").strip()

        if choice == "1":

            summary_results = {}

            for metric, config in METRICS.items():

                if not config.get("show_in_summary", False):
                    continue

                result = get_analytics(
                    session["token"],
                    {"metric": metric}
                )

                if not result["success"]:
                    print(result["message"])
                    continue

                response = result["response"]

                if response.status_code == 200:
                    summary_results[metric] = response.json()["results"]

                elif response.status_code in (400, 401, 403, 501):

                    print(f"\n{response.json()['detail']}")
                    input("\nPress Enter to continue...")
                    return

                elif response.status_code == 422:

                    for error in response.json()["detail"]:
                        print(f"- {error['msg']}")

                    input("\nPress Enter to continue...")
                    return

                else:

                    print("\nAn unexpected server error occurred.")
                    input("\nPress Enter to continue...")
                    return

            display_summary_results(summary_results)

            while True:

                print("\n1. Return to Analytics Menu")
                print("2. Back")

                option = input("\nEnter your choice : ").strip()

                if option == "1":

                    break

                elif option == "2":

                    return

                else:

                    print("\nInvalid choice.")

        elif choice == "2":

            params = {}

            print("\nAvailable Metrics:\n")

            for metric in METRICS:
                print(f"- {metric}")

            print()

            while True:

                metric = input("Metric (Required) : ").strip().lower()

                if not metric:
                    print("Metric is required.")
                    continue

                if metric not in METRICS:
                    print("Invalid metric.")
                    continue

                params["metric"] = metric
                break

            print("\nAvailable Group By Fields:\n")

            for field in ALLOWED_GROUP_BY_FIELDS:
                print(f"- {field}")

            print()

            while True:

                value = input("Group By : ").strip().lower()

                if value == "":
                    break

                if value not in ALLOWED_GROUP_BY_FIELDS:
                    print("Invalid Group By field.")
                    continue

                params["group_by"] = value
                break

            print("\nAvailable Ranking Bases:\n")

            for base in RANKING_BASES:
                print(f"- {base}")

            print()

            while True:

                value = input("Based On : ").strip().lower()

                if value == "":
                    break

                if value not in RANKING_BASES:
                    print("Invalid ranking basis.")
                    continue

                params["based_on"] = value
                break

            while True:

                value = input("Direction (top/bottom) : ").strip().lower()

                if value == "":
                    break

                if value not in ("top", "bottom"):
                    print("Direction must be top or bottom.")
                    continue

                params["direction"] = value
                break

            while True:

                value = input("Top N : ").strip()

                if value == "":
                    break

                if not value.isdigit():
                    print("Top N must be a positive integer.")
                    continue

                value = int(value)

                if value < 1 or value > 20:
                    print("Top N must be between 1 and 20.")
                    continue

                params["n"] = value
                break

            print("\nChoose your filters.")
            print("Leave blank to skip any filter.\n")

            for key, label in ANALYTICS_FILTERS:

                while True:

                    value = input(f"{label:<25}: ").strip()

                    if value == "":
                        break

                    try:

                        if key in (
                            "customer_id",
                            "year",
                            "month",
                            "min_quantity",
                            "max_quantity",
                            "min_age",
                            "max_age",
                            "min_rating",
                            "max_rating",
                        ):
                            value = int(value)

                        elif key in (
                            "min_amount",
                            "max_amount",
                        ):
                            value = float(value)

                    except ValueError:

                        print(f"Invalid value for {label}.")
                        continue

                    params[key] = value
                    break

            result = get_analytics(
                session["token"],
                params
            )

            if not result["success"]:

                print(result["message"])
                input("\nPress Enter to continue...")
                continue

            response = result["response"]

            if response.status_code == 200:

                results = response.json()

                display_analytics_results(results)

                while True:

                    print("\n1. Visualize Results")
                    print("2. Return to Analytics Menu")
                    print("3. Back")

                    option = input("\nEnter your choice : ").strip()

                    if option == "1":

                        visualize_results(results)

                    elif option == "2":

                        break

                    elif option == "3":

                        return

                    else:

                        print("\nInvalid choice.")

            elif response.status_code in (400, 401, 403, 501):

                print(f"\n{response.json()['detail']}")

            elif response.status_code == 422:

                print()

                for error in response.json()["detail"]:
                    print(f"- {error['msg']}")
            

            else:

                print("\nAn unexpected server error occurred.")

            input("\nPress Enter to continue...")

        elif choice == "3":

            return

        else:

            print("\nInvalid choice. Please try again.")