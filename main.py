import csv

CSV_FILE = "stocks (1).csv"

def load_stocks(filename):
    stocks = []
    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stocks.append({
                "ID": row["ID"],
                "Performance": float(row["Performance"]),
                "Industry": row["Industry"],
                "FoundationYear": int(row["FoundationYear"]),
                "Environment": int(row["Environment"]),
                "Social": int(row["Social"]),
                "Governance": int(row["Governance"]),
            })
    return stocks


def merge_sort_desc(stocks):
    if not stocks:
        return []

    result = stocks[:]
    total = len(result)
    group_size = 1

    while group_size < total:
        merged = []
        left_start = 0

        while left_start < total:
            left_end = min(left_start + group_size - 1, total - 1)
            right_start = left_end + 1
            right_end = min(left_end + group_size, total - 1)

            i = left_start
            j = right_start

            while i <= left_end and j <= right_end:
                if result[i]["Performance"] >= result[j]["Performance"]:
                    merged.append(result[i])
                    i += 1
                else:
                    merged.append(result[j])
                    j += 1

            while i <= left_end:
                merged.append(result[i])
                i += 1

            while j <= right_end:
                merged.append(result[j])
                j += 1

            left_start = right_end + 1

        result = merged
        group_size *= 2

    return result


def apply_filter1(stocks, use_filter1):
    if use_filter1 == "no":
        return stocks[:]

    filtered = []

    for stock in stocks:
        industry_size = sum(
            1 for s in stocks if s["Industry"] == stock["Industry"]
        )

        top25_stocks = industry_size / 4

        stocks_above = sum(
            1 for s in stocks
            if s["Industry"] == stock["Industry"]
            and s["Performance"] > stock["Performance"]
        )

        if stocks_above < top25_stocks:
            filtered.append(stock)

    return filtered


def apply_filter2(stocks, use_filter2, max_year):
    if use_filter2 == "no":
        return stocks[:]

    return [s for s in stocks if s["FoundationYear"] <= max_year]


def apply_filter3(stocks, use_filter3):
    if use_filter3 == "no":
        return stocks[:]

    filtered = []

    for stock in stocks:
        esg_average = (
            stock["Environment"] + stock["Social"] + stock["Governance"]
        ) / 3

        if esg_average >= 7:
            filtered.append(stock)

    return filtered


def format_stock(stock):
    return (
        f"{stock['ID']}: "
        f"Performance={stock['Performance']}, "
        f"Industry={stock['Industry']}, "
        f"FoundationYear={stock['FoundationYear']}, "
        f"ESG=({stock['Environment']},{stock['Social']},{stock['Governance']})"
    )


def main():
    stocks = load_stocks(CSV_FILE)

    # SUB-PROBLEM 1: INPUT
    while True:
        try:
            n = int(input("How many stocks would you like to get? Enter a whole number from 1 to 100:\n> ")) 
        except ValueError:
            print("Invalid number of stocks, please try again.")
            continue

        if not(1 <= n <= 100):
            print("Invalid number of stocks, please try again.")
        else:
            break

    while True:
        use_filter1 = input("Only the best stocks in their industry? (yes/no)\n> ").strip().lower()
        if use_filter1 in ("yes", "no"):
            break

    while True:
        use_filter2 = input("Only companies founded in or before a chosen year? (yes/no)\n> ").strip().lower()
        if use_filter2 in ("yes", "no"):
            break

    max_year = None

    if use_filter2 == "yes":
        while True:
            try:
                max_year = int(input("Enter a year from 1800 to 2020\n> "))
            except ValueError:
                print("Invalid year, please try again.")
                continue

            if 1800 <= max_year <= 2020:
                break

            print("Invalid year, please try again.")

    while True:
        use_filter3 = input("Only companies with a high ESG score? (yes/no)\n> ").strip().lower()

        if use_filter3 in ("yes", "no"):
            break

    # SUB-PROBLEM 2: SORT ALL STOCKS
    stocks = merge_sort_desc(stocks)

    # SUB-PROBLEM 3: APPLY FILTER #1 (TOP-25%)
    stocks_filter1 = apply_filter1(stocks, use_filter1)

    # SUB-PROBLEM 4: APPLY FILTER #2 (YEAR)
    stocks_filter2 = apply_filter2(stocks_filter1, use_filter2, max_year)

    # SUB-PROBLEM 5: APPLY FILTER #3 (ESG)
    stocks_filter3 = apply_filter3(stocks_filter2, use_filter3)

    # SUB-PROBLEM 6: REMOVE STOCKS WITH NEGATIVE PERFORMANCE
    recommended_stocks = [
        s for s in stocks_filter3 if s["Performance"] >= 0]

    positive_stocks_number = len(recommended_stocks)

    # SUB-PROBLEM 7: OUTPUT
    if positive_stocks_number == 0:
        print("No stocks match your filter. Please try again with other filters.")

    elif positive_stocks_number < n:
        print(
            f"Only {positive_stocks_number} stocks match your filter. "
            "Try other filters to see more."
        )
        for stock in recommended_stocks:
            print(format_stock(stock))

    else:
        recommended_stocks_topN = recommended_stocks[:n]
        print(f"Your top {n} recommended stocks are:")
        for stock in recommended_stocks_topN:
            print(format_stock(stock))

main()